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

### Current version of tensorflow 1.4.0, keras 2.1.1


