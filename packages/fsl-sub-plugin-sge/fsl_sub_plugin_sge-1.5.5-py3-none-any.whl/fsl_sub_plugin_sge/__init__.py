# fsl_sub plugin for:
#  * Sun Grid Engine
#  * Son of Grid Engine
#  * Open Grid Scheduler
#  * Univa Grid Engine

# Author Duncan Mortimer

import datetime
import logging
import os
import shutil
import subprocess as sp
import warnings
import xml.etree.ElementTree as ET
from collections import defaultdict
from functools import lru_cache
from ruamel.yaml.comments import CommentedMap
from shutil import which

from fsl_sub.exceptions import (
    BadSubmission,
    BadConfiguration,
    MissingConfiguration,
    GridOutputError,
    UnknownJobId,
)
from fsl_sub.config import (
    method_config,
    coprocessor_config,
    queue_config,
)
import fsl_sub.consts
from fsl_sub.coprocessors import (
    coproc_get_module
)
from fsl_sub.shell_modules import (
    loaded_modules
)
from fsl_sub.utils import (
    affirmative,
    split_ram_by_slots,
    parse_array_specifier,
    bash_cmd,
    flatten_list,
    fix_permissions,
    job_script,
    write_wrapper,
    human_to_ram,
    update_envvar_list,
)
from .version import PLUGIN_VERSION


METHOD_NAME = 'sge'


def plugin_version():
    return PLUGIN_VERSION


def qtest():
    '''Command that confirms method is available'''
    return qconf_cmd()


def qconf_cmd():
    '''Command that queries queue configuration'''
    qconf = which('qconf')
    if qconf is None:
        raise BadSubmission("Cannot find Grid Engine software")
    return qconf


def qhost_cmd():
    '''Command that queries host information'''
    qhost = which('qhost')
    if qhost is None:
        raise BadSubmission("Cannot find Grid Engine software")
    return qhost


@lru_cache()
def qstat_cmd():
    '''Command that queries queue state'''
    qstat = which('qstat')
    if qstat is None:
        raise BadSubmission("Cannot find Grid Engine software")
    return qstat


@lru_cache()
def qacct_cmd():
    '''Command that queries completed job stats'''
    qacct = which('qacct')
    if qacct is None:
        raise BadSubmission("Cannot find Grid Engine software")
    return qacct


def qsub_cmd():
    '''Command that submits a job'''
    qsub = which('qsub')
    if qsub is None:
        raise BadSubmission("Cannot find Grid Engine software")
    return qsub


def qdel(job_id):
    '''Deletes a job - returns a tuple, output, return code'''
    qdel = which('qdel')
    if qdel is None:
        raise BadSubmission("Cannot find Grid Engine software")
    result = sp.run(
        [qdel, str(job_id), ],
        universal_newlines=True,
        stdout=sp.PIPE, stderr=sp.STDOUT
    )
    return (result.stdout, result.returncode)


def queue_exists(qname, qtest=None):
    '''Does qname exist'''
    if qtest is None:
        qtest = qconf_cmd()
    # If user has specified 'q@host' or 'q@host,q@host2' we need to test individually
    if '@' in qname:
        qlist = []
        for q in qname.split(','):
            # We can't simply check for queue@host so lets ignore this and let qsub complain
            qlist.append(q.split('@')[0])
        qname = ','.join(qlist)
    try:
        sp.run(
            [qtest, '-sq', qname],
            stdout=sp.DEVNULL,
            stderr=sp.DEVNULL,
            check=True, universal_newlines=True)
        return True
    except FileNotFoundError:
        raise BadSubmission(
            "Grid Engine software may not be correctly installed")
    except sp.CalledProcessError:
        return False


def _check_pe(pe_name, queue, qconf=None, qstat=None):
    if qconf is None:
        qconf = qconf_cmd()
    if qstat is None:
        qstat = qstat_cmd()
    # Check for configured PE of pe_name
    cmd = sp.run(
        [qconf, '-sp', pe_name],
        stdout=sp.DEVNULL,
        stderr=sp.DEVNULL)
    if cmd.returncode != 0:
        raise BadSubmission(pe_name + " is not a valid PE")

    # Check for availability of PE
    cmd = sp.run(
        [qstat, '-g', 'c', '-pe', pe_name, '-xml'],
        universal_newlines=True,
        stdout=sp.PIPE, stderr=sp.PIPE)
    if (cmd.returncode != 0 or (
            cmd.stderr is not None
            and "error: no such parallel environment" in cmd.stderr)):
        raise BadSubmission(
            "No instances of {} configured".format(pe_name))

    # Check that PE is available on requested queue
    queue_defs = ET.fromstring(cmd.stdout)
    if queue not in [b.text for b in queue_defs.iter('name')]:
        raise BadSubmission(
            "PE {} is not configured on {}".format(pe_name, queue)
        )


def already_queued():
    '''Is this a running Grid Engine job?'''
    mconfig = method_config(METHOD_NAME)
    allow_nested = True if os.getenv('FSLSUB_NESTED', '0') == '1' else False
    if allow_nested:
        return False
    if mconfig.get('allow_nested_queuing', False):
        return False
    return 'JOB_ID' in os.environ.keys()


