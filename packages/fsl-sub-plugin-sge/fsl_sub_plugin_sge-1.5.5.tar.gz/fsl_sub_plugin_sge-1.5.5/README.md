# fsl\_sub\_plugin\_sge

Job submission to Grid Engine variant cluster queues.
_Copyright 2018-2020, University of Oxford (Duncan Mortimer)_

## Introduction

fsl\_sub provides a consistent interface to various cluster backends, with a fall back to running tasks locally where no cluster is available.
This fsl\_sub plugin provides support for submitting tasks to Sun/Son of/Univa Grid Engine (Grid Engine) clusters.

For installation instructions please see `INSTALL.md`; for building packages see `BUILD.md`.

## Configuration

Use the command:

> fsl_sub_config sge > fsl_sub.yml

to generate an example configuration, including queue definitions gleaned from the Grid Engine software - check these, paying attention to any warnings generated.

Use the `fsl_sub.yml` file as per the main fsl_sub documentation.

The configuration for the Grid Engine plugin is in the _method\_opts_ section, under the key _sge_.

### Method options

| Key | Values (default/recommended in bold) | Description |
| ----|--------|-------------|
| queues | **True** | Does this method use queues/partitions (should be always be True) |
| large\_job\_split\_pe | _parallel environment name_ | Name of a _parallel environment_ should be used to break up large memory jobs. |
| copy\_environment | **True**/False | Whether to replicate the environment variables in the shell that called fsl_sub into the job's shell. |
| has\_parallel_envs | **True**/False | Whether to enable support for parallel environments, this should usually be left as True. |
| affinity\_type | Null/**linear** | whether to lock jobs to CPU cores (soft-enforces a maximum number of threads for a job) and what core spread should Grid Engine use, see _man qsub_ for options. _None_ disabled locking and typically _linear_ is the correct mechanism to use when this is switched on. |
| affinity\_control | **threads**/slots | Typically set to _threads_, _slots_ may be specified for Son of Grid Engine (SGE) (but not on UGE). This controls how the bound cores will be specified. SGE uses 'slots' to automatically calculate this based on the number of slots requested for the job on the node running the job thus catering for heterogenous clusters. |
| script\_conf | **True**/False | Whether _--usesscript_ option to fsl_sub is available via this method. This option allows you to define the grid options as comments in a shell script and then provide this to the cluster for running. Should be set to True. |
| mail\_support | True/**False** | Whether the grid installation is configured to send email on job events. |
| mail\_modes | Dictionary of option lists | If the grid has email notifications turned on, this option configures the submission options for different verbosity levels, 'b' = job start, 'e' = job end, 'a' = job abort, 'f' = all events, 'n' = no mail. Each event type should then have a list of submission mail arguments that will be applied to the submitted job. Typically, these should not be edited. |
| mail\_mode | b/e/a/f/**n** | Which of the above mail_modes to use by default. |
| map\_ram| **True**/False | If a job requests more RAM than is available in any one queue whether fsl\_sub should request a parallel environment with sufficient slots to achieve this memory request, e.g. if your maximum slot size is 16GB and you request 64GB if this option is on then fsl\_sub will request the parallel environment specified in _large\_job\_split\_pe_ be setup with four slots. As a side-effect your job will now be free to use four threads. |
| thread\_ram_divide | **True** | If you have requested a multi-threaded job, does your grid software expect you to specify the appropriate fraction of the total memory required (True) or the total memory of the task (False). For Grid Engine this should be left at True. |
| notify\_ram\_usage | True/**False** | Whether to notify Grid Engine of the RAM you have requested. Advising the grid software of your RAM requirements can help with scheduling or may be used for special features (such as RAM disks). Use this to control whether fsl_sub passes on your RAM request to the grid scheduler. |
| set\_time\_limit | True/**False** | Whether to notify Grid Engine of the expected **maximum** run-time of your job. This helps the scheduler fill in reserved slots (for e.g. parallel environment jobs), however, this time limit will be enforced, resulting in a job being killed if it is exceeded, even if this is less than the queue run-time limit. This can be disabled on a per-job basis by setting the environment variable FSLSUB_NOTIMELIMIT to '1' (or 'True'). |
| set\_hard\_time | True/**False** | Whether to automatically specify the queue's hard run-time limit for the job if _set\_time\_limit_ is not set. Also helps with filling reserved slots. This can be disabled on a per-job basis by setting the environment variable FSLSUB_NOTIMELIMIT to '1' (or 'True'). |
| ram\_resources | resource name list | This is a list of the grid resource variables to be defined with notifying the grid scheduler of your RAM requirements. The defaults are typically correct for U/SGE. |
| job\_priorities | **True**/False | Enable job priority support. |
| min\_priority | (a signed integer) | What is the minimum priority a user can request, -1023 is the correct figure on U/SGE. |
| max\_priority | (a signed integer) | What is the maximum priority a user can request, 0 is the correct figure on U/SGE. |
| array\_holds | **True**/False | Enable support array holds, e.g. sub-task 1 waits for parent sub-task 1. |
| array\_limit | **True**/False | Enable limiting number of concurrent array tasks. |
| architecture | True/**False** | Is there more than one architecture available on the cluster? Usually False. |
| job\_resources | **True**/False | Enable additional job resource specification support. |
| projects | **True**/False | Enable support for projects typically used auditing/charging purposes. |
| preseve\_modules | True/**False** | Requires (and will enforce) use_jobscript. Whether to re-load shell modules on the compute node. Required if you have multiple CPU generations and per-generation optimised libraries configured with modules. |
| add_module_paths | **[]**/ a list | List of file system paths to search for modules in addition to the system defined ones. Useful if you have your own shell modules directory but need to allow the compute node to auto-set it's MODULEPATH environment variable (e.g. to a architecture specific folder). Only used when preserve_modules is True. |
| export\_vars | **[]**/List | List of environment variables that should transfered with the job to the compute node. |
| use\_jobscript | **True**/False | Create a Grid Engine job description script rather than setting job options on the command line. Necessary where the environment can't be fully copied to a running job. |
| keep\_jobscript | True/**False** | Whether to preserve the generated wrapper in a file `jobid_wrapper.sh`. This file contains sufficient information to resubmit this job in the future. |
| extra\_args | **[]**/List | List of additional Grid Engine arguments to pass through to the sheduler. |
| allow_nested_queuing | True/**False** | Whether fsl_sub, when called from within a cluster job, should be able to submit further jobs (True) or run subsequent jobs with the shell plugin. You can override this on a per-job or session basis using the environmet  |

### Coprocessor Configuration

This plugin is not capable of automatically determining the necessary information to configure your co-processors. In the case of Grid Engine the most useful output is that given by `qconf -sc <hostname>`. In this output look for somthing that indicates a co-processor resource, e.g. _gpu_. Also look for something that might be used to select between different versions of the co-processor, e.g. _gpu\_type_.

For each coprocessor hardware type you need a sub-section given an identifier than will be used to request this type of coprocessor. For CUDA processors this sub-section **must** be called 'cuda' to ensure that FSL tools can auto-detect and use CUDA hardware/queues.

| Key | Values (default/recommended in bold) | Description |
| ----|--------|-------------|
| resource| String | Grid resource that, when requested, selects machines with the hardware present, e.g. _gpu_. Look in the output of `qconf -sc <hostname>`. |
| uses_pe | String/**False** | Name of Parallel Environment - SGE doesn't support GPUs natively and so it is common to use a prolog script to assign GPUs to tasks. These scripts are typically configured to request a number of GPUs equal to the slots in a parallel environment. If your cluster is set up like this, change this to the name of the parallel environment to use. If you haven't requested one specifically it will then submit the job to this PE. Leave as False for clusters that support GPUs natively, e.g. Univa Grid Engine. |
| classes | True/**False** | Whether more than one type of this co-processor is available. |
| include\_more_capable | **True**/False | Whether to automatically request all classes that are more capable than the requested class. |
| class\_types | Configuration dictionary | This contains the definition of the GPU classes... |
| | _Key_ | |
| | class selector | This is the letter (or word) that is used to select this class of co-processor from the fsl\_sub commandline. For CUDA devices you may consider using the card name e.g. A100. |
| | resource | This is the name of the Grid Engine 'complex' that will be used to select this GPU family, you can look for possible values with `qconf -sc <hostname>` (it's normally _gputype_). |
| | doc | The description that appears in the fsl\_sub help text about this device. |
| | capability | An integer defining the feature set of the device, your most basic device should be given the value 1 and more capable devices higher values, e.g. GTX = 1, Kelper = 2, Pascal = 3, Volta = 4. |
| default\_class | _Class type key_ | The _class selector_ for the class to assign jobs to where a class has not been specified in the fsl\_sub call. For FSL tools that automatically submit to CUDA queues you should aim to select one that has good double-precision performance (K40\|80, P100, V100, A100) and ensure all higher capability devices also have good double-precision. |
| no_binding | **True**/False | Where the grid software supports CPU core binding fsl\_sub will attempt to prevent tasks using more than the requested number of cores. This option allows you to override this setting when submitting coprocessor tasks as these machines often have signifcantly more CPU cores than GPU cores. |
| set_visible | True/**False** | Whether to set CUDA_VISIBLE_DEVICES and GPU_DEVICE_ORDINAL automatically based on the Univa Grid Engine SGE_HGR_gpu variable. Only supported on Univa Grid Engine and may not be necessary if the cluster administrator has ensured this is set automatically. |
| presence\_test | _Program path_ (**nvidia-smi** for CUDA) | The name of a program that can be used to look for this coprocessor type, for example nvidia-smi for CUDA devices. Program needs to return non-zero exit status if there are no available coprocessors. |

### Queue Definitions

The example configuration should include automatically discovered queue definitions, these should be reviewed, especially any warnings included.
If the auto-discovery fails you can get a list of all available queues use:

> qconf -sql

Then the details for a queue can be obtained with:

> qconf -sq _qname_

Any queue that doesn't have a _qtype_ of _BATCH_ should be ignored for the purposes of configuring fsl_sub.

The queue definition 'key' is the name of the queue and has the following properties:

| Key | Values (default/recommended in bold) | Description |
| ----|--------|-------------|
| time | _time in minutes_ | Maximum runtime for a job on this queue (may be wall or CPU time depending on your cluster setup). This is given by _s\_rt_ (wall time) or _h\_cpu_ (CPU time) in the `qconf -sq \<queue name>` output in the form hours:minutes:seconds. |
| max\_size | _memory_ | The units for this are defined in the main fsl\_sub configuration. This is the maximum amount of memory a single job is likely to be able to request. The output of `qhost` will give an indication as to what this might be - identify the hosts in this queue and then find the highest figure in the _MEMTOT_ column. It is usually best to take 2-4GB off this figure to allow for OS operations. |
| slot\_size | _memory_ | The units for this are defined in the main fsl\_sub configuration. This is equivalent to _h\_vmem_ in `qconf` output, converted to units specified. |
| max\_slots | _slots_ | This is the maximum number of slots (and thus threads) available per node in this queue. In the `qconf -sq` output, this is the maximum number reported in the host/group list, e.g. [@lx64_20HT=20],[@lx64_28HT=28] means max_slots should be 28. |
| map_ram | True/False | Whether to automatically submit large jobs into at parallel environment with sufficient threads to achieve the memory requested. |
| parallel\_envs | _List of PE names_ | The list of parallel environments available in this queue. Find these in _pe\_list_ of `qconf -sq`. Where this differs between hosts this may take the form of a list of host/group definitions, e.g. [@lx64_8=openmp ramdisk], include all found. |
| priority | _integer_ | Order of wpecifies an order for queues within a group, smaller = higher priority. |
| group | _integer_ | An integer that allows grouping similar queues together, all queues in the same group will be candidates for a job that matches their capabilities. |
| default | True | Add to the queue that jobs should be submitted to if no queue, RAM or time information is given. |
| copros | _Co-processor dictionary_ | _Optional_ If this queue has hosts with co-processors (e.g. CUDA devices), then provide this entry, with a key identical to the associated co-processor definition, e.g. _cuda_. Options are: |
| | max\_quantity | An integer representing the maximum number of this coprocessor type available on a single compute node. This can be obtained by looking at the _complexes_ entry of `qconf -se <hostname>` for all of the hosts in this queue. If the complex is _gpu_ then an entry of _gpu=2_ would indicated that this value should be set to 2. |
| | classes | A list of coprocessor classes (as defined in the coprocessor configuration section) that this queue has hardware for. |
| | exclusive | True/**False** - Whether this queue is only used for co-processor requiring tasks.|

#### Compound Queues

Some clusters may be configured with multiple variants of the same run-time queue, e.g. short.a, short.b, with each queue having different hardware, perhaps CPU generation or maximum memory or memory available per slot. To maximise scheduling options you can define compound queues which have the configuration of the least capable constituent. To define a compound queue, the queue name (key of the YAML dictionary) should be a comma separated list of queue names (no space).

#### Host Group Queues

Some clusters may be configured with host groups which sub-divide a queue by hardware capabilities (e.g. different system RAM sizes or run-time limits). You can target these host groups by specifying the queue name as 'queue@@hostgroup'. These would normally be included both in a compound queue (see above) along with the base queue name and a specific host group queue with the specific limits to maximise scheduling options.
