#!/usr/bin/env python
import copy
import datetime
import io
import os
import subprocess
import tempfile
import unittest
import fsl_sub_plugin_sge

from ruamel.yaml import YAML
from unittest.mock import (patch, mock_open, )

conf_dict = YAML(typ='safe').load('''---
method_opts:
    sge:
        large_job_split_pe: shmem
        affinity_type: linear
        affinity_control: threads
        mail_support: True
        mail_modes:
            b:
                - b
            e:
                - e
            a:
                - a
            f:
                - a
                - e
                - b
            n:
                - n
        mail_mode: a
        map_ram: True
        notify_ram_usage: True
        set_time_limit: False
        set_hard_time: False
        ram_resources:
            - m_mem_free
            - h_vmem
        job_priorities: True
        min_priority: -1023
        max_priority: 0
        array_holds: True
        array_limit: True
        architecture: False
        job_resources: True
        projects: True
        use_jobscript: False
        keep_jobscript: False
        preserve_modules: False
        export_vars: []
        copy_environment: True
        allow_nested_queuing: False
copro_opts:
    cuda:
        resource: gpu
        classes: True
        class_resource: gputype
        class_types:
            K:
                resource: k80
                doc: Kepler. ECC, double- or single-precision workloads
                capability: 2
            P:
                resource: p100
                doc: >
                    Pascal. ECC, double-, single- and half-precision
                    workloads
                capability: 3
        default_class: K
        include_more_capable: True
        uses_modules: False
        module_parent: cuda
        no_binding: True
''')
mconf_dict = conf_dict['method_opts']['sge']


@patch('fsl_sub_plugin_sge.fsl_sub.config.read_config', autospec=True)
class TestQueueProperties(unittest.TestCase):
    def test__get_qeueue_time(self, mock_qconfig):
        mock_qconfig.return_value = {
            'queues': {
                'myq': {
                    'time': 1000,
                }
            }
        }
        with self.subTest("Plain queue"):
            self.assertEqual(
                fsl_sub_plugin_sge._get_queue_time('myq'),
                1000
            )
        with self.subTest("Queue + host"):
            self.assertEqual(
                fsl_sub_plugin_sge._get_queue_time('myq@myhost'),
                1000
            )
        with self.subTest('Queue + hostgroup'):
            self.assertEqual(
                fsl_sub_plugin_sge._get_queue_time('myq@@hostgroup'),
                1000
            )
        mock_qconfig.return_value = {
            'queues': {
                'myq@@hostgroup': {
                    'time': 1000,
                }
            }
        }
        with self.subTest("Hostgroup queue"):
            self.assertEqual(
                fsl_sub_plugin_sge._get_queue_time('myq'),
                1000
            )
        with self.subTest("Hostgroup queue with queue + host"):
            self.assertEqual(
                fsl_sub_plugin_sge._get_queue_time('myq@myhost'),
                1000
            )
        with self.subTest("Hostgroup queue with queue + hostgroup"):
            self.assertEqual(
                fsl_sub_plugin_sge._get_queue_time('myq@@hostgroup'),
                1000
            )


class TestSgeUtils(unittest.TestCase):
    @patch(
        'fsl_sub_plugin_sge.method_config',
        return_value=conf_dict['method_opts']['sge'])
    def test_already_queued(self, mock_mc):

        with patch.dict(os.environ, {'JOB_ID': '1234'}, clear=True):
            self.assertTrue(fsl_sub_plugin_sge.already_queued())

        with patch.dict(os.environ, {
                "FSLSUB_NESTED": "1",
                "JOB_ID": "1234"}, clear=True):
            self.assertFalse(fsl_sub_plugin_sge.already_queued())
        test_cd = copy.deepcopy(conf_dict['method_opts']['sge'])
        test_cd['allow_nested_queuing'] = True
        mock_mc.return_value = test_cd
        with patch.dict(os.environ, {"JOB_ID": "1234"}, clear=True):
            self.assertFalse(fsl_sub_plugin_sge.already_queued())

    def test__qacct_timestamp(self):
        with self.subTest("Univa"):
            dobj = datetime.datetime(2020, 11, 19, 12, 46, 42, 441000)
            self.assertEqual(
                dobj,
                fsl_sub_plugin_sge._qacct_timestamp("11/19/2020 12:46:42.441")
            )
        with self.subTest('SGE'):
            dobj = datetime.datetime(2020, 11, 19, 12, 46, 42)
            self.assertEqual(
                dobj,
                fsl_sub_plugin_sge._qacct_timestamp("Thu Nov 19 12:46:42 2020")
            )

    def test__valid_resources(self):
        with self.subTest("Good"):
            self.assertTrue(
                fsl_sub_plugin_sge._valid_resources(
                    ['a=b', 'c=d', 'e=f', ]))
        with self.subTest('Bad'):
            self.assertTrue(
                fsl_sub_plugin_sge._valid_resources(
                    ['a=b', 'cd', 'e=f', ]))

    def test__resource_dict(self):
        self.assertDictEqual(
            {
                'a': 'b',
                'c': 'd',
                'e': 'f', },
            fsl_sub_plugin_sge._resource_dict(['a=b', 'c=d', 'e=f'])
        )

    def test__filter_on_resource_dict(self):
        with self.subTest("No dict"):
            self.assertListEqual(
                fsl_sub_plugin_sge._filter_on_resource_dict(
                    ['a', 'b', ],
                    {}
                ),
                ['a', 'b', ]
            )
        with self.subTest("all matches"):
            self.assertListEqual(
                fsl_sub_plugin_sge._filter_on_resource_dict(
                    ['a', 'b', ],
                    {'a': 'c', 'b': 'd'}
                ),
                []
            )
        with self.subTest("one match"):
            self.assertListEqual(
                fsl_sub_plugin_sge._filter_on_resource_dict(
                    ['a', 'e', ],
                    {'a': 'c', 'b': 'd'}
                ),
                ['e']
            )
        with self.subTest("no match"):
            self.assertListEqual(
                fsl_sub_plugin_sge._filter_on_resource_dict(
                    ['g', ],
                    {'a': 'c', 'b': 'd'}
                ),
                ['g', ]
            )
        with self.subTest("no list"):
            self.assertListEqual(
                fsl_sub_plugin_sge._filter_on_resource_dict(
                    [],
                    {'a': 'c', 'b': 'd'}
                ),
                []
            )


class TestAlreadyQueued(unittest.TestCase):
    @patch.dict('fsl_sub_plugin_sge.os.environ', {'JOB_ID': '1'})
    def test_alreadyqueued(self):
        self.assertTrue(fsl_sub_plugin_sge.already_queued())

    @patch.dict('fsl_sub_plugin_sge.os.environ', clear=True)
    def test_notqueued(self):
        self.assertFalse(fsl_sub_plugin_sge.already_queued())


class TestSgeFinders(unittest.TestCase):
    @patch('fsl_sub_plugin_sge.qconf_cmd', autospec=True)
    def test_qtest(self, mock_qconf):
        bin_path = '/opt/sge/bin/qconf'
        mock_qconf.return_value = bin_path
        self.assertEqual(
            bin_path,
            fsl_sub_plugin_sge.qtest()
        )
        mock_qconf.assert_called_once_with()

    @patch('fsl_sub_plugin_sge.which', autospec=True)
    def test_qconf(self, mock_which):
        bin_path = '/opt/sge/bin/qconf'
        with self.subTest("Test 1"):
            mock_which.return_value = bin_path
            self.assertEqual(
                bin_path,
                fsl_sub_plugin_sge.qconf_cmd()
            )
        mock_which.reset_mock()
        with self.subTest("Test 2"):
            mock_which.return_value = None
            self.assertRaises(
                fsl_sub_plugin_sge.BadSubmission,
                fsl_sub_plugin_sge.qconf_cmd
            )

    @patch('fsl_sub_plugin_sge.which', autospec=True)
    def test_qstat(self, mock_which):
        bin_path = '/opt/sge/bin/qstat'
        with self.subTest("Test 1"):
            mock_which.return_value = bin_path
            self.assertEqual(
                bin_path,
                fsl_sub_plugin_sge.qstat_cmd()
            )
        mock_which.reset_mock()
        fsl_sub_plugin_sge.qstat_cmd.cache_clear()
        with self.subTest("Test 2"):
            mock_which.return_value = None
            self.assertRaises(
                fsl_sub_plugin_sge.BadSubmission,
                fsl_sub_plugin_sge.qstat_cmd
            )

    @patch('fsl_sub_plugin_sge.which', autospec=True)
    def test_qsub(self, mock_which):
        bin_path = '/opt/sge/bin/qsub'
        with self.subTest("Test 1"):
            mock_which.return_value = bin_path
            self.assertEqual(
                bin_path,
                fsl_sub_plugin_sge.qsub_cmd()
            )
        mock_which.reset_mock()
        with self.subTest("Test 2"):
            mock_which.return_value = None
            self.assertRaises(
                fsl_sub_plugin_sge.BadSubmission,
                fsl_sub_plugin_sge.qsub_cmd
            )

    @patch('fsl_sub_plugin_sge.qconf_cmd', autospec=True)
    @patch('fsl_sub_plugin_sge.sp.run', autospec=True)
    def test_queue_exists(self, mock_spr, mock_qconf):
        bin_path = '/opt/sge/bin/qtest'
        qname = 'myq'
        with self.subTest("Test 1"):
            mock_qconf.return_value = bin_path
            mock_spr.return_value = subprocess.CompletedProcess(
                [bin_path, '-sq', qname],
                returncode=0
            )
            self.assertTrue(
                fsl_sub_plugin_sge.queue_exists(qname)
            )
            mock_qconf.assert_called_once_with()
            mock_spr.assert_called_once_with(
                [bin_path, '-sq', qname],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                check=True,
                universal_newlines=True)
        mock_spr.reset_mock()
        mock_qconf.reset_mock()
        with self.subTest("Hostname in queue"):
            target_q = 'myq@myhost'
            mock_qconf.return_value = bin_path
            mock_spr.return_value = subprocess.CompletedProcess(
                [bin_path, '-sq', qname],
                returncode=0
            )
            self.assertTrue(
                fsl_sub_plugin_sge.queue_exists(target_q)
            )
            mock_qconf.assert_called_once_with()
            mock_spr.assert_called_once_with(
                [bin_path, '-sq', qname],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                check=True,
                universal_newlines=True)
        mock_qconf.reset_mock()
        mock_spr.reset_mock()
        with self.subTest("Comma separated queues"):
            target_q = 'myq,myotherq'
            mock_qconf.return_value = bin_path
            mock_spr.side_effect = [
                subprocess.CompletedProcess(
                    [bin_path, '-sq', qname],
                    returncode=0
                ),
                subprocess.CompletedProcess(
                    [bin_path, '-sq', 'myotherq'],
                    returncode=0
                )
            ]
            self.assertTrue(
                fsl_sub_plugin_sge.queue_exists(target_q)
            )
            mock_qconf.assert_called_once_with()
            mock_spr.assert_called_once_with(
                [bin_path, '-sq', target_q],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                check=True,
                universal_newlines=True)
        mock_qconf.reset_mock()
        mock_spr.reset_mock()
        with self.subTest("No queue"):
            mock_spr.side_effect = subprocess.CalledProcessError(
                returncode=1, cmd=bin_path)
            self.assertFalse(
                fsl_sub_plugin_sge.queue_exists(qname, bin_path)
            )
        mock_qconf.reset_mock()
        with self.subTest("Grid software not found"):
            mock_qconf.side_effect = fsl_sub_plugin_sge.BadSubmission(
                "Bad")
            self.assertRaises(
                fsl_sub_plugin_sge.BadSubmission,
                fsl_sub_plugin_sge.queue_exists,
                qname
            )


@patch(
    'fsl_sub_plugin_sge.qconf_cmd',
    autospec=True, return_value="/usr/bin/qconf")
@patch(
    'fsl_sub_plugin_sge.qstat_cmd',
    autospec=True, return_value="/usr/bin/qstat")