def _start_mode(queue, qconf=None):
    if qconf is None:
        qconf = qconf_cmd()
    cmd = sp.run(
        [qconf, '-sq', queue],
        universal_newlines=True,
        stdout=sp.PIPE,
        stderr=sp.PIPE)
    if cmd.returncode != 0:
        raise BadSubmission(
            queue + " configuration cannot be found - is it a valid queue: "
            + cmd.stderr)
    for line in cmd.stdout.splitlines():
        if line.startswith('shell_start_mode'):
            (_, mode) = line.strip().split()
    return mode


def _valid_resources(res_defs):
    validity = [True if a else False for a in res_defs if '=' in a]
    return all(validity)


def _resource_dict(res):
    '''Returns a dictionary of key, value from a list of strings of form
    key=value'''

    return dict(a.split('=') for a in res)


def _filter_on_resource_dict(res_list, res_defs):
    '''Return list of resources from res_list that aren't present in the
    resource definitions in res_defs dict'''
    if res_defs is None:
        return res_list
    result = [r for r in res_list if r not in res_defs]
    return result


def _get_queue_time(queues):
    logger = _get_logger()
    queue_times = []
    qconfig = None
    if isinstance(queues, str):
        queues = [queues]
    for timed_q in queues:
        try:
            qconfig = queue_config(timed_q)
        except BadConfiguration:
            logger.debug("Queue {0} not found in config.".format(timed_q))
            logger.debug("Checking for queue without host/group specifier")
            try:
                qname = timed_q.split('@')[0]
                qconfig = queue_config(qname)
            except BadConfiguration:
                logger.debug("Looking for configured queue without host/group specifier")
                for q, config in queue_config().items():
                    if q.split('@')[0] == qname:
                        qconfig = config
                if qconfig is None:
                    logger.debug("Unable to find " + timed_q)

        if qconfig is not None:
            queue_times.append(qconfig['time'])

    # As exceeding this run time will result in job termination get the longest lived queue
    if queue_times:
        return max(queue_times)
    else:
        return None


def _get_logger():
    return logging.getLogger('fsl_sub.' + __name__)


