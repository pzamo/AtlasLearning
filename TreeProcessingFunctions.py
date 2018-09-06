import numpy as np


### Here are some functions to preprocess the data, these are explained here, feel free to add new ones in this file. ###




def permutation_finder(seq, reverse = True):
    """In order to use only the most energetic clusters one have to sort them. but to keep consistency one has to sort the other cluster variables by the same pattern.
    This function is used to find the permutation pattern that sorts one sequence of data."""
    return(sorted(range(len(seq)), key = lambda x: seq[x], reverse = reverse))

def permutation_applier(seq, perm):
    """This functions is used to apply the permutation pattern found by permutation_finder to any sequence of data of the same size"""
    ordered = [seq[i] for i in perm]
    return(ordered)


def ponderation_applier(seq1, seq2):
    """Applies a ponderation, multiplying element-wise seq1 by seq2, same as multiplying two numpy arrays"""
    pondered = [seq1[i]*seq2[i] for i in range(len(seq1))]
    return(pondered)


def delta_applier(seq, jet_value, norm = 0.4):
    """Substracts a scalar value from a list, element-wise, eventually apply a normalization to [-1, 1] (0.4 is used to normalize the outputs of a cluster list where the jet
    is defined by all the clusters that are in a distance of at most 0.4 from its center)"""
    if norm == None:
        delta = [(c - jet_value) for c in seq]
    else:
        delta = [(c - jet_value)/0.4 for c in seq]
    return(delta)



def normalize_to_max(seq):
    """Normalizes a sequence to its maximum value"""
    M = abs(max([c for c in seq]))
    normalized = [c/M for c in seq]
    return(normalized)

def normalize_to_gauss(seq, mean, std):
    """Apply a normalization to a gaussian distribution of a sequence"""
    normalized = [(c-mean)/std for c in seq]
    return(normalized)

def mask_applier(seq, masked_length, masking_value = -50):
    """Used to pad a sequence with a mask value, it is useful to not backpropagate the weights to neurons that were not used by the neural network. since the inputs have to be the same length (in order to be converted to a tensor)
    one must pad sequences of inequal length with masking values."""
    n = min(len(seq), masked_length)
    masked = [seq[i] for i in range(n)] + [float(masking_value)]*max(0, masked_length-n)
    return(masked)

def intime(seq, threshold):
    """Returns a list of booleans that indicates if the clusters of the sequence have a time of appearance more or less than a threshold"""
    return([int(abs(c)<threshold) for c in seq])

def mean(seq):
    """Returns the mean of a sequence"""
    return np.mean(seq)

def moment(seq, mean, order):
    """Applies a moment to a variable, see moments in probability theory"""
    return(np.mean([(c-mean)**order for c in seq]))