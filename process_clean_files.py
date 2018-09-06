#!/usr/bin/env python2.7
### This is the file where all the additional classes and methods are defined ###

import ROOT as rt
import pandas as pd
import os
import sys
import root_numpy as rn
import numpy as np
import time as tm
import datetime
import subprocess as sp
from TreeProcessing import *

size = lambda x: os.path.getsize(x)/10.0**9
get_files_list = lambda x: sp.check_output(['ls', x]).splitlines()
date = datetime.datetime.now
root_process = rt.gInterpreter.ProcessLine
stamp = tm.time
isfile = os.path.isfile
sizeof = lambda x: sys.getsizeof(x)/125000



def fileinside(directory, suffix = '.root'):
    """Check if there are files with suffix in the directory
    Arguments:
    directory: string of type '/path/to/directory/'
    suffix: string of type '.extension'"""
    for c in get_files_list(directory):
        if c.split('.')[-1] == suffix[1:]:
            return(True)
    return(False)


def process_list(L):
    """This function is useful to save a file in csv format, since all the values are converted to strings, one can store arrays in this way:
    [1,2,3] -> '1:2:3'
    to convert back one can use: lambda x: list(map(float, x.split(':'))"""
    return(':'.join(map(str, L)))

def process_path(path):
    """Used to process string representing paths to an universal format, permits to avoid errors"""
    if path[0] == '.':
        path = os.path.abspath(path)
    elif path[0] == '~':
        path = os.path.expanduser('~') + path[1:]
    ifile = os.path.isfile(path)
    return(path+'/'*(path[-1]!='/')*(not ifile), ifile)


def process_df(dataframe, tuples_list):
    for c in tuples_list:
        new_col = dataframe[c].apply(lambda x: process_list(list(x)))
        dataframe.drop([c], axis = 1, inplace = True)
        dataframe[c] = new_col
    return(dataframe)


def qsub(script, name = None, ressources = None, queue = None, log_dir = None, scriptargs = []):
    """This function is used to launch a job on the CC.
    Arguments:
    script: the string path to the script to be launched in the job
    name: string representing the name you want to give to the job
    ressources: string to request ressources for the job, see https://doc.cc.in2p3.fr/en:utiliser_le_systeme_batch_ge_depuis_le_centre_de_calcul
    queue: string with the name of the queue you want to use
    log_dir: string with the path where you want the working machine to sent the logs of your job (errors and outputs)
    scriptargs: list with arguments to pass to the job, useful for example when many jobs are launched by one script to differenciate the names of the output files (see XXX)"""
    command = ['qsub', '-P', 'P_atlas']
    if name:
        command += ['-N', name]
    if ressources:
        command += ['-l', ressources]
    if queue:
        command += ['-q', queue]
    if log_dir:
        command += ['-o', log_dir, '-e', log_dir]
    command += [script]
    for arg in scriptargs:
        command += [str(arg)]
    sp.call(command)





