def submit(
        command,
        job_name=None,
        queue=None,
        threads=1,
        array_task=False,
        jobhold=None,
        array_hold=None,
        array_limit=None,
        array_specifier=None,
        parallel_env=None,
        jobram=None,
        jobtime=None,
        resources=None,
        ramsplit=False,
        priority=None,
        mail_on=None,
        mailto=None,
        logdir=None,
        coprocessor=None,
        coprocessor_toolkit=None,
        coprocessor_class=None,
        coprocessor_class_strict=False,
        coprocessor_multi=1,
        usescript=False,
        architecture=None,
        requeueable=True,
        project=None,
        export_vars=None,
        keep_jobscript=False,
        extra_args=None):
    '''Submits the job to a Grid Engine cluster
    Requires:

    command - list containing command to run
                or the file name of the array task file.
                If array_specifier is given then this must be
                a list containing the command to run.
    job_name - Symbolic name for task
    queue - Queue to submit to (may be a comma separated string of multiple queues)

    Optional:
    array_task - is the command is an array task (defaults to False)
    jobhold - id(s) of jobs to hold for (string or list)
    array_hold - complex hold string, integer or list
    array_limit - limit concurrently scheduled array
            tasks to specified number
    array_specifier - n[-m[:s]] n subtasks or starts at n, ends at m with
            a step of s
    parallelenv - parallel environment name
    jobram - RAM required by job (total of all threads)
    jobtime - time (in minutes for task)
    requeueable - may a job be requeued if a node fails
    resources - list of resource request strings
    ramsplit - break tasks into multiple slots to meet RAM constraints
    priority - job priority (0-1023)
    mail_on - mail user on 'a'bort or reschedule, 'b'egin, 'e'nd,
            's'uspended, 'n'o mail
    mailto - email address to receive job info
    logdir - directory to put log files in
    coprocessor - name of coprocessor required
    coprocessor_toolkit - coprocessor toolkit version
    coprocessor_class - class of coprocessor required
    coprocessor_class_strict - whether to choose only this class
            or all more capable
    coprocessor_multi - how many coprocessors you need (or
            complex description) (string)
    usescript - queue config is defined in script
    project - which project to associate this job with
    export_vars - list of environment variables to preserve for job.
            Pass list of 'argument=value' if you wish to change value
            for the submitted jobs
    keep_jobscript - whether to generate (if not configured already) and keep
            a wrapper script for the job
    extra_args - list of scheduler specific arguments to pass through
    '''

    logger = _get_logger()
    if command is None:
        raise BadSubmission(
            "Must provide command line or array task file name")
    if not isinstance(command, list):
        raise BadSubmission(
            "Internal error: command argument must be a list"
        )
    if extra_args is not None and type(extra_args) != list:
        raise BadSubmission(
            "Internal error: extra_args should be a list"
        )

    # Can't just have export_vars=[] in function definition as the list is mutable so subsequent calls
    # will return the updated list!
    if export_vars is None:
        export_vars = []
    my_export_vars = export_vars

    mconf = defaultdict(lambda: False, method_config(METHOD_NAME))
    qsub = qsub_cmd()
    command_args = []
    modules = []
    extra_lines = []

    if isinstance(resources, str):
        resources = [resources, ]

    array_map = {
        'FSLSUB_JOBID_VAR': 'JOB_ID',
        'FSLSUB_ARRAYTASKID_VAR': 'SGE_TASK_ID',
        'FSLSUB_ARRAYSTARTID_VAR': 'SGE_TASK_FIRST',
        'FSLSUB_ARRAYENDID_VAR': 'SGE_TASK_LAST',
        'FSLSUB_ARRAYSTEPSIZE_VAR': 'SGE_TASK_STEPSIZE',
        'FSLSUB_ARRAYCOUNT_VAR': '',
        'FSLSUB_NSLOTS': 'NSLOTS',
    }

    if usescript:
        if len(command) > 1:
            raise BadSubmission(
                "Command should be a grid submission script (no arguments)")
        use_jobscript = False
        keep_jobscript = False
    else:
        if queue is None:
            raise BadSubmission("Queue not specified")
        if type(queue) == str:
            if ',' in queue:
                queues = queue.split(',')
            else:
                queues = [queue, ]
        elif type(queue) == list:
            queues = queue
        pure_queues = [q.split('@')[0] for q in queues]
        use_jobscript = mconf.get('use_jobscript', True)
        if job_name is None:
            job_name = command[0]
        if not keep_jobscript:
            keep_jobscript = mconf.get('keep_jobscript', False)
        if keep_jobscript:
            use_jobscript = True
        # Check Parallel Environment is available
        if parallel_env:
            for q in pure_queues:
                _check_pe(parallel_env, q)
            command_args.append(
                ['-pe', parallel_env, str(threads), ])
            command_args.append(
                ['-R', 'y', ])
        if mconf.get('copy_environment', False):
            command_args.append('-V')
        for var, value in array_map.items():
            if not value:
                value = '""'
            update_envvar_list(my_export_vars, '='.join((var, value)))
        conf_export_vars = mconf.get('export_vars', False)
        if conf_export_vars:
            for evar in conf_export_vars:
                update_envvar_list(my_export_vars, evar)

        my_simple_vars = []
        if my_export_vars:
            for var in my_export_vars:
                if '=' in var:
                    vname, vvalue = var.split('=', 1)
                    # Check if there is a comma or space in the env-var value, if so add it to my_complex_vars
                    if any(x in vvalue for x in [',', ' ']):
                        if (
                                (vvalue.startswith('"') and vvalue.endswith('"'))
                                or (vvalue.startswith("'") and vvalue.endswith("'"))):
                            extra_lines.append('export {0}={1}'.format(vname, vvalue))
                        else:
                            extra_lines.append('export {0}="{1}"'.format(vname, vvalue))
                        use_jobscript = True
                    else:
                        my_simple_vars.append(var)
                else:
                    my_simple_vars.append(var)

        command_args.append(['-v', ','.join(my_simple_vars)])

        binding = mconf['affinity_type']

        if coprocessor is not None:
            # Setup the coprocessor
            cpconf = coprocessor_config(coprocessor)
            if cpconf.get('set_visible', False):
                extra_lines.extend([
                    'if [ -n "$SGE_HGR_gpu" ]',
                    'then',
                    '  if [ -z "$CUDA_VISIBLE_DEVICES" ]',
                    '  then',
                    '     export CUDA_VISIBLE_DEVICES=${SGE_HGR_gpu// /,}',
                    '  fi',
                    '  if [ -z "$GPU_DEVICE_ORDINAL" ]',
                    '  then',
                    '     export GPU_DEVICE_ORDINAL=${SGE_HGR_gpu// /,}',
                    '  fi',
                    'fi'
                ])
            if cpconf['no_binding']:
                binding = None
            if cpconf['classes']:
                available_classes = cpconf['class_types']
                if coprocessor_class is None:
                    coprocessor_class = cpconf['default_class']
                if (coprocessor_class_strict
                        or not cpconf['include_more_capable']):
                    try:
                        copro_class = available_classes[
                            coprocessor_class][
                                'resource']
                    except KeyError:
                        raise BadSubmission("Unrecognised coprocessor class")
                else:
                    copro_capability = available_classes[
                        coprocessor_class]['capability']
                    base_list = [
                        a for a in cpconf['class_types'].keys() if
                        cpconf['class_types'][a]['capability']
                        >= copro_capability]
                    copro_class = '|'.join(
                        [
                            cpconf['class_types'][a]['resource'] for a in
                            sorted(
                                base_list,
                                key=lambda x:
                                cpconf['class_types'][x]['capability'])
                        ]
                    )

                command_args.append(
                    ['-l',
                     '='.join((cpconf['class_resource'], copro_class))]
                )
            command_args.append(
                ['-l',
                 '='.join((cpconf['resource'], str(coprocessor_multi)))]
            )

        if binding is not None:
            if mconf['affinity_control'] == 'threads':
                affinity_spec = ':'.join(
                    (mconf['affinity_type'], str(threads)))
            elif mconf['affinity_control'] == 'slots':
                affinity_spec = ':'.join(
                    (mconf['affinity_type'], 'slots'))
            else:
                raise BadConfiguration(
                    ("Unrecognised affinity_control setting "
                        + mconf['affinity_control']))
            command_args.append(['-binding', affinity_spec])

        if (mconf['job_priorities']
                and priority is not None):
            if 'min_priority' in mconf:
                priority = max(mconf['min_priority'], priority)
                priority = min(mconf['max_priority'], priority)
            command_args.append(['-p', str(priority), ])

        if resources and _valid_resources(resources):
            command_args.append(
                ['-l', ','.join(resources), ])
            resources = _resource_dict(resources)

        if extra_args is not None:
            command_args.extend(extra_args)

        if logdir is not None:
            command_args.append(['-o', logdir, ])
            command_args.append(['-e', logdir, ])

        hold_state = '-hold_jid'
        # But have I not specified that array_task is not set for array
        # aware tasks
        if array_task and array_hold is not None:
            if mconf['array_holds']:
                jobhold = array_hold
                hold_state = '-hold_jid_ad'
            else:
                jobhold = array_hold

        if jobhold:
            if isinstance(jobhold, (list, tuple)):
                parents = ','.join([str(a) for a in jobhold])
            elif isinstance(jobhold, str):
                parents = jobhold
            elif isinstance(jobhold, int):
                parents = str(jobhold)
            else:
                raise BadSubmission(
                    "jobhold is of unsupported type " + str(type(jobhold)))
            command_args.append([hold_state, parents])

        if array_task is not None:
            if mconf['array_limit'] and array_limit:
                command_args.append(
                    ['-tc', str(array_limit), ]
                )

        if jobram:
            ram_units = fsl_sub.consts.RAMUNITS
            if ramsplit:
                jobram = split_ram_by_slots(jobram, threads)
            if mconf['notify_ram_usage']:
                # If a ram_resource has been specified for the job don't change
                ram_resources = sorted(
                    _filter_on_resource_dict(
                        mconf['ram_resources'],
                        resources))
                if ram_resources:
                    command_args.append(
                        ['-l', ','.join(
                            ['{0}={1}{2}'.format(
                                a, jobram, ram_units) for
                                a in ram_resources])]
                    )
        try:
            no_set_tlimit = (os.environ['FSLSUB_NOTIMELIMIT'] == '1' or affirmative(os.environ['FSLSUB_NOTIMELIMIT']))
        except Exception:
            no_set_tlimit = False
        if jobtime:
            if mconf['set_time_limit'] and not no_set_tlimit:
                command_args.append(['-l', 'h_rt=' + str(_minutes_to_seconds(jobtime)), ])
        if not no_set_tlimit:
            if mconf['set_hard_time'] and not (jobtime and mconf['set_time_limit']):
                max_qtime = _get_queue_time(queues)
                if max_qtime is not None:
                    command_args.append(
                        [
                            '-l',
                            'h_rt=' + str(_minutes_to_seconds(max_qtime)),
                        ]
                    )

        if mconf['mail_support']:
            if mailto:
                command_args.append(['-M', mailto, ])
                if not mail_on:
                    mail_on = mconf['mail_mode']
                if mail_on not in mconf['mail_modes']:
                    raise BadSubmission("Unrecognised mail mode")
                command_args.append(
                    [
                        '-m',
                        ','.join(mconf['mail_modes'][mail_on])
                    ])

        command_args.append(['-N', job_name, ])
        command_args.append('-cwd')
        command_args.append(['-q', ','.join(queues), ])

        if requeueable:
            command_args.append(
                ['-r', 'y', ]
            )
        if project is not None:
            command_args.append(
                ['-P', project, ]
            )
        if array_task:
            # Submit array task file
            if array_specifier:
                (
                    array_start,
                    array_end,
                    array_stride
                ) = parse_array_specifier(array_specifier)
                if not array_start:
                    raise BadSubmission("array_specifier doesn't make sense")
                array_spec = "{0}". format(array_start)
                if array_end:
                    array_spec += "-{0}".format(array_end)
                if array_stride:
                    array_spec += ":{0}".format(array_stride)
                command_args.append(['-t', array_spec])
            else:
                with open(command[0], 'r') as cmd_f:
                    array_slots = len(cmd_f.readlines())
                command_args.append(
                    ['-t', "1-{0}".format(
                        array_slots)])

    logger.info("sge_args: " + " ".join(
        [str(a) for a in command_args]))

    bash = bash_cmd()

    # Notify user

    if array_task and not array_specifier:
        logger.info("executing array task")
    else:
        if usescript:
            logger.info("executing cluster script")
        else:
            if array_specifier:
                logger.info("excuting array task {0}-{1}:{2}".format(
                    array_start,
                    array_end,
                    array_stride
                ))
            else:
                logger.info("executing single task")

    logger.info(" ".join([str(a) for a in command_args]))
    logger.debug(command_args)

    if array_task and not array_specifier:
        extra_lines.insert(0, '#$ -S ' + bash)
        extra_lines.extend([
            '',
            'the_command=$(sed -n -e "${{SGE_TASK_ID}}p" {0})'.format(command[0]),
            '',
        ])
        command = ['exec', bash, '-c', '"$the_command"', ]
        command_args = command_args if use_jobscript else []
        use_jobscript = True

    if use_jobscript:
        modules_paths = mconf.get('add_module_paths', None)

        if mconf.get('preserve_modules', True):
            if not mconf.get('copy_environment', False):
                modules = loaded_modules()
                logger.debug("Found following loaded modules")
                logger.debug(str(modules))
            else:
                warnings.warn(
                    "'preserve_modules' and 'copy_environment' settings are mutually "
                    "exclusive - not reloading modules")

        if mconf.get('copy_environment', False):
            if coprocessor_toolkit:
                cp_module = coproc_get_module(coprocessor, coprocessor_toolkit)
                if (cp_module is not None and cp_module not in loaded_modules()):
                    try:
                        modules.append(cp_module)
                    except NameError:
                        modules = [cp_module]

        js_lines = job_script(
            command, command_args,
            '#$', (METHOD_NAME, plugin_version()),
            modules=modules, extra_lines=extra_lines, modules_paths=modules_paths)
        logger.debug('\n'.join(js_lines))
        wrapper_name = write_wrapper(js_lines)
        logger.debug(wrapper_name)
        command_args = [wrapper_name]
        # Assume all queues in the list have the same start mode
        smode = _start_mode(pure_queues[0])
        if smode == 'posix_compliant' or smode == 'script_from_stdin':
            command_args.extend(['-S', bash])

        logger.debug("Calling fix_permissions " + str(0o755))
        fix_permissions(wrapper_name, 0o755)
    else:
        command_args = flatten_list(command_args)
        # Maintain behaviour with previous version
        if not usescript:
            command_args.extend(
                ['-shell', 'n', '-b', 'y', ]
            )
        command_args.extend(command)

    command_args.insert(0, qsub)

    result = sp.run(
        command_args, universal_newlines=True,
        stdout=sp.PIPE, stderr=sp.PIPE)
    if result.returncode != 0:
        if use_jobscript:
            try:
                os.remove(wrapper_name)
            except Exception:
                pass
        raise BadSubmission(result.stderr)

    # Search for a line of the form "Your job <id> has been submitted"
    try:
        job_id = None
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if line.startswith("Your job") and line.endswith("has been submitted"):
                line   = line.split(' ')
                job_id = int(line[2].split('.')[0])
                break
        if job_id is None:
            raise ValueError('Job ID not found')
    except ValueError:
        raise GridOutputError("Grid output was " + result.stdout)

    if use_jobscript:
        if keep_jobscript:
            logger.debug("Requested preservation of job script")
            new_name = os.path.join(
                os.getcwd(),
                '_'.join(('wrapper', str(job_id))) + '.sh'
            )
            try:
                logger.debug("Renaming wrapper to " + new_name)
                shutil.copy(
                    wrapper_name,
                    new_name
                )
            except OSError as e:
                warnings.warn("Unable to preserve wrapper script:" + str(e))
        try:
            os.remove(wrapper_name)
        except OSError as e:
            warnings.warn("Unable to remove wrapper temporary file" + str(e))
    return job_id


