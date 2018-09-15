# AtlasLearning
Here is some code to process ROOT files and adapt them to be fed to a neural network using keras and tensorflow

## Setting up your environment.
First we have to talk about setup, there are a few things to know to be able to send jobs on gpu in the CC:

My advice is to set up a virtual environment to ensure the versions of python modules are those of the CC.

### Setting up a conda virtualenv:

Fist we will need to download and install Anaconda or Miniconda; Anaconda comes with many modules such as Pandas, numpy, scipy, etc... so that you 
do not have to download all of them separately.

To download Anaconda:\
with python 2: ```wget https://repo.anaconda.com/archive/Anaconda2-5.2.0-Linux-x86_64.sh```\
with python 3: ```wget https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh```

To download Miniconda:\
with python 2: ```wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh```\
with python 3: ```wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh```


Then ```sh <myfile>.sh```

To be able to use ROOT within the conda installation, you have to add the channel: \
```conda config --add channels https://conda.anaconda.org/NLeSC```

To enable the virtual environment:\
```conda create —name=<env name> root=6 python=<python version you want to use>```

Now that you created your virtual environment, you can activate it with:\
```source activate <env_name>```

Once you activated the environment, depending on your choice between Anaconda and Miniconda you will need to setup some packages.
The minimum you need (already prvided with Anaconda) is numpy, pandas, scikit-learn and pyroot (matplotlib highly recomended).
to set it up:\
```pip install <package name>``` \
if it is not executed in virtualenv you will eventually get errors due to the fact that pip has to manipulate some files that you dont have rights of access and writing to;
for that use the option --user (```pip install --user <package name>```)

For Miniconda AND Anaconda:\
To be able to work on the CC you will need tensorflow 1.4.0 or 1.4.1 and keras 2.1.1 (for cuda version compatibility purposes)
To do so you have to specify to pip the version

/!\ /!\ /!\ If you are planning to work on standard CPU queues only tensorflow not gpu will do, else for GPU queues tensorflow-gpu is what you need (else it will never use the gpus)

GPU: ```pip install tensorflow-gpu==1.4.0```\
CPU: ```pip install tensorflow``` (the version is not so important here since it will not try to use cuda)\
And at the end you will need Keras:\
GPU: ```pip install keras==2.1.1```\
CPU: ```pip install keras``` (version is irrelevant once again, except if some implemented functions change and bugs appear)

### Current version of CUDA (on mc_gpu_interactive): CUDA 8.0, and the versions that are working with it are tensorflow 1.4.0, keras 2.1.1

You also need to add those lines in your .bashrc (it is possible that everything works fine without, but chances are you need those) to indicate your environment where to find CUDA:

```Shell
if ! echo ${LD_LIBRARY_PATH} | /bin/grep -q /opt/cuda-8.0/lib64 ; then
      LD_LIBRARY_PATH=/opt/cuda-8.0/lib64:${LD_LIBRARY_PATH}
fi
```

(to check cuda version: ```which nvcc``` on the machine where the gpus are)

## Running interactive jobs using GPU's on CC

To run on interactive machines with GPU's, the following command is valid:

```qlogin -q mc_gpu_interactive -pe multicores_gpu 4```

in a more precise fashion, one can use this as a ready to go command with ressources scheduling, and project ATLAS already plugged in:

```qlogin -l sps=1,GPU=2,os=cl7 -q mc_gpu_interactive -pe multicores_gpu 4 -P P_atlas```

once launched:

```Shell
JSV "/opt/sge/util/resources/jsv/corebinding.jsv" has been started
JSV "/opt/sge/util/resources/jsv/corebinding.jsv" has been stopped
Your job 51781307 ("QLOGIN") has been submitted
waiting for interactive job to be scheduled ...timeout (3 s) expired while waiting on socket fd 6
.timeout (6 s) expired while waiting on socket fd 6

Your interactive job 51781307 has been successfully scheduled.

Your interactive job 51781307 has been successfully scheduled.
Establishing /usr/bin/qlogin_wrapper session to host ccwgige010.in2p3.fr ...
The authenticity of host '[ccwgigeXXX.in2p3.fr]:40774 ([134.158.48.126]:40774)' can't be established.
ECDSA key fingerprint is SHA256:wmXwcX0cJrRE/D5kyxYRVq2hYpF7PTYHud6X4/Ygmh0.
ECDSA key fingerprint is MD5:93:0b:6c:35:dc:cd:6f:eb:9b:39:68:03:44:d7:a5:dc.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[ccwgigeXXX.in2p3.fr]:40774,[134.158.48.126]:40774' (ECDSA) to the list of known hosts.
username@ccwgige010.in2p3.fr's password: 
Last login: Sat Sep 15 18:38:57 2018 from cca001.in2p3.fr
  ___  ___     __  __ _  ____  ____  ____ 
 / __)/ __)___(  )(  ( \(___ \(  _ \( __ \
( (__( (__(___))( /    / / __/ ) __/ (__ (
 \___)\___)   (__)\_)__)(____)(__)  (____/

Platform: CentOS 7.4.1708 
Architecture: x86_64

[username@ccwgigeXXX ~]$ bash
bash-4.2$ source activate <environment name>
```

And you are ready to go.

### Checking for gpu effective usage on job:

To ensure that everything works fine, one might want to check if the GPU's are effectively recognized by the tensorflow-gpu module (this works for tensorflow, but there must be ways to do it with any other package allowing parallel computation on GPU)

just execute this script:

```Python
from tensorflow.python.client import device_lib
local_device_protos = device_lib.list_local_devices()
print([x.name for x in local_device_protos])
```

Which should output something like that:

```Shell
2018-09-15 18:58:39.438512: I tensorflow/core/platform/cpu_feature_guard.cc:137] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 FMA
2018-09-15 18:58:39.649437: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Found device 0 with properties: 
name: Tesla K80 major: 3 minor: 7 memoryClockRate(GHz): 0.8235
pciBusID: 0000:04:00.0
totalMemory: 11.17GiB freeMemory: 11.10GiB
2018-09-15 18:58:39.810251: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Found device 1 with properties: 
name: Tesla K80 major: 3 minor: 7 memoryClockRate(GHz): 0.8235
pciBusID: 0000:05:00.0
totalMemory: 11.17GiB freeMemory: 11.10GiB
2018-09-15 18:58:39.810655: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1045] Device peer to peer matrix
2018-09-15 18:58:39.810709: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1051] DMA: 0 1 
2018-09-15 18:58:39.810725: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1061] 0:   Y Y 
2018-09-15 18:58:39.810734: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1061] 1:   Y Y 
2018-09-15 18:58:39.810761: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1120] Creating TensorFlow device (/device:GPU:0) -> (device: 0, name: Tesla K80, pci bus id: 0000:04:00.0, compute capability: 3.7)
2018-09-15 18:58:39.810776: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1120] Creating TensorFlow device (/device:GPU:1) -> (device: 1, name: Tesla K80, pci bus id: 0000:05:00.0, compute capability: 3.7)

```