class root_path:
    """This class implements some useful tricks to ease your life when processing data
    This class creates an object that carries data of what the directory or file path is containing, see XXX for a usecase
    Arguments:
    directory: string of the form '/path/to/directory'
    output_dir: string of the form '/path/to/directory', used to determine where the outputs of the processing one is going to apply on the directory will be stored
    input_suffix: string of the form '.extension' that will be used to consider only the files with this extension in the directory
    output_suffix: used to write the goot output files extension, same form than input_suffix
    """
    def __init__(self, directory, output_dir = None, input_suffix = '.root', output_suffix = '.csv'):
        if type(directory) == list:
            self.path = directory
            self.tfiles = directory
            self.output_dir = output_dir

            self.sizes = {c: size(c) for c in self.tfiles}
            self.totsize = sum(self.sizes.values())
        else:
            self.path, self.ifile = process_path(directory)
            if self.ifile and self.path.split('.')[-1] == input_suffix[1:]:

                self.tfiles = self.path
                self.sizes = {self.tfiles: size(self.tfiles)}
                if output_dir == None:

                    self.output_dir = process_path('/'.join(self.path.split('.')[0].split('/')[0:-1]))[0]
                else:

                    self.output_dir = process_path(output_dir)[0]
                self.totsize = size(self.path)


            elif not self.ifile and fileinside(self.path, suffix = input_suffix):
                self.tfiles = [self.path + c for c in get_files_list(self.path) if c.split('.')[-1] == input_suffix[1:]]
                self.sizes = {c: size(c) for c in self.tfiles}
                if output_dir == None:

                    self.output_dir = self.path
                else:

                    self.output_dir = process_path(output_dir)[0]
                self.totsize = sum(self.sizes[c] for c in self.tfiles)
            else:


                raise ValueError('No {} files in {}'.format(output_suffix, repr(self)))

        self.output_suffix = output_suffix
        self.batch_number = 0
        self.input_suffix = input_suffix

    def __repr__(self):
        return(self.path)
    def __str__(self):
        return(str(self.path))

    def preprocess_tree(self, input_treeName, output_treeName = None, output_fileName = None, max_clusters = 70, masking_length = 10):
        """This function calls TreeProcessing function from TreeProcessing.py, used to preprocess one tree in order to have the needed variables to feed to a neural network"""
        if output_treeName == None:
            output_treeName = 'PreprocTree'
        if output_fileName == None:
            output_fileName = 'PreprocTree.root'
        TreeProcessing(in_path = self.tfiles, in_treeName = input_treeName, out_path = self.output_dir + output_fileName, out_treeName = output_treeName, MAX_CLUSTERS = max_clusters, masking_length = masking_length)

    def create_batches(self, batch_size = 3):
        """This method is used to generate lists of paths that are approximately the same size to send jobs afterwhile
        Arguments:
        batch_size: float or int representing the size in Gb of the batches"""
        batch_list = []
        sze = 0
        batch = []
        for file in sorted(self.tfiles, key = lambda x: self.sizes[x]):
            if sze < batch_size:
                batch.append(file)
                sze += self.sizes[file]
            else:
                batch_list.append(batch)
                sze = 0
                batch = [file]
        if batch:
            batch_list.append(batch)
        for i, batch in enumerate(batch_list):
            path = root_path(batch, output_dir = self.output_dir, input_suffix = self.input_suffix, output_suffix = self.output_suffix)
            path.batch_number = i
            yield path

    def process_with_script(self, script, on_cc = False, name = None, ressources = None, queue = None, log_dir = None):
        """if on_cc, scriptfile must accept minimal bash arguments:
            batch : a string of one or multiple paths, comma separated
            batch_number an int """
        if on_cc:
            for i, batch in enumerate(self.create_batches()):
                qsub(script, name, ressources, queue, log_dir, scriptargs = [','.join(batch.tfiles), self.output_dir, i])

    def file_generator(self, chunksize = 1000, fit = False, treename = 'PreprocTree'):

        """This method is used to generate batches from root tree an pandas dataframes, one can then process this data one last time in order to feed it to the neural net, see RNN_proc.py
        Argument:
        chunksize: int for the size of every batch of data generated
        fit: boolean indicating whether or not the generator must loop for ever or not across the data (useful to fit a neural network since the same events can be learned from many times)
        treename: string indicating what is the name of the tree in the clean_file_tree (explained in depth later) that one is willing to use to generate its data"""
        if self.input_suffix == '.root':
            if type(self.tfiles) == str:
                files = [self.tfiles]
            else:
                files = self.tfiles
            once_again = True
            while once_again:
                for file in files:
                    f = rt.TFile.Open(file)
                    t = f.Get(treename)
                    yield clean_file_tree(t)
                once_again = fit
        if self.input_suffix == '.csv':
            enter = True
            while enter:
                for file in self.tfiles:
                    for df in pd.read_csv(file, iterator = True, chunksize = chunksize):
                        yield df
                enter = fit

    def apply(self, function):
        for file in self.tfiles:
            for item in function(file):
                yield item
