def _default_config_file():
    return os.path.join(
        os.path.realpath(os.path.dirname(__file__)),
        'fsl_sub_sge.yml')


def default_conf():
    '''Returns a string containing the default configuration for this
    cluster plugin.'''

    try:
        with open(_default_config_file()) as d_conf_f:
            d_conf = d_conf_f.read()
    except FileNotFoundError as e:
        raise MissingConfiguration("Unable to find default configuration file: " + str(e))
    return d_conf


def job_status(job_id, sub_job_id=None):
    '''Return details for the job with given ID.

    details holds a dict with following info:
        id
        name
        sub_time
        tasks (dict keyed on sub-task ID):
            status:
                fsl_sub.consts.QUEUED
                fsl_sub.consts.RUNNING
                fsl_sub.consts.FINISHED
                fsl_sub.consts.FAILED
                fsl_sub.consts.HELD
            start_time
            end_time
        '''

    # Look for running jobs
    if isinstance(job_id, str):
        if '.' in job_id:
            if sub_job_id is None:
                job_id, sub_job_id = job_id.split('.')
                sub_job_id = int(sub_job_id)
            else:
                job_id, _ = job_id.split('.')
        job_id = int(job_id)
    if isinstance(sub_job_id, str):
        sub_job_id = int(sub_job_id)

    try:
        running_job_details = _qstat_job(job_id, sub_job_id=sub_job_id)
        completed_job_details = _qacct_job(job_id, sub_job_id=sub_job_id)
        if running_job_details is None and completed_job_details is None:
            raise UnknownJobId("Job {0} not found".format(job_id))
        elif running_job_details is None:
            job_details = completed_job_details
        elif completed_job_details is None:
            job_details = running_job_details
        else:
            job_details = fsl_sub.utils.merge_dict(completed_job_details, running_job_details)

    except UnknownJobId:
        raise
    except Exception as e:
        raise GridOutputError from e

    return job_details