@patch('fsl_sub_plugin_sge.sp.run', autospec=True)
class TestCheckPE(unittest.TestCase):
    def test_queue_name(self, mock_spr, mock_qstat, mock_qconf):
        mock_spr.return_value = subprocess.CompletedProcess('a', 1)
        self.assertRaises(
            fsl_sub_plugin_sge.BadSubmission,
            fsl_sub_plugin_sge._check_pe,
            "nope", "aqueue"
        )
        mock_spr.assert_called_once_with(
            ["/usr/bin/qconf", "-sp", "nope", ],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        mock_qstat.assert_called_once_with()
        mock_qconf.assert_called_once_with()

    def test_pe_available_anywhere(self, mock_spr, mock_qstat, mock_qconf):
        with self.subTest("SonOfGrid Engine"):
            mock_spr.side_effect = [
                subprocess.CompletedProcess('a', 0),
                subprocess.CompletedProcess('a', 1)
            ]
            self.assertRaises(
                fsl_sub_plugin_sge.BadSubmission,
                fsl_sub_plugin_sge._check_pe,
                "ape", "aqueue"
            )
        with self.subTest("Univa Grid Engine"):
            mock_spr.side_effect = [
                subprocess.CompletedProcess('a', 0),
                subprocess.CompletedProcess(
                    'a', 0,
                    stderr="error: no such parallel environment")
            ]
            self.assertRaises(
                fsl_sub_plugin_sge.BadSubmission,
                fsl_sub_plugin_sge._check_pe,
                "ape", "aqueue"
            )

    def test_pe_available(self, mock_spr, mock_qstat, mock_qconf):
        example_pe_xml = '''<?xml version='1.0'?>
<job_info  xmlns:xsd="http://a.web.server.com/qstat.xsd">
  <cluster_queue_summary>
    <name>a.q</name>
    <load>0.44016</load>
    <used>0</used>
    <resv>0</resv>
    <available>1</available>
    <total>1</total>
    <temp_disabled>0</temp_disabled>
    <manual_intervention>0</manual_intervention>
  </cluster_queue_summary>
</job_info>
'''
        mock_qstat.return_value = 'a'
        mock_qconf.return_value = 'a'
        mock_spr.side_effect = [
            subprocess.CompletedProcess('a', 0),
            subprocess.CompletedProcess(
                'a', 0,
                stdout=example_pe_xml),
        ]
        self.assertRaises(
            fsl_sub_plugin_sge.BadSubmission,
            fsl_sub_plugin_sge._check_pe,
            "ape", "b.q"
        )
        mock_spr.reset_mock()
        mock_spr.side_effect = [
            subprocess.CompletedProcess('a', 0),
            subprocess.CompletedProcess(
                'a', 0,
                stdout=example_pe_xml),
        ]
        self.assertRaises(
            fsl_sub_plugin_sge.BadSubmission,
            fsl_sub_plugin_sge._check_pe,
            "ape", "ba.q"
        )
        mock_spr.reset_mock()
        mock_spr.side_effect = [
            subprocess.CompletedProcess('a', 0),
            subprocess.CompletedProcess(
                'a', 0,
                stdout=example_pe_xml),
        ]
        self.assertRaises(
            fsl_sub_plugin_sge.BadSubmission,
            fsl_sub_plugin_sge._check_pe,
            "ape", "a.q1"
        )
        mock_spr.reset_mock()
        mock_spr.side_effect = [
            subprocess.CompletedProcess('a', 0),
            subprocess.CompletedProcess(
                'a', 0,
                stdout=example_pe_xml),
        ]
        fsl_sub_plugin_sge._check_pe("ape", "a.q")


@patch('fsl_sub.utils.VERSION', '1.0.0')
@patch('fsl_sub.utils.sys.argv', ['fsl_sub', '-q', 'short.q', './mycommand', 'arg1', 'arg2'])
@patch(
    'fsl_sub_plugin_sge._check_pe',
    autospec=True
)
@patch(
    'fsl_sub_plugin_sge.os.getcwd',
    autospec=True, return_value='/Users/testuser')
@patch('fsl_sub_plugin_sge.split_ram_by_slots', autospec=True)
@patch(
    'fsl_sub_plugin_sge.coprocessor_config', autospec=True)
@patch('fsl_sub_plugin_sge.sp.run', autospec=True)
@patch('fsl_sub_plugin_sge.os.remove', autospec=True)
class TestWrapperSubmit(unittest.TestCase):
    def setUp(self):
        self.ww = tempfile.NamedTemporaryFile(
            mode='w+t',
            delete=False)
        self.now = datetime.datetime.now()
        self.strftime = datetime.datetime.strftime
        self.bash = '/bin/bash'
        os.environ['FSLSUB_SHELL'] = self.bash
        self.qsub = '/usr/bin/qsub'
        self.config = copy.deepcopy(conf_dict)
        self.mconfig = self.config['method_opts']['sge']
        self.patch_objects = {
            'fsl_sub.utils.datetime': {'autospec': True, },
            'fsl_sub_plugin_sge.plugin_version': {'autospec': True, 'return_value': '2.0.0', },
            'fsl_sub_plugin_sge.loaded_modules': {'autospec': True, 'return_value': ['mymodule', ], },
            'fsl_sub_plugin_sge.bash_cmd': {'autospec': True, 'return_value': self.bash, },
            'fsl_sub_plugin_sge.write_wrapper': {'autospec': True, 'side_effect': self.w_wrapper},
            'fsl_sub_plugin_sge._start_mode': {'autospec': True, 'return_value': 'unix_behavior', },
            'fsl_sub_plugin_sge.method_config': {'return_value': self.mconfig, },
            'fsl_sub_plugin_sge.qsub_cmd': {'autospec': True, 'return_value': self.qsub, },
        }

        self.patch_dict_objects = {}
        self.patches = {}
        for p, kwargs in self.patch_objects.items():
            self.patches[p] = patch(p, **kwargs)
        self.mocks = {}
        for o, p in self.patches.items():
            self.mocks[o] = p.start()

        self.dict_patches = {}
        for p, kwargs in self.patch_dict_objects.items():
            self.dict_patches[p] = patch.dict(p, **kwargs)

        for o, p in self.dict_patches.items():
            self.mocks[o] = p.start()
        self.mocks['fsl_sub.utils.datetime'].datetime.now.return_value = self.now
        self.mocks['fsl_sub.utils.datetime'].datetime.strftime = self.strftime
        self.addCleanup(patch.stopall)
        self.wrap_head = [
            '#!' + self.bash,
            '',
            '#$ -v '
            'FSLSUB_JOBID_VAR=JOB_ID,'
            'FSLSUB_ARRAYTASKID_VAR=SGE_TASK_ID,'
            'FSLSUB_ARRAYSTARTID_VAR=SGE_TASK_FIRST,'
            'FSLSUB_ARRAYENDID_VAR=SGE_TASK_LAST,'
            'FSLSUB_ARRAYSTEPSIZE_VAR=SGE_TASK_STEPSIZE,'
            'FSLSUB_ARRAYCOUNT_VAR="",'
            'FSLSUB_NSLOTS=NSLOTS',
        ]
        self.doc = [
            '# Built by fsl_sub v.1.0.0 and fsl_sub_plugin_sge v.2.0.0',
            '# Command line: fsl_sub -q short.q ./mycommand arg1 arg2',
            '# Submission time (H:M:S DD/MM/YYYY): {0}'.format(self.now.strftime("%H:%M:%S %d/%m/%Y")),
            '',
        ]

    def tearDown(self):
        self.ww.close()
        os.unlink(self.ww.name)
        patch.stopall()

    plugin = fsl_sub_plugin_sge

    def w_wrapper(self, content):
        for line in content:
            self.ww.write(line + '\n')
        return self.ww.name

    def test_submit_wrapper(
        self, mock_osunl, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['mycommand', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        w_conf = copy.deepcopy(conf_dict)
        w_conf['method_opts']['sge']['use_jobscript'] = True
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = w_conf['method_opts']['sge']
        mock_cpconf.return_value = w_conf['copro_opts']['cuda']

        with self.subTest("No preserve"):
            expected_cmd = [
                self.qsub,
                self.ww.name
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            mock_osunl.assert_called_once_with(
                self.ww.name
            )
            self.ww.seek(0)
            wrapper_lines = self.ww.read().splitlines()
            self.maxDiff = None
            exp_wrap = list(self.wrap_head)
            exp_wrap.extend([
                '#$ -binding linear:1',
                '#$ -N ' + job_name,
                '#$ -cwd',
                '#$ -q ' + queue,
                '#$ -r y',
            ])
            exp_wrap.insert(2, '#$ -V')
            exp_wrap.extend(self.doc)
            exp_wrap.extend([' '.join(cmd), ''])
            self.assertListEqual(
                wrapper_lines,
                exp_wrap
            )
        mock_sprun.reset_mock()

    def test_submit_wrapper_with_extra_args(
        self, mock_osunl, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['mycommand', 'arg1', 'arg2', ]
        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        extra_args = ['--something=blah', '--nothing', '-z', ]
        w_conf = copy.deepcopy(conf_dict)
        w_conf['method_opts']['sge']['use_jobscript'] = True
        w_conf['method_opts']['sge']['copy_environment'] = False
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = w_conf['method_opts']['sge']
        mock_cpconf.return_value = w_conf['copro_opts']['cuda']

        expected_cmd = [
            self.qsub,
            self.ww.name
        ]
        mock_sprun.return_value = subprocess.CompletedProcess(
            expected_cmd, 0,
            stdout=qsub_out, stderr=None)
        self.assertEqual(
            jid,
            self.plugin.submit(
                command=cmd,
                job_name=job_name,
                queue=queue,
                extra_args=extra_args
            )
        )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        mock_osunl.assert_called_once_with(
            self.ww.name
        )
        self.ww.seek(0)
        wrapper_lines = self.ww.read().splitlines()
        self.maxDiff = None
        exp_wrap = list(self.wrap_head)
        exp_wrap.append('#$ -binding linear:1')
        exp_wrap.extend(['#$ ' + s for s in extra_args])
        exp_wrap.extend([
            '#$ -N ' + job_name,
            '#$ -cwd',
            '#$ -q ' + queue,
            '#$ -r y',
        ])
        exp_wrap.extend(self.doc)
        exp_wrap.extend([' '.join(cmd), ''])
        self.assertListEqual(
            wrapper_lines,
            exp_wrap
        )
        mock_sprun.reset_mock()

    def test_submit_wrapper_with_modules_path(
        self, mock_osunl, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['mycommand', 'arg1', 'arg2', ]
        mod_p = ['/usr/local/shellmodules', ]
        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        w_conf = copy.deepcopy(conf_dict)
        w_conf['method_opts']['sge']['use_jobscript'] = True
        w_conf['method_opts']['sge']['copy_environment'] = False
        w_conf['method_opts']['sge']['preserve_modules'] = True
        w_conf['method_opts']['sge']['add_module_paths'] = mod_p
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = w_conf['method_opts']['sge']
        mock_cpconf.return_value = w_conf['copro_opts']['cuda']

        with self.subTest("With extra module path of " + ':'.join(mod_p)):
            expected_cmd = [
                self.qsub,
                self.ww.name
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            mock_osunl.assert_called_once_with(
                self.ww.name
            )
            self.ww.seek(0)
            wrapper_lines = self.ww.read().splitlines()
            self.maxDiff = None
            exp_wrap = list(self.wrap_head)
            exp_wrap.extend([
                '#$ -binding linear:1',
                '#$ -N ' + job_name,
                '#$ -cwd',
                '#$ -q ' + queue,
                '#$ -r y',
                'MODULEPATH=' + ':'.join(mod_p) + ':$MODULEPATH',
                'module load mymodule',
            ])
            exp_wrap.extend(self.doc)
            exp_wrap.extend([' '.join(cmd), ''])
            self.assertListEqual(
                wrapper_lines,
                exp_wrap
            )
        mock_sprun.reset_mock()

    def test_submit_wrapper_with_gpu_control(
        self, mock_osunl, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['mycommand', 'arg1', 'arg2', ]
        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        w_conf = copy.deepcopy(conf_dict)
        w_conf['method_opts']['sge']['use_jobscript'] = True
        w_conf['method_opts']['sge']['copy_environment'] = False
        w_conf['copro_opts']['cuda']['set_visible'] = True
        w_conf['method_opts']['sge']['preserve_modules'] = True
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = w_conf['method_opts']['sge']
        mock_cpconf.return_value = w_conf['copro_opts']['cuda']

        with self.subTest("With GPU env vars"):
            expected_cmd = [
                self.qsub,
                self.ww.name
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    coprocessor='cuda',
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            mock_osunl.assert_called_once_with(
                self.ww.name
            )
            self.ww.seek(0)
            wrapper_lines = self.ww.read().splitlines()
            self.maxDiff = None
            exp_wrap = list(self.wrap_head)
            exp_wrap.extend([
                '#$ -l gputype=k80|p100',
                '#$ -l gpu=1',
                '#$ -N ' + job_name,
                '#$ -cwd',
                '#$ -q ' + queue,
                '#$ -r y',
                'module load mymodule',
            ])
            exp_wrap.extend(self.doc)
            exp_wrap.extend([
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
                'fi',
            ])
            exp_wrap.extend([' '.join(cmd), ''])
            self.assertListEqual(
                wrapper_lines,
                exp_wrap
            )
        mock_sprun.reset_mock()

    def test_submit_wrapper_comma_vars(
        self, mock_osunl, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['mycommand', 'arg1', 'arg2', ]
        mod_p = ['/usr/local/shellmodules', ]
        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        w_conf = copy.deepcopy(conf_dict)
        w_conf['method_opts']['sge']['use_jobscript'] = True
        w_conf['method_opts']['sge']['copy_environment'] = False
        w_conf['method_opts']['sge']['preserve_modules'] = True
        w_conf['method_opts']['sge']['add_module_paths'] = mod_p
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = w_conf['method_opts']['sge']
        mock_cpconf.return_value = w_conf['copro_opts']['cuda']

        with self.subTest("With extra module path of " + ':'.join(mod_p)):
            expected_cmd = [
                self.qsub,
                self.ww.name
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    export_vars=['AVAR=1,2']
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            mock_osunl.assert_called_once_with(
                self.ww.name
            )
            self.ww.seek(0)
            wrapper_lines = self.ww.read().splitlines()
            self.maxDiff = None
            exp_wrap = list(self.wrap_head)
            exp_wrap.extend([
                '#$ -binding linear:1',
                '#$ -N ' + job_name,
                '#$ -cwd',
                '#$ -q ' + queue,
                '#$ -r y',
                'MODULEPATH=' + ':'.join(mod_p) + ':$MODULEPATH',
                'module load mymodule',
            ])
            exp_wrap.extend(self.doc)
            exp_wrap.extend(['export AVAR="1,2"'])
            exp_wrap.extend([' '.join(cmd), ''])
            self.assertListEqual(
                wrapper_lines,
                exp_wrap
            )
        mock_sprun.reset_mock()

    def test_submit_wrapper_comma_vars_multiple(
        self, mock_osunl, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['mycommand', 'arg1', 'arg2', ]
        mod_p = ['/usr/local/shellmodules', ]
        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        w_conf = copy.deepcopy(conf_dict)
        w_conf['method_opts']['sge']['use_jobscript'] = True
        w_conf['method_opts']['sge']['copy_environment'] = False
        w_conf['method_opts']['sge']['preserve_modules'] = True
        w_conf['method_opts']['sge']['add_module_paths'] = mod_p
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = w_conf['method_opts']['sge']
        mock_cpconf.return_value = w_conf['copro_opts']['cuda']

        with self.subTest("With extra module path of " + ':'.join(mod_p)):
            expected_cmd = [
                self.qsub,
                self.ww.name
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    export_vars=['AVAR="1,2"', 'BVAR=a', 'CVAR="a space separated string"']
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            mock_osunl.assert_called_once_with(
                self.ww.name
            )
            self.ww.seek(0)
            wrapper_lines = self.ww.read().splitlines()
            self.maxDiff = None
            exp_wrap = list(self.wrap_head)
            exp_wrap[-1] = exp_wrap[-1].replace('-v ', '-v BVAR=a,')
            exp_wrap.extend([
                '#$ -binding linear:1',
                '#$ -N ' + job_name,
                '#$ -cwd',
                '#$ -q ' + queue,
                '#$ -r y',
                'MODULEPATH=' + ':'.join(mod_p) + ':$MODULEPATH',
                'module load mymodule',
            ])
            exp_wrap.extend(self.doc)
            exp_wrap.extend(['export AVAR="1,2"', 'export CVAR="a space separated string"'])
            exp_wrap.extend([' '.join(cmd), ''])
            self.assertListEqual(
                wrapper_lines,
                exp_wrap
            )
        mock_sprun.reset_mock()

    def test_submit_wrapper_keep(
        self, mock_osunl, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['mycommand', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        w_conf = copy.deepcopy(conf_dict)
        w_conf['method_opts']['sge']['use_jobscript'] = True
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = w_conf['method_opts']['sge']
        mock_cpconf.return_value = w_conf['copro_opts']['cuda']

        with self.subTest("No preserve"):
            expected_cmd = [
                self.qsub,
                self.ww.name
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            with patch('fsl_sub_plugin_sge.shutil.copy') as mock_copy:
                self.assertEqual(
                    jid,
                    self.plugin.submit(
                        command=cmd,
                        job_name=job_name,
                        queue=queue,
                        keep_jobscript=True
                    )
                )
                mock_sprun.assert_called_once_with(
                    expected_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                mock_osunl.assert_called_once_with(
                    self.ww.name
                )
                mock_copy.assert_called_once_with(
                    self.ww.name,
                    os.path.join(
                        os.getcwd(),
                        '_'.join(('wrapper', str(jid) + '.sh'))
                    )
                )
                self.ww.seek(0)
                wrapper_lines = self.ww.read().splitlines()
                self.maxDiff = None
                exp_wrap = list(self.wrap_head)
                exp_wrap.insert(2, '#$ -V')
                exp_wrap.extend([
                    '#$ -binding linear:1',
                    '#$ -N ' + job_name,
                    '#$ -cwd',
                    '#$ -q ' + queue,
                    '#$ -r y',
                ])
                exp_wrap.extend(self.doc)
                exp_wrap.extend([' '.join(cmd), ''])
                self.assertListEqual(
                    wrapper_lines,
                    exp_wrap
                )
            mock_sprun.reset_mock()

    def test_submit_wrapper_set_vars(
        self, mock_osunl, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['mycommand', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        w_conf = copy.deepcopy(conf_dict)
        w_conf['method_opts']['sge']['use_jobscript'] = True
        w_conf['method_opts']['sge']['copy_environment'] = False
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = w_conf['method_opts']['sge']
        mock_cpconf.return_value = w_conf['copro_opts']['cuda']

        with self.subTest("No preserve"):
            expected_cmd = [
                self.qsub,
                self.ww.name
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            mock_osunl.assert_called_once_with(
                self.ww.name
            )
            self.ww.seek(0)
            wrapper_lines = self.ww.read().splitlines()
            self.maxDiff = None
            exp_wrap = list(self.wrap_head)
            exp_wrap.extend([
                '#$ -binding linear:1',
                '#$ -N ' + job_name,
                '#$ -cwd',
                '#$ -q ' + queue,
                '#$ -r y',
            ])
            exp_wrap.extend(self.doc)
            exp_wrap.extend([' '.join(cmd), ''])
            self.assertListEqual(
                wrapper_lines,
                exp_wrap
            )
        mock_sprun.reset_mock()


@patch('fsl_sub.utils.VERSION', '1.0.0')
@patch('fsl_sub.utils.sys.argv', ['fsl_sub', '-q', 'a.q', 'acmd', 'arg1', 'arg2'])
@patch(
    'fsl_sub_plugin_sge._check_pe',
    autospec=True
)
@patch(
    'fsl_sub_plugin_sge.os.getcwd',
    autospec=True, return_value='/Users/testuser')
@patch('fsl_sub_plugin_sge.split_ram_by_slots', autospec=True)
@patch('fsl_sub_plugin_sge.coprocessor_config', autospec=True)
@patch('fsl_sub_plugin_sge.sp.run', autospec=True)
class TestSubmit(unittest.TestCase):
    def setUp(self):
        self.ww = tempfile.NamedTemporaryFile(
            mode='w+t',
            delete=False)

        self.bash = '/bin/bash'
        self.now = datetime.datetime.now()
        self.strftime = datetime.datetime.strftime
        os.environ['FSLSUB_SHELL'] = self.bash
        self.qsub = '/usr/bin/qsub'
        self.config = copy.deepcopy(conf_dict)
        self.mconfig = self.config['method_opts']['sge']
        self.patch_objects = {
            'fsl_sub.utils.datetime': {'autospec': True, },
            'fsl_sub_plugin_sge.plugin_version': {'autospec': True, 'return_value': '2.0.0', },
            'fsl_sub_plugin_sge.loaded_modules': {
                'autospec': True, 'return_value': ['mymodule', ]},
            'fsl_sub_plugin_sge._start_mode': {'autospec': True, 'return_value': 'unix_behavior', },
            'fsl_sub_plugin_sge.write_wrapper': {'autospec': True, 'side_effect': self.w_wrapper, },
            'fsl_sub_plugin_sge.method_config': {'return_value': self.mconfig, },
            'fsl_sub_plugin_sge.qsub_cmd': {'autospec': True, 'return_value': self.qsub, },
        }
        self.patches = {}
        for p, kwargs in self.patch_objects.items():
            self.patches[p] = patch(p, **kwargs)
        self.mocks = {}
        for o, p in self.patches.items():
            try:
                self.mocks[o] = p.start()
            except AttributeError:
                print("Error setting up mock for " + o)
        self.mocks['fsl_sub.utils.datetime'].datetime.now.return_value = self.now
        self.mocks['fsl_sub.utils.datetime'].datetime.strftime = self.strftime
        self.addCleanup(patch.stopall)
        self.job_name = 'test_job'
        self.queue = 'a.q'
        self.cmd = ['acmd', 'arg1', 'arg2', ]
        self.jid = 12345
        self.qsub_out = 'Your job ' + str(self.jid) + ' ("' + self.cmd[0] + '") has been submitted'
        self.q_env = (
            'FSLSUB_JOBID_VAR=JOB_ID,'
            'FSLSUB_ARRAYTASKID_VAR=SGE_TASK_ID,'
            'FSLSUB_ARRAYSTARTID_VAR=SGE_TASK_FIRST,'
            'FSLSUB_ARRAYENDID_VAR=SGE_TASK_LAST,'
            'FSLSUB_ARRAYSTEPSIZE_VAR=SGE_TASK_STEPSIZE,'
            'FSLSUB_ARRAYCOUNT_VAR="",'
            'FSLSUB_NSLOTS=NSLOTS')

    def TearDown(self):
        self.ww.close()
        os.unlink(self.ww.name)
        patch.stopall()

    plugin = fsl_sub_plugin_sge

    def w_wrapper(self, *args, **kwargs):
        for line in args[0]:
            self.ww.write(line + '\n')
        return self.ww.name

    def test_empty_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs, mock_getcwd, mock_check_pe):
        self.assertRaises(
            self.plugin.BadSubmission,
            self.plugin.submit,
            None, None, None
        )

    def test_submit_basic(
            self, mock_sprun, mock_cpconf,
            mock_srbs, mock_getcwd, mock_check_pe):
        with self.subTest("Univa"):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-N', self.job_name,
                '-cwd', '-q', self.queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=self.qsub_out, stderr=None)
            self.assertEqual(
                self.jid,
                self.plugin.submit(
                    command=self.cmd,
                    job_name=self.job_name,
                    queue=self.queue
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("sge"):
            sge_dict = copy.deepcopy(mconf_dict)
            sge_dict['affinity_control'] = 'slots'
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = sge_dict
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:slots',
                '-N', self.job_name,
                '-cwd', '-q', self.queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=self.qsub_out, stderr=None)
            self.assertEqual(
                self.jid,
                self.plugin.submit(
                    command=self.cmd,
                    job_name=self.job_name,
                    queue=self.queue
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("Bad affinity type"):
            sge_dict['affinity_control'] = 'nonsense'
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = sge_dict
            self.assertRaises(
                self.plugin.BadConfiguration,
                self.plugin.submit,
                command=self.cmd,
                job_name=self.job_name,
                queue=self.queue
            )

    @patch('fsl_sub_plugin_sge.queue_config')
    def test_set_time_limit(
            self, mock_qc, mock_sprun, mock_cpconf,
            mock_srbs, mock_getcwd, mock_check_pe):
        job_time = 10
        test_dict = copy.deepcopy(mconf_dict)
        test_dict['set_time_limit'] = True
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_dict
        expected_cmd = [
            self.qsub,
            '-V',
            '-v',
            self.q_env,
            '-binding',
            'linear:1',
            '-l', 'h_rt=' + str(job_time * 60),
            '-N', self.job_name,
            '-cwd', '-q', self.queue,
            '-r', 'y',
            '-shell', 'n',
            '-b', 'y',
            'acmd', 'arg1', 'arg2'
        ]
        mock_sprun.return_value = subprocess.CompletedProcess(
            expected_cmd, 0,
            stdout=self.qsub_out, stderr=None)
        self.assertEqual(
            self.jid,
            self.plugin.submit(
                command=self.cmd,
                job_name=self.job_name,
                queue=self.queue,
                jobtime=job_time
            )
        )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

    @patch('fsl_sub_plugin_sge.queue_config')
    def test_disable_set_time_limit(
            self, mock_qc, mock_sprun, mock_cpconf,
            mock_srbs, mock_getcwd, mock_check_pe):
        job_time = 10
        test_dict = copy.deepcopy(mconf_dict)
        test_dict['set_time_limit'] = True
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_dict
        expected_cmd = [
            self.qsub,
            '-V',
            '-v',
            self.q_env,
            '-binding',
            'linear:1',
            '-N', self.job_name,
            '-cwd', '-q', self.queue,
            '-r', 'y',
            '-shell', 'n',
            '-b', 'y',
            'acmd', 'arg1', 'arg2'
        ]
        mock_sprun.return_value = subprocess.CompletedProcess(
            expected_cmd, 0,
            stdout=self.qsub_out, stderr=None)
        with patch.dict('fsl_sub_plugin_sge.os.environ', {'FSLSUB_NOTIMELIMIT': '1', }):
            self.assertEqual(
                self.jid,
                self.plugin.submit(
                    command=self.cmd,
                    job_name=self.job_name,
                    queue=self.queue,
                    jobtime=job_time
                )
            )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

    @patch('fsl_sub_plugin_sge.queue_config')
    def test_set_hard_time(
            self, mock_qc, mock_sprun, mock_cpconf,
            mock_srbs, mock_getcwd, mock_check_pe):
        with self.subTest("with set time"):
            q_time = 20
            job_time = 10
            test_dict = copy.deepcopy(mconf_dict)
            test_dict['set_time_limit'] = True
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_dict
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-l', 'h_rt=' + str(job_time * 60),
                '-N', self.job_name,
                '-cwd', '-q', self.queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=self.qsub_out, stderr=None)
            self.assertEqual(
                self.jid,
                self.plugin.submit(
                    command=self.cmd,
                    job_name=self.job_name,
                    queue=self.queue,
                    jobtime=job_time
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("without set time"):
            q_time = 20
            job_time = 10
            test_dict = copy.deepcopy(mconf_dict)
            test_dict['set_time_limit'] = False
            test_dict['set_hard_time'] = True
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_dict
            mock_qc.return_value = {'time': q_time, }
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-l', 'h_rt=' + str(q_time * 60),
                '-N', self.job_name,
                '-cwd', '-q', self.queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=self.qsub_out, stderr=None)
            self.assertEqual(
                self.jid,
                self.plugin.submit(
                    command=self.cmd,
                    job_name=self.job_name,
                    queue=self.queue
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

    @patch('fsl_sub_plugin_sge.queue_config')
    def test_disable_set_hard_time(
            self, mock_qc, mock_sprun, mock_cpconf,
            mock_srbs, mock_getcwd, mock_check_pe):
        with self.subTest("with set time"):
            q_time = 20
            job_time = 10
            test_dict = copy.deepcopy(mconf_dict)
            test_dict['set_time_limit'] = True
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_dict
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-N', self.job_name,
                '-cwd', '-q', self.queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=self.qsub_out, stderr=None)
            with patch.dict('fsl_sub_plugin_sge.os.environ', {'FSLSUB_NOTIMELIMIT': '1', }):
                self.assertEqual(
                    self.jid,
                    self.plugin.submit(
                        command=self.cmd,
                        job_name=self.job_name,
                        queue=self.queue,
                        jobtime=job_time
                    )
                )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("without set time"):
            q_time = 20
            job_time = 10
            test_dict = copy.deepcopy(mconf_dict)
            test_dict['set_time_limit'] = False
            test_dict['set_hard_time'] = True
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_dict
            mock_qc.return_value = {'time': q_time, }
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-N', self.job_name,
                '-cwd', '-q', self.queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=self.qsub_out, stderr=None)
            with patch.dict('fsl_sub_plugin_sge.os.environ', {'FSLSUB_NOTIMELIMIT': '1', }):
                self.assertEqual(
                    self.jid,
                    self.plugin.submit(
                        command=self.cmd,
                        job_name=self.job_name,
                        queue=self.queue
                    )
                )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

    def test_submit_requeueable(
            self, mock_sprun, mock_cpconf,
            mock_srbs, mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]
        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest("Univa"):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    requeueable=False,
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

    def test_submit_logdir(
            self, mock_sprun, mock_cpconf,
            mock_srbs, mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest("logdir"):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-o', '/tmp/alog',
                '-e', '/tmp/alog',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    logdir="/tmp/alog"
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

    def test_no_env_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        test_dict = copy.deepcopy(mconf_dict)
        test_dict['copy_environment'] = False
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_dict
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        expected_cmd = [
            self.qsub,
            '-v',
            self.q_env,
            '-binding',
            'linear:1',
            '-N', job_name,
            '-cwd', '-q', queue,
            '-r', 'y',
            '-shell', 'n',
            '-b', 'y',
            'acmd', 'arg1', 'arg2'
        ]
        mock_sprun.return_value = subprocess.CompletedProcess(
            expected_cmd, 0,
            stdout=qsub_out, stderr=None)
        self.assertEqual(
            jid,
            self.plugin.submit(
                command=cmd,
                job_name=job_name,
                queue=queue,
            )
        )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

    def test_no_affinity_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        test_dict = copy.deepcopy(mconf_dict)
        test_dict['affinity_type'] = None
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_dict
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        expected_cmd = [
            self.qsub,
            '-V',
            '-v',
            self.q_env,
            '-N', job_name,
            '-cwd', '-q', queue,
            '-r', 'y',
            '-shell', 'n',
            '-b', 'y',
            'acmd', 'arg1', 'arg2'
        ]
        mock_sprun.return_value = subprocess.CompletedProcess(
            expected_cmd, 0,
            stdout=qsub_out, stderr=None)
        self.assertEqual(
            jid,
            self.plugin.submit(
                command=cmd,
                job_name=job_name,
                queue=queue,
            )
        )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

    def test_priority_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest("No priorities"):
            test_dict = copy.deepcopy(mconf_dict)
            test_dict['job_priorities'] = False
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_dict
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    priority=1000
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = copy.deepcopy(mconf_dict)
        with self.subTest("With priorities"):
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = copy.deepcopy(mconf_dict)
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-p', str(-1000),
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    priority=-1000
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = copy.deepcopy(mconf_dict)
        with self.subTest("With priorities (limited)"):
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = copy.deepcopy(mconf_dict)
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-p', str(-1023),
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    priority=-2000
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = copy.deepcopy(mconf_dict)
        with self.subTest("With priorities positive"):
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = copy.deepcopy(mconf_dict)
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-p', str(0),
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    priority=2000
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

    def test_project_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        project = 'Aproject'
        cmd = ['acmd', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest("No projects"):
            test_dict = copy.deepcopy(mconf_dict)
            test_dict['projects'] = False
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_dict
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-N', 'test_job',
                '-cwd', '-q', 'a.q',
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = copy.deepcopy(mconf_dict)
        with self.subTest("With Project"):
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = copy.deepcopy(mconf_dict)
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-N', 'test_job',
                '-cwd', '-q', 'a.q',
                '-r', 'y',
                '-P', project,
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    project=project
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

    def test_resources_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest("With single resource"):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-l', 'ramlimit=1000',
                '-N', job_name,
                '-cwd', '-q', 'a.q',
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    resources='ramlimit=1000'
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("With multiple resources"):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-l', 'resource1=1,resource2=2',
                '-N', 'test_job',
                '-cwd', '-q', 'a.q',
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    resources=['resource1=1', 'resource2=2', ]
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

    def test_job_hold_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        jid = 12345
        hjid = 12344
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest("Basic string"):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-hold_jid', str(hjid),
                '-N', job_name,
                '-cwd', '-q', 'a.q',
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    jobhold=hjid
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        with self.subTest("List"):
            mock_sprun.reset_mock()
            hjid2 = 23456
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-hold_jid', ",".join((str(hjid), str(hjid2))),
                '-N', job_name,
                '-cwd', '-q', 'a.q',
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    jobhold=[hjid, hjid2]
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        with self.subTest("List of strings"):
            mock_sprun.reset_mock()
            hjid2 = 23456
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-hold_jid', ",".join((str(hjid), str(hjid2))),
                '-N', job_name,
                '-cwd', '-q', 'a.q',
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    jobhold=[str(hjid), str(hjid2)]
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        with self.subTest("Tuple"):
            mock_sprun.reset_mock()
            hjid2 = 23456
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-hold_jid', ",".join((str(hjid), str(hjid2))),
                '-N', job_name,
                '-cwd', '-q', 'a.q',
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    jobhold=(hjid, hjid2)
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        with self.subTest("Native"):
            mock_sprun.reset_mock()
            native_hjid = "1234,2345"
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-hold_jid', native_hjid,
                '-N', job_name,
                '-cwd', '-q', 'a.q',
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    jobhold=native_hjid,
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

    def test_no_array_hold_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        self.assertRaises(
            self.plugin.BadSubmission,
            self.plugin.submit,
            command=cmd,
            job_name=job_name,
            queue=queue,
            array_hold=12345
        )

    def test_no_array_limit_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        self.assertRaises(
            self.plugin.BadSubmission,
            self.plugin.submit,
            command=cmd,
            job_name=job_name,
            queue=queue,
            array_limit=5
        )

    def test_jobram_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        jid = 123456
        jobram = 1024
        cmd = ['acmd', 'arg1', 'arg2', ]

        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest('Basic submission'):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-l', "h_vmem={0}G,m_mem_free={0}G".format(jobram),
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    jobram=jobram
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("Split on RAM"):
            threads = 2
            split_ram = jobram // threads
            mock_srbs.return_value = split_ram
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:2',
                '-l', "h_vmem={0}G,m_mem_free={0}G".format(split_ram),
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    jobram=jobram,
                    threads=threads,
                    ramsplit=True
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        ram_override = "2048"
        with self.subTest('Not overriding memory request 1'):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-l', "m_mem_free={0}G".format(ram_override),
                '-l', "h_vmem={0}G".format(jobram),
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    jobram=jobram,
                    resources=['m_mem_free=' + ram_override + 'G']
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest('Not overriding memory request 2'):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-l', "h_vmem={0}G".format(ram_override),
                '-l', "m_mem_free={0}G".format(jobram),
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    jobram=jobram,
                    resources=['h_vmem=' + ram_override + 'G']
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest('Not overriding memory request 3'):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-l', "m_mem_free={0}G,h_vmem={0}G".format(ram_override),
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    jobram=jobram,
                    resources=[
                        'm_mem_free=' + ram_override + 'G',
                        'h_vmem=' + ram_override + 'G',
                    ]
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()

    def test_mail_support(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        jid = 123456
        mailto = 'auser@adomain.com'
        mail_on = 'e'
        cmd = ['acmd', 'arg1', 'arg2', ]

        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest("Test mail settings"):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-M', mailto,
                '-m', mail_on,
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    mailto=mailto,
                    mail_on=mail_on
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("Test for auto set of mail mode"):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-M', mailto,
                '-m', mconf_dict['mail_mode'],
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    mailto=mailto,
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("Test for multiple mail modes"):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-M', mailto,
                '-m', 'a,e,b',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    mailto=mailto,
                    mail_on='f'
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

        with self.subTest("Test for bad input"):
            mail_on = 't'
            self.assertRaises(
                self.plugin.BadSubmission,
                self.plugin.submit,
                command=cmd,
                job_name=job_name,
                queue=queue,
                mailto=mailto,
                mail_on=mail_on
            )

    def test_coprocessor_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        jid = 123456
        cmd = ['acmd', 'arg1', 'arg2', ]
        copro_type = 'cuda'
        cp_opts = copy.deepcopy(conf_dict['copro_opts'][copro_type])
        mock_cpconf.return_value = cp_opts
        gpuclass = 'P'
        gputype = cp_opts['class_types'][gpuclass]['resource']
        second_gtype = cp_opts['class_types']['K']['resource']
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest("Test basic GPU"):
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-l', 'gputype=' + '|'.join((second_gtype, gputype)),
                '-l', 'gpu=1',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    coprocessor=copro_type,
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("Test specific class of GPU"):
            gpuclass = 'K'
            gputype = cp_opts['class_types'][gpuclass]['resource']
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-l', 'gputype=' + gputype,
                '-l', 'gpu=1',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    coprocessor=copro_type,
                    coprocessor_class_strict=True
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("Test more capable classes of GPU"):
            gpuclass = 'K'
            gputype = cp_opts['class_types'][gpuclass]['resource']
            second_gtype = cp_opts['class_types']['P']['resource']
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-l', 'gputype={0}|{1}'.format(gputype, second_gtype),
                '-l', 'gpu=1',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    coprocessor=copro_type,
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("Test more capable classes of GPU (configuration)"):
            test_mconf = copy.deepcopy(mconf_dict)
            copro_opts = copy.deepcopy(cp_opts)
            copro_opts['include_more_capable'] = False
            gpuclass = 'K'
            gputype = cp_opts['class_types'][gpuclass]['resource']
            mock_cpconf.return_value = copro_opts
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-l', 'gputype=' + gputype,
                '-l', 'gpu=1',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_mconf
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    coprocessor=copro_type,
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        mock_cpconf.return_value = cp_opts
        with self.subTest("Test multi-GPU"):
            multi_gpu = 2
            gpuclass = cp_opts['default_class']
            gputype = 'k80|p100'
            expected_cmd = [
                self.qsub,
                '-V',
                '-v',
                self.q_env,
                '-l', 'gputype=' + gputype,
                '-l', 'gpu=' + str(multi_gpu),
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    coprocessor=copro_type,
                    coprocessor_multi=2
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

    @patch('fsl_sub_plugin_sge.qconf_cmd', autospec=True)
    def test_parallel_env_submit(
            self, mock_qconf, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        mock_qconf.return_value = '/usr/bin/qconf'
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest("One thread"):
            expected_cmd = [
                self.qsub,
                '-pe', 'openmp', '1',
                '-R', 'y',
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    parallel_env='openmp',
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("Two threads"):
            expected_cmd = [
                self.qsub,
                '-pe', 'openmp', str(2),
                '-R', 'y',
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:2',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    parallel_env='openmp',
                    threads=2
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

        with self.subTest("Bad PE"):
            mock_check_pe.side_effect = self.plugin.BadSubmission
            self.assertRaises(
                self.plugin.BadSubmission,
                self.plugin.submit,
                command=cmd,
                job_name=job_name,
                queue=queue,
                parallel_env='openmp',
                threads=2
            )

    @patch('fsl_sub_plugin_sge.qconf_cmd', autospec=True)
    def test_multiqueue_submit(
            self, mock_qconf, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        mock_qconf.return_value = '/usr/bin/qconf'
        job_name = 'test_job'
        queue = 'a.q,b.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        jid = 12345
        qsub_out = 'Your job ' + str(jid) + ' ("acmd") has been submitted'
        with self.subTest("As string"):
            expected_cmd = [
                self.qsub,
                '-pe', 'openmp', '1',
                '-R', 'y',
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:1',
                '-N', job_name,
                '-cwd', '-q', queue,
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    parallel_env='openmp',
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        mock_sprun.reset_mock()
        with self.subTest("As list"):
            queue = ['a.q', 'b.q', ]
            expected_cmd = [
                self.qsub,
                '-pe', 'openmp', str(2),
                '-R', 'y',
                '-V',
                '-v',
                self.q_env,
                '-binding',
                'linear:2',
                '-N', job_name,
                '-cwd', '-q', ','.join(queue),
                '-r', 'y',
                '-shell', 'n',
                '-b', 'y',
                'acmd', 'arg1', 'arg2'
            ]
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=cmd,
                    job_name=job_name,
                    queue=queue,
                    parallel_env='openmp',
                    threads=2
                )
            )
            mock_sprun.assert_called_once_with(
                expected_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

    def test_array_hold_on_non_array_submit(
            self, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        cmd = ['acmd', 'arg1', 'arg2', ]

        hjid = 12344
        self.assertRaises(
            self.plugin.BadSubmission,
            self.plugin.submit,
            command=cmd,
            job_name=job_name,
            queue=queue,
            array_hold=hjid
        )

    @patch('fsl_sub_plugin_sge.os.remove', autospec=True)
    def test_array_submit(
            self, mock_osr, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        job_file = '''
acmd 1 2 3
acmd 4 5 6
acmd 6 7 8
'''
        job_file_name = 'll_job'
        jid = 12344
        qsub_out = 'Your job ' + str(jid) + ' ("test_job") has been submitted'
        expected_cmd = [
            self.qsub,
            self.ww.name
        ]
        with patch(
                'fsl_sub_plugin_sge.open',
                new_callable=mock_open, read_data=job_file) as m:
            m.return_value.__iter__.return_value = job_file.splitlines()
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=[job_file_name],
                    job_name=job_name,
                    queue=queue,
                    array_task=True
                )
            )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        self.ww.seek(0)
        wrapper_lines = self.ww.read().splitlines()
        wrapper_lines
        self.assertListEqual(
            wrapper_lines,
            [
                '#!' + self.bash,
                '',
                '# Built by fsl_sub v.1.0.0 and fsl_sub_plugin_sge v.2.0.0',
                '# Command line: fsl_sub -q a.q acmd arg1 arg2',
                '# Submission time (H:M:S DD/MM/YYYY): {0}'.format(self.now.strftime("%H:%M:%S %d/%m/%Y")),
                '',
                '#$ -S ' + self.bash,
                '',
                'the_command=$(sed -n -e "${{SGE_TASK_ID}}p" {0})'.format(job_file_name),
                '',
                'exec ' + self.bash + ' -c "$the_command"',
                ''
            ]
        )

        mock_osr.assert_called_once_with(self.ww.name)

    @patch('fsl_sub_plugin_sge.os.remove', autospec=True)
    def test_array_submit_fails(
            self, mock_osr, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        job_file = '''
acmd 1 2 3
acmd 4 5 6
acmd 6 7 8
'''
        job_file_name = 'll_job'
        jid = 12344
        qsub_out = 'Your job ' + str(jid) + ' ("test_job") has been submitted'
        expected_cmd = [
            self.qsub,
            self.ww.name
        ]
        with patch(
                'fsl_sub_plugin_sge.open',
                new_callable=mock_open, read_data=job_file) as m:
            m.return_value.__iter__.return_value = job_file.splitlines()
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 1, stdout=qsub_out, stderr="Bad job")
            self.assertRaises(
                self.plugin.BadSubmission,
                self.plugin.submit,
                command=[job_file_name],
                job_name=job_name,
                queue=queue,
                array_task=True
            )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        self.ww.seek(0)
        wrapper_lines = self.ww.read().splitlines()
        self.assertListEqual(
            wrapper_lines,
            [
                '#!' + self.bash,
                '',
                '# Built by fsl_sub v.1.0.0 and fsl_sub_plugin_sge v.2.0.0',
                '# Command line: fsl_sub -q a.q acmd arg1 arg2',
                '# Submission time (H:M:S DD/MM/YYYY): {0}'.format(self.now.strftime("%H:%M:%S %d/%m/%Y")),
                '',
                '#$ -S ' + self.bash,
                '',
                'the_command=$(sed -n -e "${{SGE_TASK_ID}}p" {0})'.format(job_file_name),
                '',
                'exec ' + self.bash + ' -c "$the_command"',
                ''
            ]
        )
        mock_osr.assert_called_once_with(self.ww.name)

    @patch('fsl_sub_plugin_sge.os.remove', autospec=True)
    def test_array_submit_complex_commands(
            self, mock_osr, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        job_file = '''
sleep 1; acmd 1 2 3
sleep 1; acmd 4 5 6
sleep 1; acmd 6 7 8
'''
        job_file_name = 'll_job'
        jid = 12344
        qsub_out = 'Your job ' + str(jid) + ' ("test_job") has been submitted'
        expected_cmd = [
            self.qsub,
            self.ww.name
        ]
        with patch(
                'fsl_sub_plugin_sge.open',
                new_callable=mock_open, read_data=job_file) as m:
            m.return_value.__iter__.return_value = job_file.splitlines()
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=[job_file_name],
                    job_name=job_name,
                    queue=queue,
                    array_task=True
                )
            )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        self.ww.seek(0)
        wrapper_lines = self.ww.read().splitlines()
        wrapper_lines
        self.assertListEqual(
            wrapper_lines,
            [
                '#!' + self.bash,
                '',
                '# Built by fsl_sub v.1.0.0 and fsl_sub_plugin_sge v.2.0.0',
                '# Command line: fsl_sub -q a.q acmd arg1 arg2',
                '# Submission time (H:M:S DD/MM/YYYY): {0}'.format(self.now.strftime("%H:%M:%S %d/%m/%Y")),
                '',
                '#$ -S ' + self.bash,
                '',
                'the_command=$(sed -n -e "${{SGE_TASK_ID}}p" {0})'.format(job_file_name),
                '',
                'exec ' + self.bash + ' -c "$the_command"',
                ''
            ]
        )

        mock_osr.assert_called_once_with(self.ww.name)

    @patch('fsl_sub_plugin_sge.os.remove', autospec=True)
    def test_array_submit_specifier(
            self, mock_osr, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        job_file_name = ['ll_job']
        jid = 12344
        qsub_out = 'Your job ' + str(jid) + ' ("test_job") has been submitted'
        expected_cmd = [
            self.qsub,
            '-V',
            '-v',
            self.q_env,
            '-binding',
            'linear:1',
            '-N', job_name,
            '-cwd', '-q', queue,
            '-r', 'y',
            '-t', "1-8:2",
            '-shell', 'n', '-b', 'y',
            ''.join(job_file_name)
        ]
        mock_sprun.return_value = subprocess.CompletedProcess(
            expected_cmd, 0,
            stdout=qsub_out, stderr=None)
        self.assertEqual(
            jid,
            self.plugin.submit(
                command=job_file_name,
                job_name=job_name,
                queue=queue,
                array_task=True,
                array_specifier='1-8:2'
            )
        )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

    @patch('fsl_sub_plugin_sge.os.remove', autospec=True)
    def test_array_limit_submit(
            self, mock_osr, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        job_file = '''
acmd 1 2 3
acmd 4 5 6
acmd 6 7 8
'''
        job_file_name = 'll_job'
        jid = 12344
        limit = 2
        qsub_out = 'Your job ' + str(jid) + ' ("test_job") has been submitted'
        expected_cmd = [
            self.qsub,
            self.ww.name
        ]
        with patch(
                'fsl_sub_plugin_sge.open',
                new_callable=mock_open, read_data=job_file) as m:
            m.return_value.__iter__.return_value = job_file.splitlines()
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=[job_file_name],
                    job_name=job_name,
                    queue=queue,
                    array_task=True,
                    array_limit=limit
                )
            )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        self.ww.seek(0)
        wrapper_lines = self.ww.read().splitlines()
        self.assertListEqual(
            wrapper_lines,
            [
                '#!' + self.bash,
                '',
                '# Built by fsl_sub v.1.0.0 and fsl_sub_plugin_sge v.2.0.0',
                '# Command line: fsl_sub -q a.q acmd arg1 arg2',
                '# Submission time (H:M:S DD/MM/YYYY): {0}'.format(self.now.strftime("%H:%M:%S %d/%m/%Y")),
                '',
                '#$ -S ' + self.bash,
                '',
                'the_command=$(sed -n -e "${{SGE_TASK_ID}}p" {0})'.format(job_file_name),
                '',
                'exec ' + self.bash + ' -c "$the_command"',
                ''
            ]
        )
        mock_osr.assert_called_once_with(self.ww.name)

    @patch('fsl_sub_plugin_sge.os.remove', autospec=True)
    def test_array_limit_disabled_submit(
            self, mock_osr, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        job_file = '''
acmd 1 2 3
acmd 4 5 6
acmd 6 7 8
'''
        job_file_name = 'll_job'
        jid = 12344
        qsub_out = 'Your job ' + str(jid) + ' ("test_job") has been submitted'
        test_mconf = copy.deepcopy(mconf_dict)
        test_mconf['array_limit'] = False
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_mconf
        expected_cmd = [
            self.qsub,
            self.ww.name
        ]
        with patch(
                'fsl_sub_plugin_sge.open',
                new_callable=mock_open, read_data=job_file) as m:
            m.return_value.__iter__.return_value = job_file.splitlines()
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=[job_file_name],
                    job_name=job_name,
                    queue=queue,
                    array_task=True,
                    array_limit=2
                )
            )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        self.ww.seek(0)
        wrapper_lines = self.ww.read().splitlines()
        self.assertListEqual(
            wrapper_lines,
            [
                '#!' + self.bash,
                '',
                '# Built by fsl_sub v.1.0.0 and fsl_sub_plugin_sge v.2.0.0',
                '# Command line: fsl_sub -q a.q acmd arg1 arg2',
                '# Submission time (H:M:S DD/MM/YYYY): {0}'.format(self.now.strftime("%H:%M:%S %d/%m/%Y")),
                '',
                '#$ -S ' + self.bash,
                '',
                'the_command=$(sed -n -e "${{SGE_TASK_ID}}p" {0})'.format(job_file_name),
                '',
                'exec ' + self.bash + ' -c "$the_command"',
                ''
            ]
        )
        mock_osr.assert_called_once_with(self.ww.name)

    @patch('fsl_sub_plugin_sge.os.remove', autospec=True)
    def test_array_hold_submit(
            self, mock_osr, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        job_file = '''
acmd 1 2 3
acmd 4 5 6
acmd 6 7 8
'''
        job_file_name = 'll_job'
        jid = 12344
        hold_jid = 12343
        qsub_out = 'Your job ' + str(jid) + ' ("test_job") has been submitted'
        expected_cmd = [
            self.qsub,
            self.ww.name
        ]
        with patch(
                'fsl_sub_plugin_sge.open',
                new_callable=mock_open, read_data=job_file) as m:
            m.return_value.__iter__.return_value = job_file.splitlines()
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=[job_file_name],
                    job_name=job_name,
                    queue=queue,
                    array_task=True,
                    array_hold=hold_jid
                )
            )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        self.ww.seek(0)
        wrapper_lines = self.ww.read().splitlines()
        self.assertListEqual(
            wrapper_lines,
            [
                '#!' + self.bash,
                '',
                '# Built by fsl_sub v.1.0.0 and fsl_sub_plugin_sge v.2.0.0',
                '# Command line: fsl_sub -q a.q acmd arg1 arg2',
                '# Submission time (H:M:S DD/MM/YYYY): {0}'.format(self.now.strftime("%H:%M:%S %d/%m/%Y")),
                '',
                '#$ -S ' + self.bash,
                '',
                'the_command=$(sed -n -e "${{SGE_TASK_ID}}p" {0})'.format(job_file_name),
                '',
                'exec ' + self.bash + ' -c "$the_command"',
                ''
            ]
        )
        mock_osr.assert_called_once_with(self.ww.name)

    @patch('fsl_sub_plugin_sge.os.remove', autospec=True)
    def test_export_vars_config_submit(
            self, mock_osr, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        command = ['./mycommand', 'arg1', 'arg2', ]
        jid = 12344
        qsub_out = 'Your job ' + str(jid) + ' ("test_job") has been submitted'
        expected_cmd = [
            self.qsub,
            self.ww.name
        ]
        exp_head = [
            '#!' + self.bash,
            '',
            '#$ -V',
        ]
        exp_vars = self.q_env
        exp_cmd_next = [
            '#$ -binding linear:1',
            '#$ -N ' + job_name,
            '#$ -cwd',
            '#$ -q ' + queue,
            '#$ -r y',
        ]

        exp_cmd_start = list(exp_head)
        exp_cmd_mid = []
        exp_cmd_mid.extend([
            '# Built by fsl_sub v.1.0.0 and fsl_sub_plugin_sge v.2.0.0',
            '# Command line: fsl_sub -q a.q acmd arg1 arg2',
            '# Submission time (H:M:S DD/MM/YYYY): {0}'.format(self.now.strftime("%H:%M:%S %d/%m/%Y")),
            '',
        ])

        self.config['method_opts']['sge']['use_jobscript'] = True
        self.config['method_opts']['sge']['export_vars'] = ['FSLTEST']
        self.mconfig['use_jobscript'] = True
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = self.mconfig

        with self.subTest("Export vars"):
            test_cmd = copy.copy(exp_cmd_start)
            test_cmd.append('#$ -v ' + exp_vars + ',FSLTEST')
            test_cmd.extend(exp_cmd_next)
            test_cmd.extend(exp_cmd_mid)
            test_cmd.extend([' '.join(command), ''])
            with patch.dict('fsl_sub_plugin_sge.os.environ', {'FSLTEST': 'abcd'}):
                self.maxDiff = None
                mock_sprun.return_value = subprocess.CompletedProcess(
                    expected_cmd, 0,
                    stdout=qsub_out, stderr=None)
                self.assertEqual(
                    jid,
                    self.plugin.submit(
                        command=command,
                        job_name=job_name,
                        queue=queue,
                    )
                )
                mock_sprun.assert_called_once_with(
                    expected_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                self.ww.seek(0)
                wrapper_lines = self.ww.read().splitlines()
                self.assertListEqual(
                    wrapper_lines,
                    test_cmd
                )
                mock_osr.assert_called_once_with(self.ww.name)

        with self.subTest("Export vars with value"):
            mock_sprun.reset_mock()
            mock_osr.reset_mock()
            self.ww.seek(0)
            self.ww.truncate()
            self.config['method_opts']['sge']['export_vars'] = ['FSLTEST="abcd"']
            self.mocks['fsl_sub_plugin_sge.method_config'].return_value = self.mconfig
            test_cmd = copy.copy(exp_cmd_start)
            test_cmd.append('#$ -v ' + exp_vars + ',FSLTEST="abcd"')
            test_cmd.extend(exp_cmd_next)
            test_cmd.extend(exp_cmd_mid)
            test_cmd.extend([' '.join(command), ''])
            with patch.dict('fsl_sub_plugin_sge.os.environ', {'FSLTEST': 'abcd'}):
                self.maxDiff = None
                mock_sprun.return_value = subprocess.CompletedProcess(
                    expected_cmd, 0,
                    stdout=qsub_out, stderr=None)
                self.assertEqual(
                    jid,
                    self.plugin.submit(
                        command=command,
                        job_name=job_name,
                        queue=queue,
                    )
                )
                mock_sprun.assert_called_once_with(
                    expected_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                self.ww.seek(0)
                wrapper_lines = self.ww.read().splitlines()
                self.assertListEqual(
                    wrapper_lines,
                    test_cmd
                )
                mock_osr.assert_called_once_with(self.ww.name)

    @patch('fsl_sub_plugin_sge.os.remove', autospec=True)
    def test_export_vars_submit(
            self, mock_osr, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        command = ['./mycommand', 'arg1', 'arg2', ]
        jid = 12344
        qsub_out = 'Your job ' + str(jid) + ' ("test_job") has been submitted'
        expected_cmd = [
            self.qsub,
            self.ww.name
        ]
        exp_head = [
            '#!' + self.bash,
            '',
            '#$ -V',
        ]
        exp_vars = self.q_env
        exp_cmd_next = [
            '#$ -binding linear:1',
            '#$ -N ' + job_name,
            '#$ -cwd',
            '#$ -q ' + queue,
            '#$ -r y',
        ]

        exp_cmd_start = list(exp_head)
        exp_cmd_mid = []
        exp_cmd_mid.extend([
            '# Built by fsl_sub v.1.0.0 and fsl_sub_plugin_sge v.2.0.0',
            '# Command line: fsl_sub -q a.q acmd arg1 arg2',
            '# Submission time (H:M:S DD/MM/YYYY): {0}'.format(self.now.strftime("%H:%M:%S %d/%m/%Y")),
            '',
        ])

        self.config['method_opts']['sge']['use_jobscript'] = True
        self.mconfig['use_jobscript'] = True
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = self.mconfig

        with self.subTest("Export vars"):
            test_cmd = copy.copy(exp_cmd_start)
            test_cmd.append('#$ -v ' + 'MYVAR,' + exp_vars)
            test_cmd.extend(exp_cmd_next)
            test_cmd.extend(exp_cmd_mid)
            test_cmd.extend([' '.join(command), ''])
            with patch.dict('fsl_sub_plugin_sge.os.environ', {'MYVAR': 'abcd'}):
                self.maxDiff = None
                mock_sprun.return_value = subprocess.CompletedProcess(
                    expected_cmd, 0,
                    stdout=qsub_out, stderr=None)
                self.assertEqual(
                    jid,
                    self.plugin.submit(
                        command=command,
                        job_name=job_name,
                        queue=queue,
                        export_vars=['MYVAR', ]
                    )
                )
                mock_sprun.assert_called_once_with(
                    expected_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                self.ww.seek(0)
                wrapper_lines = self.ww.read().splitlines()
                self.assertListEqual(
                    wrapper_lines,
                    test_cmd
                )
                mock_osr.assert_called_once_with(self.ww.name)

    @patch('fsl_sub_plugin_sge.os.remove', autospec=True)
    def test_array_hold_disabled_submit(
            self, mock_osr, mock_sprun, mock_cpconf,
            mock_srbs,
            mock_getcwd, mock_check_pe):
        job_name = 'test_job'
        queue = 'a.q'
        job_file = '''
acmd 1 2 3
acmd 4 5 6
acmd 6 7 8
'''
        job_file_name = 'll_job'
        jid = 12344
        hold_jid = 12343
        qsub_out = 'Your job ' + str(jid) + ' ("test_job") has been submitted'
        test_mconf = copy.deepcopy(mconf_dict)
        test_mconf['array_holds'] = False
        self.mocks['fsl_sub_plugin_sge.method_config'].return_value = test_mconf
        expected_cmd = [
            self.qsub,
            self.ww.name
        ]
        with patch(
                'fsl_sub_plugin_sge.open',
                new_callable=mock_open, read_data=job_file) as m:
            m.return_value.__iter__.return_value = job_file.splitlines()
            mock_sprun.return_value = subprocess.CompletedProcess(
                expected_cmd, 0,
                stdout=qsub_out, stderr=None)
            self.assertEqual(
                jid,
                self.plugin.submit(
                    command=[job_file_name],
                    job_name=job_name,
                    queue=queue,
                    array_task=True,
                    array_hold=hold_jid
                )
            )
        mock_sprun.assert_called_once_with(
            expected_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        self.ww.seek(0)
        wrapper_lines = self.ww.read().splitlines()
        self.assertListEqual(
            wrapper_lines,
            [
                '#!' + self.bash,
                '',
                '# Built by fsl_sub v.1.0.0 and fsl_sub_plugin_sge v.2.0.0',
                '# Command line: fsl_sub -q a.q acmd arg1 arg2',
                '# Submission time (H:M:S DD/MM/YYYY): {0}'.format(self.now.strftime("%H:%M:%S %d/%m/%Y")),
                '',
                '#$ -S ' + self.bash,
                '',
                'the_command=$(sed -n -e "${{SGE_TASK_ID}}p" {0})'.format(job_file_name),
                '',
                'exec ' + self.bash + ' -c "$the_command"',
                ''
            ]
        )
        mock_osr.assert_called_once_with(self.ww.name)


class TestQdel(unittest.TestCase):
    @patch('fsl_sub_plugin_sge.which', autospec=True)
    @patch('fsl_sub_plugin_sge.sp.run', autospec=True)
    def testqdel(self, mock_spr, mock_which):
        pid = 1234
        mock_which.return_value = '/usr/bin/qdel'
        mock_spr.return_value = subprocess.CompletedProcess(
            ['/usr/bin/qdel', str(pid)],
            0,
            'Job ' + str(pid) + ' deleted',
            ''
        )
        self.assertTupleEqual(
            fsl_sub_plugin_sge.qdel(pid),
            ('Job ' + str(pid) + ' deleted', 0)
        )
        mock_spr.assert_called_once_with(
            ['/usr/bin/qdel', str(pid)],
            universal_newlines=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )


class TestJobStatus(unittest.TestCase):
    def setUp(self):
        self.QUEUED = 0
        self.RUNNING = 1
        self.FINISHED = 2
        self.FAILED = 3
        self.HELD = 4
        self.REQUEUED = 5
        self.RESTARTED = 6
        self.SUSPENDED = 7
        self.STARTING = 8

        self.REPORTING = [
            'Queued',
            'Running',
            'Finished',
            'Failed but requeued',
            'Held',
            'Requeued',
            'Restarted',
            'Suspended',
            'Starting'
        ]

        self.qacct_out_univa = '''==============================================================
qname        a.q
hostname     node1.cluster.com
group        agroup
owner        auser
project      myproject
department   defaultdepartment
jobname      feat_job
jobnumber    123456
taskid       undefined
pe_taskid    NONE
account      sge
priority     0
cwd          /myfolder
submit_host  submitnode.cluster.com
submit_cmd   /bin/qsub /tmp/tmprih81yic
qsub_time    11/19/2020 13:09:58.720
start_time   11/19/2020 13:10:07.739
end_time     11/19/2020 13:10:57.812
granted_pe   NONE
slots        1
failed       0
deleted_by   NONE
exit_status  0
ru_wallclock 50.073
ru_utime     0.012
ru_stime     0.008
ru_maxrss    10552
ru_ixrss     0
ru_ismrss    0
ru_idrss     0
ru_isrss     0
ru_minflt    3305
ru_majflt    0
ru_nswap     0
ru_inblock   0
ru_oublock   16
ru_msgsnd    0
ru_msgrcv    0
ru_nsignals  0
ru_nvcsw     29
ru_nivcsw    6
wallclock    50.107
cpu          0.020
mem          0.000
io           0.000
iow          0.000
ioops        160
maxvmem      13.602M
maxrss       1.926M
maxpss       491.000K
arid         undefined
jc_name      NONE
bound_cores  NONE
'''
        self.qacct_out = '''==============================================================
qname        long.q
hostname     host1.uk
group        auser
owner        auser
project      NONE
department   defaultdepartment
jobname      feat_job
jobnumber    123456
taskid       undefined
account      sge
priority     10
qsub_time    Mon Nov  9 12:42:26 2020
start_time   Mon Nov  9 12:44:31 2020
end_time     Mon Nov  9 15:18:32 2020
granted_pe   NONE
slots        1
failed       0
exit_status  0
ru_wallclock 9241s
ru_utime     8669.690s
ru_stime     499.526s
ru_maxrss    9.989MB
ru_ixrss     0.000B
ru_ismrss    0.000B
ru_idrss     0.000B
ru_isrss     0.000B
ru_minflt    9222727
ru_majflt    8
ru_nswap     0
ru_inblock   3747872
ru_oublock   16328568
ru_msgsnd    0
ru_msgrcv    0
ru_nsignals  0
ru_nvcsw     487949
ru_nivcsw    15695
cpu          9169.216s
mem          41.984TBs
io           45.348GB
iow          0.000s
maxvmem      7.651GB
arid         undefined
ar_sub_time  undefined
category     -u auser -q long.q
'''
        self.qacct_job = {
            'id': 123456,
            'name': 'feat_job',
            'sub_time': datetime.datetime(2020, 11, 9, 12, 42, 26),
            'tasks': {
                1: {
                    'status': self.FINISHED,
                    'start_time': datetime.datetime(2020, 11, 9, 12, 44, 31),
                    'end_time': datetime.datetime(2020, 11, 9, 15, 18, 32),
                },
            },
        }

        self.qstat_job = {
            'id': 123456,
            'name': 'feat',
            'sub_time': datetime.datetime.fromtimestamp(1603383001),
            'tasks': {
                1: {
                    'status': self.RUNNING,
                    'start_time': datetime.datetime.fromtimestamp(1603383003),
                    'end_time': None,
                },
            },
        }
        self.qacct_job_univa = {
            'id': 123456,
            'name': 'feat_job',
            'sub_time': datetime.datetime(2020, 11, 19, 13, 9, 58, 720000),
            'tasks': {
                1: {
                    'status': self.FINISHED,
                    'start_time': datetime.datetime(2020, 11, 19, 13, 10, 7, 739000),
                    'end_time': datetime.datetime(2020, 11, 19, 13, 10, 57, 812000),
                },
            },
        }

        self.qstat_job_univa = {
            'id': 123456,
            'name': 'feat',
            'sub_time': datetime.datetime.fromtimestamp(1605791398720 / 1000.0),
            'tasks': {
                1: {
                    'status': self.RUNNING,
                    'start_time': datetime.datetime.fromtimestamp(1605791407703 / 1000.0),
                    'end_time': None,
                },
            },
        }
        self.qstat_running_out_univa = (
            '''<?xml version='1.0'?>
<detailed_job_info  xmlns:xsd="http://www.univa.com" '''
            '''xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '''
            '''xsi:schemaLocation="file:///mgmt/uge/8.6.8/util/resources/xsd/qstat/qstat.xsd '''
            '''file:///mgmt/uge/8.6.8/util/resources/xsd/qstat/message.xsd '''
            '''file:///mgmt/uge/8.6.8/util/resources/xsd/qstat/detailed_job_info.xsd">
  <djob_info>
    <element>
      <JB_job_number>123456</JB_job_number>
      <JB_job_name>feat</JB_job_name>
      <JB_version>0</JB_version>
      <JB_project>myproject</JB_project>
      <JB_department>defaultdepartment</JB_department>
      <JB_exec_file>job_scripts/30279117</JB_exec_file>
      <JB_script_file>/tmp/tmprih81yic</JB_script_file>
      <JB_script_size>0</JB_script_size>
      <JB_submission_time>1605791398720</JB_submission_time>
      <JB_execution_time>0</JB_execution_time>
      <JB_deadline>0</JB_deadline>
      <JB_owner>auser</JB_owner>
      <JB_uid>1234</JB_uid>
      <JB_group>agroup</JB_group>
      <JB_gid>123</JB_gid>
      <JB_account>sge</JB_account>
      <JB_cwd>/myfolder</JB_cwd>
      <JB_notify>false</JB_notify>
      <JB_type>0</JB_type>
      <JB_reserve>false</JB_reserve>
      <JB_priority>0</JB_priority>
      <JB_jobshare>0</JB_jobshare>
      <JB_verify>0</JB_verify>
      <JB_checkpoint_attr>0</JB_checkpoint_attr>
      <JB_checkpoint_interval>0</JB_checkpoint_interval>
      <JB_restart>1</JB_restart>
      <JB_merge_stderr>false</JB_merge_stderr>
      <JB_hard_resource_list>
        <element>
          <CE_name>h_vmem</CE_name>
          <CE_valtype>4</CE_valtype>
          <CE_stringval>4.45G</CE_stringval>
          <CE_doubleval>4778151117.000000</CE_doubleval>
          <CE_relop>0</CE_relop>
          <CE_consumable>0</CE_consumable>
          <CE_dominant>0</CE_dominant>
          <CE_pj_doubleval>0.000000</CE_pj_doubleval>
          <CE_pj_fbsb_doubleval>0.000000</CE_pj_fbsb_doubleval>
          <CE_pj_dominant>0</CE_pj_dominant>
          <CE_requestable>0</CE_requestable>
          <CE_tagged>0</CE_tagged>
          <CE_access_specifier>0</CE_access_specifier>
          <CE_available_after_preemption>false</CE_available_after_preemption>
          <CE_tagged_for_deletion>false</CE_tagged_for_deletion>
          <CE_license_usage>0.000000</CE_license_usage>
          <CE_affinity>0.000000</CE_affinity>
        </element>
        <element>
          <CE_name>m_mem_free</CE_name>
          <CE_valtype>4</CE_valtype>
          <CE_stringval>4.45G</CE_stringval>
          <CE_doubleval>4778151117.000000</CE_doubleval>
          <CE_relop>0</CE_relop>
          <CE_consumable>1</CE_consumable>
          <CE_dominant>0</CE_dominant>
          <CE_pj_doubleval>0.000000</CE_pj_doubleval>
          <CE_pj_fbsb_doubleval>0.000000</CE_pj_fbsb_doubleval>
          <CE_pj_dominant>0</CE_pj_dominant>
          <CE_requestable>0</CE_requestable>
          <CE_tagged>0</CE_tagged>
          <CE_access_specifier>0</CE_access_specifier>
          <CE_available_after_preemption>false</CE_available_after_preemption>
          <CE_tagged_for_deletion>false</CE_tagged_for_deletion>
          <CE_license_usage>0.000000</CE_license_usage>
          <CE_affinity>0.000000</CE_affinity>
        </element>
      </JB_hard_resource_list>
      <JB_hard_queue_list>
        <element>
          <QR_name>a.q</QR_name>
          <QR_pos>0</QR_pos>
          <QR_access_specifier>0</QR_access_specifier>
        </element>
      </JB_hard_queue_list>
      <JB_mail_options>0</JB_mail_options>
      <JB_mail_list>
        <element>
          <MR_user>auser</MR_user>
          <MR_host>node1.cluster.com</MR_host>
        </element>
      </JB_mail_list>
      <JB_ja_structure>
        <task_id_range>
          <RN_min>1</RN_min>
          <RN_max>1</RN_max>
          <RN_step>1</RN_step>
        </task_id_range>
      </JB_ja_structure>
      <JB_ja_tasks>
        <element>
          <JAT_task_number>1</JAT_task_number>
          <JAT_status>128</JAT_status>
          <JAT_start_time>1605791407703</JAT_start_time>
          <JAT_hold>0</JAT_hold>
          <JAT_job_restarted>0</JAT_job_restarted>
          <JAT_granted_destin_identifier_list>
            <element>
              <JG_qname>a.qc@node1.cluster.com</JG_qname>
              <JG_qversion>0</JG_qversion>
              <JG_qhostname>node1.cluster.com</JG_qhostname>
              <JG_slots>1</JG_slots>
              <JG_queue></JG_queue>
              <JG_tag_slave_job>0</JG_tag_slave_job>
              <JG_ticket>0.000000</JG_ticket>
              <JG_oticket>0.000000</JG_oticket>
              <JG_fticket>0.000000</JG_fticket>
              <JG_sticket>0.000000</JG_sticket>
              <JG_jcoticket>0.000000</JG_jcoticket>
              <JG_jcfticket>0.000000</JG_jcfticket>
              <JG_binding></JG_binding>
              <JG_resource_map></JG_resource_map>
            </element>
          </JAT_granted_destin_identifier_list>
          <JAT_state>128</JAT_state>
          <JAT_granted_resources_list>
            <grl>
              <GRU_type>4</GRU_type>
              <GRU_name>m_mem_free</GRU_name>
              <GRU_stringval>4.450G</GRU_stringval>
              <GRU_host>node1.cluster.com</GRU_host>
              <GRU_doubleval>4778151117.000000</GRU_doubleval>
            </grl>
          </JAT_granted_resources_list>
          <JAT_granted_request_list>
            <element>
              <CE_name>h_vmem</CE_name>
              <CE_valtype>4</CE_valtype>
              <CE_stringval>4.45G</CE_stringval>
              <CE_doubleval>4778151117.000000</CE_doubleval>
              <CE_relop>0</CE_relop>
              <CE_consumable>0</CE_consumable>
              <CE_dominant>0</CE_dominant>
              <CE_pj_doubleval>0.000000</CE_pj_doubleval>
              <CE_pj_fbsb_doubleval>0.000000</CE_pj_fbsb_doubleval>
              <CE_pj_dominant>0</CE_pj_dominant>
              <CE_requestable>0</CE_requestable>
              <CE_tagged>1</CE_tagged>
              <CE_access_specifier>0</CE_access_specifier>
              <CE_available_after_preemption>false</CE_available_after_preemption>
              <CE_tagged_for_deletion>false</CE_tagged_for_deletion>
              <CE_license_usage>0.000000</CE_license_usage>
              <CE_affinity>0.000000</CE_affinity>
            </element>
            <element>
              <CE_name>m_mem_free</CE_name>
              <CE_valtype>4</CE_valtype>
              <CE_stringval>4.45G</CE_stringval>
              <CE_doubleval>4778151117.000000</CE_doubleval>
              <CE_relop>0</CE_relop>
              <CE_consumable>1</CE_consumable>
              <CE_dominant>0</CE_dominant>
              <CE_pj_doubleval>0.000000</CE_pj_doubleval>
              <CE_pj_fbsb_doubleval>0.000000</CE_pj_fbsb_doubleval>
              <CE_pj_dominant>0</CE_pj_dominant>
              <CE_requestable>0</CE_requestable>
              <CE_tagged>2</CE_tagged>
              <CE_access_specifier>0</CE_access_specifier>
              <CE_available_after_preemption>false</CE_available_after_preemption>
              <CE_tagged_for_deletion>false</CE_tagged_for_deletion>
              <CE_license_usage>0.000000</CE_license_usage>
              <CE_affinity>0.000000</CE_affinity>
            </element>
          </JAT_granted_request_list>
        </element>
      </JB_ja_tasks>
      <JB_verify_suitable_queues>0</JB_verify_suitable_queues>
      <JB_soft_wallclock_gmt>0</JB_soft_wallclock_gmt>
      <JB_hard_wallclock_gmt>0</JB_hard_wallclock_gmt>
      <JB_override_tickets>0</JB_override_tickets>
      <JB_ar>0</JB_ar>
      <JB_ja_task_concurrency>0</JB_ja_task_concurrency>
      <JB_ja_task_concurrency_all>false</JB_ja_task_concurrency_all>
      <JB_binding>
      <BN_hostname></BN_hostname>
      <BN_strategy>no_job_binding</BN_strategy>
      <BN_type>0</BN_type>
      <BN_parameter_n>0</BN_parameter_n>
      <BN_parameter_socket_offset>0</BN_parameter_socket_offset>
      <BN_parameter_core_offset>0</BN_parameter_core_offset>
      <BN_parameter_striding_step_size>0</BN_parameter_striding_step_size>
      <BN_parameter_explicit>no_explicit_binding</BN_parameter_explicit>
      <BN_parameter_nlocal>0</BN_parameter_nlocal>
      <BN_max_slots_qend>0</BN_max_slots_qend>
      </JB_binding>
      <JB_is_binary>false</JB_is_binary>
      <JB_no_shell>false</JB_no_shell>
      <JB_is_array>false</JB_is_array>
      <JB_is_immediate>false</JB_is_immediate>
      <JB_env_list>
        <element>
          <VA_variable>FSLSUB_NSLOTS</VA_variable>
          <VA_value>NSLOTS</VA_value>
          <VA_access_specifier>0</VA_access_specifier>
        </element>
      </JB_env_list>
      <JB_mbind>0</JB_mbind>
      <JB_submission_command_line>
        <element>
          <ST_name>/bin/qsub</ST_name>
          <ST_pos>0</ST_pos>
          <ST_access_specifier>0</ST_access_specifier>
        </element>
        <element>
          <ST_name>/tmp/tmprih81yic</ST_name>
          <ST_pos>0</ST_pos>
          <ST_access_specifier>0</ST_access_specifier>
        </element>
      </JB_submission_command_line>
      <JB_preemption></JB_preemption>
      <JB_supplementary_group_list>
        <element>
          <ST_name>hpcusers</ST_name>
          <ST_pos>0</ST_pos>
          <ST_access_specifier>0</ST_access_specifier>
        </element>
      </JB_supplementary_group_list>
      <JB_category_id>98</JB_category_id>
      <JB_request_dispatch_info>false</JB_request_dispatch_info>
    </element>
  </djob_info>
  <reservations>
  </reservations>
  <messages>
    <element>
      <SME_global_message_list>
        <element>
          <MES_message_number>102</MES_message_number>
          <MES_message>(Collecting of scheduler job information is turned off)</MES_message>
          <MES_count>1</MES_count>
          <MES_total>1</MES_total>
        </element>
      </SME_global_message_list>
      <SME_exceeded>false</SME_exceeded>
    </element>
  </messages>
</detailed_job_info>
'''
        )
        self.qstat_pending_out_univa = (
            '''<?xml version='1.0'?>
<detailed_job_info  xmlns:xsd="http://www.univa.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '''
            '''xsi:schemaLocation="file:///mgmt/uge/8.6.8/util/resources/xsd/qstat/qstat.xsd '''
            '''file:///mgmt/uge/8.6.8/util/resources/xsd/qstat/message.xsd '''
            '''file:///mgmt/uge/8.6.8/util/resources/xsd/qstat/detailed_job_info.xsd">
  <djob_info>
    <element>
      <JB_job_number>123456</JB_job_number>
      <JB_job_name>echo</JB_job_name>
      <JB_version>0</JB_version>
      <JB_project>myproject</JB_project>
      <JB_department>defaultdepartment</JB_department>
      <JB_exec_file>job_scripts/30278963</JB_exec_file>
      <JB_script_file>/tmp/tmpd6hmup3l</JB_script_file>
      <JB_script_size>0</JB_script_size>
      <JB_submission_time>1605791078484</JB_submission_time>
      <JB_execution_time>0</JB_execution_time>
      <JB_deadline>0</JB_deadline>
      <JB_owner>auser</JB_owner>
      <JB_uid>1234</JB_uid>
      <JB_group>agroup</JB_group>
      <JB_gid>123</JB_gid>
      <JB_account>sge</JB_account>
      <JB_cwd>/myfolder</JB_cwd>
      <JB_notify>false</JB_notify>
      <JB_type>0</JB_type>
      <JB_reserve>false</JB_reserve>
      <JB_priority>0</JB_priority>
      <JB_jobshare>0</JB_jobshare>
      <JB_verify>0</JB_verify>
      <JB_checkpoint_attr>0</JB_checkpoint_attr>
      <JB_checkpoint_interval>0</JB_checkpoint_interval>
      <JB_restart>1</JB_restart>
      <JB_merge_stderr>false</JB_merge_stderr>
      <JB_hard_resource_list>
        <element>
          <CE_name>h_vmem</CE_name>
          <CE_valtype>4</CE_valtype>
          <CE_stringval>4.45G</CE_stringval>
          <CE_doubleval>4778151117.000000</CE_doubleval>
          <CE_relop>0</CE_relop>
          <CE_consumable>0</CE_consumable>
          <CE_dominant>0</CE_dominant>
          <CE_pj_doubleval>0.000000</CE_pj_doubleval>
          <CE_pj_fbsb_doubleval>0.000000</CE_pj_fbsb_doubleval>
          <CE_pj_dominant>0</CE_pj_dominant>
          <CE_requestable>0</CE_requestable>
          <CE_tagged>0</CE_tagged>
          <CE_access_specifier>0</CE_access_specifier>
          <CE_available_after_preemption>false</CE_available_after_preemption>
          <CE_tagged_for_deletion>false</CE_tagged_for_deletion>
          <CE_license_usage>0.000000</CE_license_usage>
          <CE_affinity>0.000000</CE_affinity>
        </element>
        <element>
          <CE_name>m_mem_free</CE_name>
          <CE_valtype>4</CE_valtype>
          <CE_stringval>4.45G</CE_stringval>
          <CE_doubleval>4778151117.000000</CE_doubleval>
          <CE_relop>0</CE_relop>
          <CE_consumable>1</CE_consumable>
          <CE_dominant>0</CE_dominant>
          <CE_pj_doubleval>0.000000</CE_pj_doubleval>
          <CE_pj_fbsb_doubleval>0.000000</CE_pj_fbsb_doubleval>
          <CE_pj_dominant>0</CE_pj_dominant>
          <CE_requestable>0</CE_requestable>
          <CE_tagged>0</CE_tagged>
          <CE_access_specifier>0</CE_access_specifier>
          <CE_available_after_preemption>false</CE_available_after_preemption>
          <CE_tagged_for_deletion>false</CE_tagged_for_deletion>
          <CE_license_usage>0.000000</CE_license_usage>
          <CE_affinity>0.000000</CE_affinity>
        </element>
      </JB_hard_resource_list>
      <JB_hard_queue_list>
        <element>
          <QR_name>a.q</QR_name>
          <QR_pos>0</QR_pos>
          <QR_access_specifier>0</QR_access_specifier>
        </element>
      </JB_hard_queue_list>
      <JB_mail_options>0</JB_mail_options>
      <JB_mail_list>
        <element>
          <MR_user>auser</MR_user>
          <MR_host>node1.cluster.com</MR_host>
        </element>
      </JB_mail_list>
      <JB_ja_structure>
        <task_id_range>
          <RN_min>1</RN_min>
          <RN_max>1</RN_max>
          <RN_step>1</RN_step>
        </task_id_range>
      </JB_ja_structure>
      <JB_verify_suitable_queues>0</JB_verify_suitable_queues>
      <JB_soft_wallclock_gmt>0</JB_soft_wallclock_gmt>
      <JB_hard_wallclock_gmt>0</JB_hard_wallclock_gmt>
      <JB_override_tickets>0</JB_override_tickets>
      <JB_ar>0</JB_ar>
      <JB_ja_task_concurrency>0</JB_ja_task_concurrency>
      <JB_ja_task_concurrency_all>false</JB_ja_task_concurrency_all>
      <JB_binding>
      <BN_hostname></BN_hostname>
      <BN_strategy>no_job_binding</BN_strategy>
      <BN_type>0</BN_type>
      <BN_parameter_n>0</BN_parameter_n>
      <BN_parameter_socket_offset>0</BN_parameter_socket_offset>
      <BN_parameter_core_offset>0</BN_parameter_core_offset>
      <BN_parameter_striding_step_size>0</BN_parameter_striding_step_size>
      <BN_parameter_explicit>no_explicit_binding</BN_parameter_explicit>
      <BN_parameter_nlocal>0</BN_parameter_nlocal>
      <BN_max_slots_qend>0</BN_max_slots_qend>
      </JB_binding>
      <JB_is_binary>false</JB_is_binary>
      <JB_no_shell>false</JB_no_shell>
      <JB_is_array>false</JB_is_array>
      <JB_is_immediate>false</JB_is_immediate>
      <JB_env_list>
        <element>
          <VA_variable>FSLSUB_NSLOTS</VA_variable>
          <VA_value>NSLOTS</VA_value>
          <VA_access_specifier>0</VA_access_specifier>
        </element>
      </JB_env_list>
      <JB_mbind>0</JB_mbind>
      <JB_submission_command_line>
        <element>
          <ST_name>/bin/qsub</ST_name>
          <ST_pos>0</ST_pos>
          <ST_access_specifier>0</ST_access_specifier>
        </element>
        <element>
          <ST_name>/tmp/tmpd6hmup3l</ST_name>
          <ST_pos>0</ST_pos>
          <ST_access_specifier>0</ST_access_specifier>
        </element>
      </JB_submission_command_line>
      <JB_preemption></JB_preemption>
      <JB_supplementary_group_list>
        <element>
          <ST_name>hpcusers</ST_name>
          <ST_pos>0</ST_pos>
          <ST_access_specifier>0</ST_access_specifier>
        </element>
      </JB_supplementary_group_list>
      <JB_category_id>91</JB_category_id>
      <JB_request_dispatch_info>false</JB_request_dispatch_info>
    </element>
  </djob_info>
  <reservations>
  </reservations>
  <messages>
    <element>
      <SME_global_message_list>
        <element>
          <MES_message_number>102</MES_message_number>
          <MES_message>(Collecting of scheduler job information is turned off)</MES_message>
          <MES_count>1</MES_count>
          <MES_total>1</MES_total>
        </element>
      </SME_global_message_list>
      <SME_exceeded>false</SME_exceeded>
    </element>
  </messages>
</detailed_job_info>
'''
        )
        self.qstat_out = (
            '''<?xml version='1.0'?>
<detailed_job_info  xmlns:xsd="http://arc.liv.ac.uk/repos/darcs/'''
            '''sge/source/dist/util/resources/schemas/qstat/detailed_job_info.xsd">
  <djob_info>
    <element>
      <JB_job_number>123456</JB_job_number>
      <JB_ar>0</JB_ar>
      <JB_exec_file>job_scripts/9983604</JB_exec_file>
      <JB_submission_time>1603383001</JB_submission_time>
      <JB_owner>auser</JB_owner>
      <JB_uid>9041</JB_uid>
      <JB_group>agroup</JB_group>
      <JB_gid>8540</JB_gid>
      <JB_account>sge</JB_account>
      <JB_merge_stderr>false</JB_merge_stderr>
      <JB_mail_list>
        <mail_list>
          <MR_user>auser</MR_user>
          <MR_host>host1.com</MR_host>
        </mail_list>
      </JB_mail_list>
      <JB_notify>false</JB_notify>
      <JB_job_name>feat</JB_job_name>
      <JB_jobshare>0</JB_jobshare>
      <JB_hard_queue_list>
        <destin_ident_list>
          <QR_name>long.q</QR_name>
        </destin_ident_list>
      </JB_hard_queue_list>
      <JB_env_list>
         <job_sublist>
          <VA_variable>SHELL</VA_variable>
          <VA_value>/bin/bash</VA_value>
        </job_sublist>
      </JB_env_list>
      <JB_job_args>
        <element>
          <ST_name>myfeat.fsf</ST_name>
        </element>
      </JB_job_args>
      <JB_script_file>feat</JB_script_file>
      <JB_ja_tasks>
        <ulong_sublist>
          <JAT_status>128</JAT_status>
          <JAT_task_number>1</JAT_task_number>
          <JAT_scaled_usage_list>
            <scaled>
              <UA_name>binding_inuse!ScttCTTCTTCTTCTTCTTCTTCTTCTTCTTSCTTCTTCTTCTTCTTCTTCTTCTTCTTCTT</UA_name>
              <UA_value>0.000000</UA_value>
            </scaled>
            <scaled>
              <UA_name>cpu</UA_name>
              <UA_value>1610382.910000</UA_value>
            </scaled>
            <scaled>
              <UA_name>mem</UA_name>
              <UA_value>635938.397043</UA_value>
            </scaled>
            <scaled>
              <UA_name>io</UA_name>
              <UA_value>890.191006</UA_value>
            </scaled>
            <scaled>
              <UA_name>iow</UA_name>
              <UA_value>0.000000</UA_value>
            </scaled>
            <scaled>
              <UA_name>vmem</UA_name>
              <UA_value>458420224.000000</UA_value>
            </scaled>
            <scaled>
              <UA_name>maxvmem</UA_name>
              <UA_value>8521097216.000000</UA_value>
            </scaled>
          </JAT_scaled_usage_list>
          <JAT_start_time>1603383003</JAT_start_time>
          <JAT_ntix>0.062768</JAT_ntix>
        </ulong_sublist>
      </JB_ja_tasks>
      <JB_cwd>/path/to/workdir</JB_cwd>
      <JB_deadline>0</JB_deadline>
      <JB_execution_time>0</JB_execution_time>
      <JB_checkpoint_attr>0</JB_checkpoint_attr>
      <JB_checkpoint_interval>0</JB_checkpoint_interval>
      <JB_reserve>false</JB_reserve>
      <JB_mail_options>262144</JB_mail_options>
      <JB_priority>1024</JB_priority>
      <JB_restart>1</JB_restart>
      <JB_verify>0</JB_verify>
      <JB_script_size>0</JB_script_size>
      <JB_verify_suitable_queues>0</JB_verify_suitable_queues>
      <JB_soft_wallclock_gmt>0</JB_soft_wallclock_gmt>
      <JB_hard_wallclock_gmt>0</JB_hard_wallclock_gmt>
      <JB_override_tickets>0</JB_override_tickets>
      <JB_version>0</JB_version>
      <JB_ja_structure>
        <task_id_range>
          <RN_min>1</RN_min>
          <RN_max>1</RN_max>
          <RN_step>1</RN_step>
        </task_id_range>
      </JB_ja_structure>
      <JB_type>320</JB_type>
      <JB_binding>
        <binding>
          <BN_strategy>linear_automatic</BN_strategy>
          <BN_type>3</BN_type>
          <BN_parameter_n>2147483647</BN_parameter_n>
          <BN_parameter_socket_offset>0</BN_parameter_socket_offset>
          <BN_parameter_core_offset>0</BN_parameter_core_offset>
          <BN_parameter_striding_step_size>0</BN_parameter_striding_step_size>
        </binding>
      </JB_binding>
      <JB_ja_task_concurrency>0</JB_ja_task_concurrency>
      <JB_nurg>1.000000</JB_nurg>
    </element>
  </djob_info>
  <messages>
    <element>
      <SME_global_message_list>
        <element>
          <MES_message_number>1</MES_message_number>
          <MES_message>queue instance &quot;long.q@host1.com&quot; dropped because it is full</MES_message>
        </element>
      </SME_global_message_list>
    </element>
  </messages>
</detailed_job_info>
''')
        self.expected_keys = [
            'id', 'name', 'sub_time', 'tasks',
        ]
        self.expected_keys.sort()

        self.task_expected_keys = [
            'status', 'start_time', 'end_time', ]
        self.task_expected_keys.sort()
        self.qstat_no_job = '''<?xml version='1.0'?>
<unknown_jobs >
    <ST_name>12345</ST_name>
</unknown_jobs>
'''
        self.qstat_no_job_univa = (
            '''<?xml version='1.0'?>
<unknown_jobs  xmlns:xsd="http://www.univa.com" '''
            '''xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '''
            '''xsi:schemaLocation="file:///mgmt/uge/8.6.8/util/resources/xsd/qstat/qstat.xsd '''
            '''file:///mgmt/uge/8.6.8/util/resources/xsd/qstat/message.xsd '''
            '''file:///mgmt/uge/8.6.8/util/resources/xsd/qstat/detailed_job_info.xsd">
  <element>
    <ST_name>1234</ST_name>
    <ST_pos>0</ST_pos>
    <ST_access_specifier>0</ST_access_specifier>
  </element>
</unknown_jobs>
'''
        )

    @patch('fsl_sub_plugin_sge.qstat_cmd', return_value='/usr/bin/qstat')
    @patch('fsl_sub_plugin_sge.qacct_cmd', return_value='/usr/bin/qacct')
    def test_job_status_keys(self, mock_qacct, mock_qs):
        self.maxDiff = None
        with self.subTest("Completed - SGE"):
            with patch('fsl_sub_plugin_sge.sp.run', autospec=True) as mock_sprun:
                mock_sprun.side_effect = (
                    subprocess.CompletedProcess(
                        ['qstat'], 0, self.qstat_no_job, ''),
                    subprocess.CompletedProcess(
                        ['qacct'], 0, self.qacct_out, '')
                )
                job_stat = fsl_sub_plugin_sge.job_status(123456)
            output_keys = list(job_stat.keys())
            output_keys.sort()
            self.assertListEqual(output_keys, self.expected_keys)
            task_output_keys = list(job_stat['tasks'][1].keys())
            task_output_keys.sort()
            self.assertListEqual(task_output_keys, self.task_expected_keys)
            self.assertDictEqual(job_stat, self.qacct_job)

        with self.subTest("Running - SGE"):
            with patch('fsl_sub_plugin_sge.sp.run', autospec=True) as mock_sprun:
                mock_sprun.side_effect = (
                    subprocess.CompletedProcess(
                        ['qstat'], 0, self.qstat_out, ''),
                    subprocess.CalledProcessError(
                        1, 'qacct', stderr="error: job id 123456 not found\n")
                )
                job_stat = fsl_sub_plugin_sge.job_status(123456)
            output_keys = list(job_stat.keys())
            output_keys.sort()
            self.assertListEqual(output_keys, self.expected_keys)
            task_output_keys = list(job_stat['tasks'][1].keys())
            task_output_keys.sort()
            self.assertListEqual(task_output_keys, self.task_expected_keys)
            self.assertDictEqual(job_stat, self.qstat_job)

        with self.subTest("Completed - Univa"):
            with patch('fsl_sub_plugin_sge.sp.run', autospec=True) as mock_sprun:
                mock_sprun.side_effect = (
                    subprocess.CompletedProcess(
                        ['qstat'], 0, self.qstat_no_job_univa, ''),
                    subprocess.CompletedProcess(
                        ['qacct'], 0, self.qacct_out_univa, '')
                )
                job_stat = fsl_sub_plugin_sge.job_status(123456)
            output_keys = list(job_stat.keys())
            output_keys.sort()
            self.assertListEqual(output_keys, self.expected_keys)
            task_output_keys = list(job_stat['tasks'][1].keys())
            task_output_keys.sort()
            self.assertListEqual(task_output_keys, self.task_expected_keys)
            self.assertDictEqual(job_stat, self.qacct_job_univa)

        with self.subTest("Running - Univa"):
            with patch('fsl_sub_plugin_sge.sp.run', autospec=True) as mock_sprun:
                mock_sprun.side_effect = (
                    subprocess.CompletedProcess(
                        ['qstat'], 0, self.qstat_running_out_univa, ''),
                    subprocess.CalledProcessError(
                        1, 'qacct', stderr="error: job id 123456 not found\n")
                )
                job_stat = fsl_sub_plugin_sge.job_status(123456)
            output_keys = list(job_stat.keys())
            output_keys.sort()
            self.assertListEqual(output_keys, self.expected_keys)
            task_output_keys = list(job_stat['tasks'][1].keys())
            task_output_keys.sort()
            self.assertListEqual(task_output_keys, self.task_expected_keys)
            self.assertDictEqual(job_stat, self.qstat_job_univa)


class TestQueueCapture(unittest.TestCase):
    def setUp(self):
        self.qhost_q_xml_single_host = '''<?xml version='1.0'?>
<qhost xmlns:xsd="http://arc.liv.ac.uk/repos/darcs/sge/source/dist/util/resources/schemas/qhost/qhost.xsd">
 <host name='global'>
   <hostvalue name='arch_string'>-</hostvalue>
   <hostvalue name='num_proc'>-</hostvalue>
   <hostvalue name='m_socket'>-</hostvalue>
   <hostvalue name='m_core'>-</hostvalue>
   <hostvalue name='m_thread'>-</hostvalue>
   <hostvalue name='load_avg'>-</hostvalue>
   <hostvalue name='mem_total'>-</hostvalue>
   <hostvalue name='mem_used'>-</hostvalue>
   <hostvalue name='swap_total'>-</hostvalue>
   <hostvalue name='swap_used'>-</hostvalue>
 </host>
 <host name='host1.cluster'>
   <hostvalue name='arch_string'>lx-amd64</hostvalue>
   <hostvalue name='num_proc'>8</hostvalue>
   <hostvalue name='m_socket'>2</hostvalue>
   <hostvalue name='m_core'>8</hostvalue>
   <hostvalue name='m_thread'>8</hostvalue>
   <hostvalue name='load_avg'>-</hostvalue>
   <hostvalue name='mem_total'>100G</hostvalue>
   <hostvalue name='mem_used'>-</hostvalue>
   <hostvalue name='swap_total'>5G</hostvalue>
   <hostvalue name='swap_used'>-</hostvalue>
 <queue name='a.q'>
   <queuevalue qname='a.q' name='qtype_string'>BP</queuevalue>
   <queuevalue qname='a.q' name='slots_used'>2</queuevalue>
   <queuevalue qname='a.q' name='slots'>2</queuevalue>
   <queuevalue qname='a.q' name='slots_resv'>0</queuevalue>
   <queuevalue qname='a.q' name='state_string'></queuevalue>
 </queue>
 </host>
</qhost>
'''
        self.qhost_q_xml_two_host = '''<?xml version='1.0'?>
<qhost xmlns:xsd="http://arc.liv.ac.uk/repos/darcs/sge/source/dist/util/resources/schemas/qhost/qhost.xsd">
 <host name='global'>
   <hostvalue name='arch_string'>-</hostvalue>
   <hostvalue name='num_proc'>-</hostvalue>
   <hostvalue name='m_socket'>-</hostvalue>
   <hostvalue name='m_core'>-</hostvalue>
   <hostvalue name='m_thread'>-</hostvalue>
   <hostvalue name='load_avg'>-</hostvalue>
   <hostvalue name='mem_total'>-</hostvalue>
   <hostvalue name='mem_used'>-</hostvalue>
   <hostvalue name='swap_total'>-</hostvalue>
   <hostvalue name='swap_used'>-</hostvalue>
 </host>
 <host name='host1.cluster'>
   <hostvalue name='arch_string'>lx-amd64</hostvalue>
   <hostvalue name='num_proc'>8</hostvalue>
   <hostvalue name='m_socket'>2</hostvalue>
   <hostvalue name='m_core'>8</hostvalue>
   <hostvalue name='m_thread'>8</hostvalue>
   <hostvalue name='load_avg'>-</hostvalue>
   <hostvalue name='mem_total'>100G</hostvalue>
   <hostvalue name='mem_used'>-</hostvalue>
   <hostvalue name='swap_total'>5G</hostvalue>
   <hostvalue name='swap_used'>-</hostvalue>
 <queue name='a.q'>
   <queuevalue qname='a.q' name='qtype_string'>BP</queuevalue>
   <queuevalue qname='a.q' name='slots_used'>2</queuevalue>
   <queuevalue qname='a.q' name='slots'>2</queuevalue>
   <queuevalue qname='a.q' name='slots_resv'>0</queuevalue>
   <queuevalue qname='a.q' name='state_string'></queuevalue>
 </queue>
 </host>
 <host name='host2.cluster'>
   <hostvalue name='arch_string'>lx-amd64</hostvalue>
   <hostvalue name='num_proc'>16</hostvalue>
   <hostvalue name='m_socket'>2</hostvalue>
   <hostvalue name='m_core'>16</hostvalue>
   <hostvalue name='m_thread'>16</hostvalue>
   <hostvalue name='load_avg'>-</hostvalue>
   <hostvalue name='mem_total'>200G</hostvalue>
   <hostvalue name='mem_used'>-</hostvalue>
   <hostvalue name='swap_total'>5G</hostvalue>
   <hostvalue name='swap_used'>-</hostvalue>
 <queue name='a.q'>
   <queuevalue qname='a.q' name='qtype_string'>BP</queuevalue>
   <queuevalue qname='a.q' name='slots_used'>2</queuevalue>
   <queuevalue qname='a.q' name='slots'>4</queuevalue>
   <queuevalue qname='a.q' name='slots_resv'>0</queuevalue>
   <queuevalue qname='a.q' name='state_string'></queuevalue>
 </queue>
 </host>
</qhost>
'''
        self.qconf_sq_aq_one_host = '''qname                 a.q
hostlist              @lx64
seq_no                0
load_thresholds       np_load_avg=1.75
suspend_thresholds    NONE
nsuspend              1
suspend_interval      00:05:00
priority              0
min_cpu_interval      00:05:00
processors            UNDEFINED,[host1.cluster=8],[host2.cluster=16]
qtype                 BATCH
ckpt_list             NONE
pe_list               make openmp
rerun                 TRUE
slots                 0,[host1.cluster=2]
tmpdir                /tmp
shell                 /bin/sh
prolog                NONE
epilog                NONE
shell_start_mode      unix_behavior
starter_method        NONE
suspend_method        NONE
resume_method         NONE
terminate_method      NONE
notify                00:00:60
owner_list            NONE
user_lists            NONE
xuser_lists           NONE
subordinate_list      NONE
complex_values        NONE
projects              NONE
xprojects             NONE
calendar              NONE
initial_state         default
s_rt                  INFINITY
h_rt                  INFINITY
s_cpu                 04:00:00
h_cpu                 04:00:00
s_fsize               INFINITY
h_fsize               INFINITY
s_data                INFINITY
h_data                INFINITY
s_stack               INFINITY
h_stack               INFINITY
s_core                INFINITY
h_core                INFINITY
s_rss                 INFINITY
h_rss                 INFINITY
s_vmem                INFINITY
h_vmem                INFINITY
'''
        self.qconf_sq_aq_two_host = '''qname                 a.q
hostlist              @lx64
seq_no                0
load_thresholds       np_load_avg=1.75
suspend_thresholds    NONE
nsuspend              1
suspend_interval      00:05:00
priority              0
min_cpu_interval      00:05:00
processors            UNDEFINED,[host1.cluster=8],[host2.cluster=16]
qtype                 BATCH
ckpt_list             NONE
pe_list               make openmp
rerun                 TRUE
slots                 0,[host1.cluster=2],[host2.cluster=4]
tmpdir                /tmp
shell                 /bin/sh
prolog                NONE
epilog                NONE
shell_start_mode      unix_behavior
starter_method        NONE
suspend_method        NONE
resume_method         NONE
terminate_method      NONE
notify                00:00:60
owner_list            NONE
user_lists            NONE
xuser_lists           NONE
subordinate_list      NONE
complex_values        NONE
projects              NONE
xprojects             NONE
calendar              NONE
initial_state         default
s_rt                  INFINITY
h_rt                  INFINITY
s_cpu                 04:00:00
h_cpu                 04:00:00
s_fsize               INFINITY
h_fsize               INFINITY
s_data                INFINITY
h_data                INFINITY
s_stack               INFINITY
h_stack               INFINITY
s_core                INFINITY
h_core                INFINITY
s_rss                 INFINITY
h_rss                 INFINITY
s_vmem                INFINITY
h_vmem                INFINITY
'''
        self.qconf_sql = '''a.q\n'''

    @patch('fsl_sub_plugin_sge.qconf_cmd', return_value='/usr/bin/qconf')
    @patch('fsl_sub_plugin_sge.qhost_cmd', return_value='/usr/bin/qhost')
    @patch('fsl_sub_plugin_sge.method_config', return_value=conf_dict['method_opts']['sge'])
    def test_build_queue_defs(self, mock_mconf, mock_qhost, mock_qconf):
        with patch('fsl_sub_plugin_sge.sp.run') as mock_spr:
            mock_spr.side_effect = (
                subprocess.CompletedProcess(
                    ['qconf', '-sql', ], 0, self.qconf_sql
                ),
                subprocess.CompletedProcess(
                    ['qhost', '-q', '-xml', ], 0, self.qhost_q_xml_single_host
                ),
                subprocess.CompletedProcess(
                    ['qconf', '-sq', 'a.q', ], 0, self.qconf_sq_aq_one_host
                )
            )
            qdefs = fsl_sub_plugin_sge.build_queue_defs()
            yaml = YAML()
            yaml.width = 128
        expected_yaml = yaml.load('''queues:
  a.q: # Queue name
  # Queue has no h_vmem or h_rss specified, slot_size calculated with max_size divided by slots.
  # default: true # Is this the default partition?
  # priority: 1 # Priority in group - higher wins
  # group: 1 # Group partitions with the same integer then order by priority
  # For co-processor queues you need the following:
  # copros:
  #   cuda: # CUDA Co-processor available
  #     max_quantity: # Maximum available per node
  #     classes: # List of classes (if classes supported)
  #     exclusive: False # Does this only run jobs requiring this co-processor?
    time: 240 # Maximum job run time in minutes
    parallel_envs: # Parallel environments configured on this queue
      - make
      - openmp
    max_slots: 2 # Maximum number of threads/slots on a queue
    max_size: 100 # Maximum RAM size of a job
    slot_size: 50 # Maximum memory per thread
    map_ram: true # Whether this queue should automatically split jobs into multiple threads to support RAM request
''')
        qd_str = io.StringIO()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump(qdefs, qd_str)
        eq_str = io.StringIO()
        yaml.dump(expected_yaml, eq_str)
        self.maxDiff = None
        self.assertEqual(qd_str.getvalue(), eq_str.getvalue())
        with self.subTest("Two hosts"):
            with patch('fsl_sub_plugin_sge.sp.run') as mock_spr:
                mock_spr.side_effect = (
                    subprocess.CompletedProcess(
                        ['qconf', '-sql', ], 0, self.qconf_sql
                    ),
                    subprocess.CompletedProcess(
                        ['qhost', '-q', '-xml', ], 0, self.qhost_q_xml_two_host
                    ),
                    subprocess.CompletedProcess(
                        ['qconf', '-sq', 'a.q', ], 0, self.qconf_sq_aq_two_host
                    )
                )
                qdefs = fsl_sub_plugin_sge.build_queue_defs()
                yaml = YAML()
                yaml.width = 128
            expected_yaml = yaml.load(
                '''queues:
  a.q: # Queue name
  # Queue has hosts of different total memory size, consider creating multiple queues for the different '''
                + '''host hardware in Grid Engine and then set the same 'group' integer to allow fsl_sub to '''
                + '''maximise hardware your job can run on. '''
                + '''Alternatively consider turning on notify_ram_usage.
  # Queue has no h_vmem or h_rss specified, slot_size calculated with max_size divided by slots.
  # Queue has multiple slot sizes - this calculation will not be correct for all hosts.
  # default: true # Is this the default partition?
  # priority: 1 # Priority in group - higher wins
  # group: 1 # Group partitions with the same integer then order by priority
  # For co-processor queues you need the following:
  # copros:
  #   cuda: # CUDA Co-processor available
  #     max_quantity: # Maximum available per node
  #     classes: # List of classes (if classes supported)
  #     exclusive: False # Does this only run jobs requiring this co-processor?
    time: 240 # Maximum job run time in minutes
    parallel_envs: # Parallel environments configured on this queue
      - make
      - openmp
    max_slots: 4 # Maximum number of threads/slots on a queue
    max_size: 200 # Maximum RAM size of a job
    slot_size: 50 # Maximum memory per thread
    map_ram: true # Whether this queue should automatically split jobs into multiple threads to support RAM request
''')
            qd_str = io.StringIO()
            yaml.indent(mapping=2, sequence=4, offset=2)
            yaml.dump(qdefs, qd_str)
            eq_str = io.StringIO()
            yaml.dump(expected_yaml, eq_str)
            self.maxDiff = None
            self.assertEqual(qd_str.getvalue(), eq_str.getvalue())


if __name__ == '__main__':
    unittest.main()