class clean_file_tree(rt.TTree):

    """This class extends the ROOT.TTree class with new function adapted for deep learning on root files, see a working example on XXX"""
    def __init__(self, tree, MAX_ENTRIES = 10000, MAX_SIZE = 3.0):
        branch_tuple = rn.tree2array(tree, stop = 1).dtype
        branch_dic = branch_tuple.fields
        tuples = [c for c in branch_tuple.names if np.dtype(branch_dic[c][0]) == np.dtype('O')]
        self.branches = branch_tuple
        self.ENTRIES = int(tree.GetEntries())
        self.vars_dic = {'scalar': [c for c in self.branches.names if c not in tuples], 'tuple': tuples}
        self.tree = tree
        self.MAX_ENTRIES = 10000
        self.MAX_SIZE = 3.0
        self.treeNames = []
        for key in self.tree.GetListOfKeys():
            self.treeNames.append(key.GetName())
    def array_generator(self, chunk_size, branches = None, as_df = False):
        """Used to generate arrays from the tree
        Arguments:
        chunk_size: int for the size of the chunks to yield
        branches: the name of the branches to keep in the array, one can see the branches from within which to chosse by using clean_tree_file.branches attribute
        as_df: boolean, if True yields the arrays in the form of pandas.DataFrame objects, else yields raw numpy.array"""
        Max = 1 + self.ENTRIES/chunk_size
        i = 0
        if not as_df:
            for i in xrange(Max):
                yield rn.tree2array(self.tree, branches = branches, start = i, stop = i + chunk_size)
        else:
            for i in xrange(Max):
                yield pd.DataFrame(rn.tree2array(self.tree, branches = branches, start = i, stop = i + chunk_size))



    def write_csv(self, path = None, branches = None, output_name = 'jetTree', sep = ',', start = None, stop = None, step = None, rewrite = False, batch_id = ''):
        """This method is used to write root trees to csv files, may be useful to explore faster the data, but csv's take much more place on ram when opened
        Arguments:
        path: an instance of the root_path class
        branches: list of strings with names of branches to keep
        output_name: string naming the output prefix of the files to write (eventually there will be many of them, divided into smaller size files)
        sep: separator for values in csv
        start/stop: integers for where to start and where to stop in tree entries
        step: integer for what step to apply in the array generator
        rewrite: boolean, if True rewrites the file (if there is a file with same name in output_dir), else appends lines to it
        batch_id: integer useful for naming the files if there are many batches at once that processes the file
        """
        if path == None:
            raise MemoryError('file may cause memory leak, use start/stop arguments to select smaller dataset, use self.max_size (current is {} events) to load more events, or define a path to store the csv'.format(self.max_size))
        # elif type(path) == str:
            
        # elif type(path)
        else:
            if step == None:
                step = self.MAX_ENTRIES
            output_path = ''
            g = self.array_generator(chunk_size = step, branches = branches, as_df = True)
            i = 0
            stamp1 = stamp()
            for df in g:
                print('{} / {}'.format(i, int(self.ENTRIES/self.MAX_ENTRIES)))
                df = process_df(df, self.vars_dic['tuple'])
                output_path = path.output_dir + output_name + '_{}_{}'.format(batch_id, path.batch_number) + path.output_suffix
                if rewrite or not isfile(output_path):
                    df.to_csv(output_path, sep = sep, header = True, index = False)
                else:
                    df.to_csv(output_path, mode = 'a', sep = sep, header = False, index = False)

                if self.MAX_SIZE < size(output_path):
                    isfirst, i, path.batch_number = True, i + 1, path.batch_number + 1
                else:
                    isfirst, i = False, i + 1
                # i += 1
            stamp2 = stamp()
            time = stamp2-stamp1
            print('done in {} s, files at {}'.format(time, output_path))
            return(path.batch_number)


def batching_jobs(path, max_batch_size, input_suffix = '.root'):
    sze = 0
    batches_list = []
    batch_list = []
    output_dir = path.output_dir
    for c in path.sizes:
        if sze < max_batch_size:
            batch_list.append(root_path(c, output_dir, input_suffix))
            sze += path.sizes[c]
        else:
            batches_list.append(batch_list)
            batch_list = []
            sze = 0
    batches_list.append(batch_list)
    return(batches_list)

def job_definition(batch_list, batch_id):
    path0 = batch_list[0]
    file = rt.TFile.Open(repr(path0))
    tree = file.Get('jvttree')
    ctree = clean_file_tree(tree)
    ctree.MAX_ENTRIES = 20000
    last_output = ctree.write_csv(path0, batch_id = batch_id)
    for path in batch_list[1:]:
        path.batch_number = last_output
        file = rt.TFile.Open(repr(path))
        tree = file.Get('jvttree')
        ctree = clean_file_tree(tree)
        ctree.MAX_ENTRIES = 20000
        last_output = ctree.write_csv(path, batch_id = batch_id)
    return('done')


class GeneratorFile():
    def __init__(self, path, tree_name):
        self.path = path
        f = rt.TFile.Open(path)
        f = f.Get(tree_name)
        length = f.GetEntries()
        self.tree = f
    def __len__(self):
        return(self.length)
    