def _qacct_job(job_id, sub_job_id=None):
    job_details = {}
    task_id = 1
    sub_task = False
    if sub_job_id is not None:
        sub_task = True
        task_id = sub_job_id

    try:
        job_info = _qacct_job_lines(job_id)
    except UnknownJobId:
        return None
    raw_task_blocks = {}
    block_id = -1
    for line in job_info:
        if line == '':
            continue
        if line.startswith('============'):
            # new task block
            block_id += 1
            raw_task_blocks[block_id] = {}
            continue
        line = ' '.join(line.strip().split())
        (key, value) = line.split(' ', maxsplit=1)
        raw_task_blocks[block_id][key] = value

    tasks = {}
    for tb in raw_task_blocks.values():
        tasks[tb['taskid']] = tb

    sample_task = tasks[list(tasks.keys())[0]]
    job_details['id'] = int(sample_task['jobnumber'])
    job_details[
        'sub_time'] = _qacct_timestamp(sample_task['qsub_time'])
    job_details['name'] = sample_task['jobname']

    if sub_task:
        sub_tasks = [t for t in tasks.values() if t['taskid'] == task_id]
        if not sub_tasks:
            raise UnknownJobId(task_id)
    else:
        sub_tasks = list(tasks.values())
    job_details['tasks'] = {}
    for details in sub_tasks:
        try:
            taskid = int(details['taskid'])
        except ValueError:
            taskid = 1
        job_details['tasks'][taskid] = {}
        td = job_details['tasks'][taskid]
        td['status'] = fsl_sub.consts.FINISHED
        if int(details['exit_status']) != 0:
            td['status'] = fsl_sub.consts.FAILED
        td['end_time'] = _qacct_timestamp(details['end_time'])
        td['start_time'] = _qacct_timestamp(details['start_time'])
    return job_details


def _qacct_timestamp(output):
    try:
        timestamp = datetime.datetime.strptime(output, '%a %b %d %H:%M:%S %Y')
    except ValueError:
        try:
            timestamp = datetime.datetime.strptime(output, '%m/%d/%Y %H:%M:%S.%f')
        except ValueError:
            raise GridOutputError("Can't understand time stamp - " + output)
    return timestamp


def _qacct_job_lines(job_id):
    qacct = qacct_cmd()

    try:
        job_info = sp.run(
            [qacct, '-j', str(job_id)],
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            check=True, universal_newlines=True)
        return job_info.stdout.split('\n')
    except FileNotFoundError:
        raise BadSubmission(
            "Grid Engine software may not be correctly installed")
    except sp.CalledProcessError as e:
        if "job id {} not found".format(job_id) in e.stderr:
            raise UnknownJobId(job_id)
        else:
            raise GridOutputError(e.stderr)


def _qstat_timestamp(ts):
    try:
        timestamp = datetime.datetime.fromtimestamp(ts)
    except ValueError:
        try:
            # Univa is in microseconds
            timestamp = datetime.datetime.fromtimestamp(ts / 1000.0)
        except ValueError:
            raise GridOutputError("Can't understand time stamp - " + ts)
    return timestamp


def _qstat_job(job_id, sub_job_id=None):
    job_details = {}
    task_id = 1
    sub_task = False
    if sub_job_id is not None:
        sub_task = True
        task_id = sub_job_id
    try:
        text_xml = _qstat_job_xml(job_id)
        if 'http://www.univa.com' in text_xml:
            task_grouper = "element"
        else:
            task_grouper = "ulong_sublist"
        xml = ET.fromstring(text_xml)
        djob_info = xml.find('djob_info')
        if djob_info is None:
            return None
        jobd = djob_info.find('element')
        jF = jobd.find
        job_details['id'] = int(jF('JB_job_number').text)
        job_details[
            'sub_time'] = _qstat_timestamp(
                int(jF('JB_submission_time').text))
        job_details['name'] = jF('JB_job_name').text
        predecessors = jF('JB_jid_predecessor_list')
        job_tasks = jF('JB_ja_tasks')
        job_details['tasks'] = {}
        if job_tasks:
            # job is running or in Eqw
            sub_tasks = {}
            for task in job_tasks.iter(task_grouper):
                # Problem is that JB_ja_tasks contains a nested ulong_sublist!
                task_number_object = task.find('JAT_task_number')
                if task_number_object is not None:
                    # We are in a top-level JB_ja_tasks element
                    task_number = int(task_number_object.text)
                    try:
                        task_entry = {
                            'start_time': _qstat_timestamp(
                                int(task.find('JAT_start_time').text)),
                            'end_time': None,
                        }
                    except Exception:
                        task_entry = {
                            'start_time': None,
                            'end_time': None
                        }
                    err_mess = task.find('JAT_message_list')
                    if err_mess:
                        task_entry['status'] = (
                            fsl_sub.consts.FAILEDNQUEUED)
                    else:
                        task_entry['status'] = (
                            fsl_sub.consts.RUNNING)
                    sub_tasks[task_number] = task_entry
            if sub_task:
                job_details['tasks'] = {'1': sub_tasks[task_id], }
            else:
                job_details['tasks'] = sub_tasks
        else:
            # Job is pending
            job_details['tasks'][1] = {
                'start_time': None,
                'end_time': None,
            }

            if predecessors:
                job_details['tasks'][1]['status'] = fsl_sub.consts.HELD
            else:
                job_details['tasks'][1]['status'] = fsl_sub.consts.QUEUED

    except Exception:
        raise GridOutputError("Unable to understand XML output")

    return job_details


def _get_scaled_value(xml_obj, name):
    for a in xml_obj.iter('scaled'):
        if a.find('UA_name').text == name:
            return a.find('UA_value').text


def _qstat_job_xml(job_id):
    qstat = qstat_cmd()
    output = None
    try:
        qstat_xml = sp.run(
            [qstat, '-j', str(job_id), '-xml'],
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            check=True, universal_newlines=True)
        output = qstat_xml.stdout
    except FileNotFoundError:
        raise BadSubmission(
            "Grid Engine software may not be correctly installed")
    except sp.CalledProcessError as e:
        raise GridOutputError(e.stderr)
    return output


def project_list():
    '''This returns a list of recognised projects (or accounts) that a job
    can be allocated to (e.g. for billing or fair share allocation)'''
    qconf = qconf_cmd()
    try:
        qconf_out = sp.run(
            [qconf, '-sprjl'],
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            check=True, universal_newlines=True
        )
    except FileNotFoundError:
        raise BadSubmission(
            "Grid Engine software may not be correctly installed")
    except sp.CalledProcessError as e:
        raise GridOutputError(e.stderr)
    return qconf_out.stdout.split()


def _get_queues(qtest=None):
    '''Return list of queue names'''
    if qtest is None:
        qtest = qconf_cmd()
    try:
        result = sp.run(
            [qtest, '-sql', ],
            stdout=sp.PIPE,
            stderr=sp.DEVNULL,
            check=True, universal_newlines=True)
    except (FileNotFoundError, sp.CalledProcessError, ):
        raise BadSubmission(
            "Grid Engine software may not be correctly installed")

    return result.stdout.splitlines()


def _get_queue_info(queue, qtest=None):
    '''Return dictionary of queue info'''
    if qtest is None:
        qtest = qconf_cmd()
    try:
        result = sp.run(
            [qtest, '-sq', queue],
            stdout=sp.PIPE,
            stderr=sp.DEVNULL,
            check=True, universal_newlines=True)
    except FileNotFoundError:
        raise BadSubmission(
            "Grid Engine software may not be correctly installed")
    except sp.CalledProcessError:
        raise BadSubmission(
            "Queue {0} not found!".format(queue))

    output = result.stdout
    conf_lines = output.replace(' \\\n', '').splitlines()
    return {a.split(maxsplit=1)[0]: a.split(maxsplit=1)[1] for a in conf_lines}


def _process_q_hl(hlist):
    hl = []
    for h_descriptor in hlist.split(','):
        if '=' in h_descriptor:
            hl.append(h_descriptor.split('=')[1].strip(']'))
        else:
            hl.append(h_descriptor)
    return hl


def _process_pe_hl(hlist):
    hl = []
    for h_descriptor in hlist.split(','):
        if '=' in h_descriptor:
            hl.extend(h_descriptor.split('=')[1].strip(']').split(' '))
        else:
            hl.extend(h_descriptor.split(' '))
    return hl


def _get_queue_ram_map(qtest=None):
    '''Return dict of queue: (max_ram, multiple_classes)'''
    ram_units = fsl_sub.consts.RAMUNITS
    if qtest is None:
        qtest = qhost_cmd()
    try:
        result = sp.run(
            [qtest, '-q', '-xml', ],
            stdout=sp.PIPE,
            stderr=sp.DEVNULL,
            check=True, universal_newlines=True)
    except (FileNotFoundError, sp.CalledProcessError, ):
        raise BadSubmission(
            "Grid Engine software may not be correctly installed")

    output = result.stdout
    xml = ET.fromstring(output)
    host_list = []
    for host in xml.iter('host'):
        hostname = host.attrib['name']
        if hostname == 'global':
            continue
        mem_total = human_to_ram(
            host.find("hostvalue[@name='mem_total']").text, output=ram_units)
        queue_dict = {}
        for q in host.iter('queue'):
            q_name = q.attrib['name']
            queue_dict[q_name] = int(q.find("queuevalue[@name='slots']").text)
        host_list.append(
            {
                'name': hostname,
                'mem': mem_total,
                'queue_slots': queue_dict,
            }
        )
        queues = {}
        for h in host_list:
            for q in h['queue_slots'].keys():
                if q not in queues.keys():
                    queues[q] = [h['mem'], False, -1, False]
                elif h['mem'] > queues[q][0]:
                    queues[q][0] = h['mem']
                    queues[q][1] = True
                elif h['mem'] != queues[q][0]:
                    queues[q][1] = True
                if queues[q][2] != -1:
                    queues[q][2] = max(h['queue_slots'][q], queues[q][2])
                    queues[q][3] = True
                else:
                    queues[q][2] = h['queue_slots'][q]

    return queues


def _to_minutes(time_str):
    '''Convert HH:MM:SS to minutes (drops seconds)'''

    times = time_str.split(':')
    return int(times[0]) * 60 + int(times[1])


def _minutes_to_seconds(minutes):
    '''Convert minutes seconds'''

    return minutes * 60


def provides_coproc_config():
    return False


def _add_comment(comments, comment):
    if comment not in comments:
        comments.append(comment)


def build_queue_defs():
    '''Return YAML suitable for configuring queues'''
    logger = _get_logger()

    ram_units = fsl_sub.consts.RAMUNITS
    try:
        queue_list = _get_queues()
        queue_ram_map = _get_queue_ram_map()
    except BadSubmission as e:
        logger.error('Unable to query Grid Engine: ' + str(e))
        return ('', [])
    q_base = CommentedMap()
    q_base['queues'] = CommentedMap()
    queues = q_base['queues']
    for q in queue_list:
        qinfo = _get_queue_info(q)
        if 'BATCH' not in qinfo['qtype']:
            continue
        queues[qinfo['qname']] = CommentedMap()
        qd = queues[qinfo['qname']]
        queues.yaml_add_eol_comment("Queue name", qinfo['qname'], column=0)
        add_key_comment = qd.yaml_add_eol_comment
        comments = []
        for coproc_m in ('gpu', 'cuda', 'phi', ):
            if coproc_m in q:
                _add_comment(
                    comments,
                    "Quene name looks like it might be a queue supporting co-processors."
                    " Cannot auto-configure."
                )
        for limit in ('h_rt', 'h_cpu'):
            if qinfo[limit] == 'INFINITY':
                qinfo[limit] = '10000:00:00'

        qd['time'] = min(
            [1000000, _to_minutes(qinfo['h_rt']), _to_minutes(qinfo['h_cpu'])])
        add_key_comment('Maximum job run time in minutes', 'time', column=0)
        if qinfo['pe_list'] != 'NONE':
            qd['parallel_envs'] = sorted(list(set(_process_pe_hl(qinfo['pe_list']))))
            add_key_comment('Parallel environments configured on this queue', 'parallel_envs', column=0)
            try:
                qd['parallel_envs'].remove('NONE')
            except ValueError:
                pass
        if ',' not in qinfo['slots']:
            qd['max_slots'] = int(qinfo['slots'])
        else:
            qd['max_slots'] = max([int(a) for a in _process_q_hl(qinfo['slots'])])
        add_key_comment("Maximum number of threads/slots on a queue", 'max_slots', column=0)
        try:
            qd['max_size'] = int(queue_ram_map[q][0])
            add_key_comment("Maximum RAM size of a job", 'max_size', column=0)
            if queue_ram_map[q][1]:
                _add_comment(
                    comments,
                    "Queue has hosts of different total memory size, consider creating multiple queues"
                    " for the different host hardware in Grid Engine and then set the same 'group' integer"
                    " to allow fsl_sub to maximise hardware your job can run on. Alternatively consider turning"
                    " on notify_ram_usage."
                )
        except KeyError:
            logger.error("Queue {0} is not defined on any hosts and is not usable".format(q))
            del queues[q]
            continue

        q_vmem = _process_q_hl(qinfo['h_vmem'])
        q_rss = _process_q_hl(qinfo['h_rss'])
        try:
            q_vmem.remove('INFINITY')
            q_rss.remove('INFINITY')
        except ValueError:
            pass

        unique_vmem = list(set(q_vmem))
        if len(unique_vmem) > 0:
            _add_comment(
                comments,
                "Queue has hosts of different per-slot memory size, consider creating multiple"
                " queues for the different host hardware in Grid Engine and then add these queues "
                " to the configuration setting the same 'group' integer in the configuration to "
                " allow fsl_sub to maximise hardware your job can run on."
            )
            qd['slot_size'] = max([human_to_ram(a, output=ram_units) for a in unique_vmem])
        elif len(unique_vmem) == 1:
            qd['slot_size'] = human_to_ram(unique_vmem[0], output=ram_units)
        else:
            unique_rss = list(set(q_rss))
            if len(unique_rss) > 0:
                if not comments:
                    _add_comment(
                        comments,
                        "Queue has hosts of different per-slot memory size, consider creating multiple"
                        " queues for the different host hardware in Grid Engine and then add these queues "
                        " to the configuration setting the same 'group' integer in the configuration to "
                        " allow fsl_sub to maximise hardware your job can run on."
                    )
                qd['slot_size'] = max([human_to_ram(a, output=ram_units) for a in unique_rss])
            elif len(unique_rss) == 1:
                qd['slot_size'] = human_to_ram(unique_rss[0], output=ram_units)
            else:
                qd['slot_size'] = int(qd['max_size']) // queue_ram_map[q][2]
                _add_comment(
                    comments,
                    "Queue has no h_vmem or h_rss specified, "
                    "slot_size calculated with max_size divided by slots.")
                if queue_ram_map[q][3]:
                    _add_comment(
                        comments,
                        "Queue has multiple slot sizes "
                        "- this calculation will not be correct for all hosts."
                    )
        add_key_comment("Maximum memory per thread", 'slot_size')
        qd['map_ram'] = method_config(METHOD_NAME)['map_ram']
        add_key_comment(
            'Whether this queue should automatically split jobs into'
            ' multiple threads to support RAM request',
            'map_ram')
        _add_comment(comments, "default: true # Is this the default partition?")
        _add_comment(comments, 'priority: 1 # Priority in group - higher wins')
        _add_comment(comments, 'group: 1 # Group partitions with the same integer then order by priority')
        _add_comment(comments, 'For co-processor queues you need the following:')
        _add_comment(comments, 'copros:')
        _add_comment(comments, '  cuda: # CUDA Co-processor available')
        _add_comment(comments, '    max_quantity: # Maximum available per node')
        _add_comment(comments, '    classes: # List of classes (if classes supported)')
        _add_comment(comments, '    exclusive: False # Does this only run jobs requiring this co-processor?')

        for w in comments:
            queues.yaml_set_comment_before_after_key(qinfo['qname'], after=w)

    return q_base
