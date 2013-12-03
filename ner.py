# Grader 

#!/usr/bin/env python
"""
Optionally run as grader.py [basic|all] to run a subset of tests
"""


import math, random, copy

import graderUtil
grader = graderUtil.Grader()
submission = grader.load('submission')

from collections import Counter

import util
import nerUtils
from util import Counters
import itertools as it


############################################################
# Problem 1: CRFs
############################################################

simpleCRF = submission.LinearChainCRF( ["-FEAT-", "-SIZE-"], 
        submission.binaryFeatureFunction,
        Counter({
            ("-FEAT-", "-SIZE-") : 0.8,
            ("-SIZE-", "-FEAT-") : 0.5,
            ("-SIZE-", "-SIZE-") : 1.,
            ("-FEAT-", "Beautiful") : 1.,
            ("-SIZE-", "Beautiful") : 0.5,
            ("-FEAT-", "2") : 0.5,
            ("-SIZE-", "2") : 1.0,
            ("-FEAT-", "bedroom") : 0.5,
            ("-SIZE-", "bedroom") : 1.0,}) )
exampleInput = "Beautiful 2 bedroom".split()
exampleTags = "-FEAT- -SIZE- -SIZE-".split()

import pickle
states, parameters = pickle.load( open('data/english.binary.crf') ) 
englishCRF = submission.LinearChainCRF( states, submission.binaryFeatureFunction, parameters ) 




def part1a_2():
    """Check that you get the gold labelling."""
    mediumCRF = submission.LinearChainCRF( ["-FEAT-", "-SIZE-"],
            submission.binaryFeatureFunction,
            Counter({
                ("-FEAT-", "-SIZE-") : 0.8,
                ("-SIZE-", "-FEAT-") : 0.5,
                ("-SIZE-", "-SIZE-") : 1.,
                ("-FEAT-", "-FEAT-") : 1.,
                ("-FEAT-", "Beautiful") : 1.,
                ("-SIZE-", "Beautiful") : 0.5,
                ("-FEAT-", "house") : 1.,
                ("-SIZE-", "house") : 0.5,
                ("-FEAT-", "2") : 0.5,
                ("-SIZE-", "2") : 1.0,
                ("-FEAT-", "bedroom") : 0.5,
                ("-SIZE-", "bedroom") : 1.0,}) )
    moreExampleInputs = [
        "This is a Beautiful 2 bedroom".split(),
        "2 bedroom Beautiful house".split(),
        ]
    moreExampleTags = [
        ['-FEAT-', '-FEAT-', '-FEAT-', '-FEAT-', '-SIZE-', '-SIZE-'],
        ['-SIZE-', '-SIZE-', '-FEAT-', '-FEAT-']
        ]
    for xs, ys in zip(moreExampleInputs, moreExampleTags):
        ys_ = submission.computeViterbi(mediumCRF, xs)
        grader.requireIsEqual( ys, ys_ )
grader.addBasicPart('1a-2', part1a_2, 0)


def part1b_3():
    """Check that values match our reference"""
    xs = exampleInput
    backward = [
            Counter({'-SIZE-': 0.564, '-FEAT-': 0.435}),
            Counter({'-SIZE-': 0.567, '-FEAT-': 0.432}),
            Counter({'-FEAT-': 0.5, '-SIZE-': 0.5})]
    backward_ = submission.computeBackward(simpleCRF, xs)
    for vec, vec_ in zip( backward, backward_):
        grader.requireIsTrue( Counters.approximateEquals( vec, vec_ ) )
grader.addBasicPart('1b-3', part1b_3, 0)


############################################################
# -- 1c: Compute expected statistics

def part1c_0():
    """Check that the expected counts at each step add up to 1."""
    xs = exampleInput
    T = submission.computeEdgeMarginals(simpleCRF, xs)
    for t in T:
        grader.requireIsEqual( 1.0, sum(t.values()) )
grader.addBasicPart('1c-0', part1c_0, 0)

def part1c_1():
    """Check that values match our reference"""
    xs = exampleInput
    T = [ Counter({('-BEGIN-', '-FEAT-'): 0.561, ('-BEGIN-', '-SIZE-'): 0.439}),
          Counter({('-FEAT-', '-SIZE-'): 0.463, ('-SIZE-', '-SIZE-'): 0.343, 
                   ('-SIZE-', '-FEAT-'): 0.096, ('-FEAT-', '-FEAT-'): 0.096}),
          Counter({('-SIZE-', '-SIZE-'): 0.590, ('-SIZE-', '-FEAT-'): 0.217,
                   ('-FEAT-', '-SIZE-'): 0.151, ('-FEAT-', '-FEAT-'): 0.041})
        ]
    T_ = submission.computeEdgeMarginals(simpleCRF, xs)
    for t, t_ in zip(T, T_):
        grader.requireIsTrue( Counters.approximateEquals(t, t_) )
grader.addBasicPart('1c-1', part1c_1, 0)



############################################################
# -- 2a: NER Features

def part2a_0():
    """Check that you have all the features we expect"""
    xs = exampleInput
    phi = Counter({('-BEGIN-', '-FEAT-'): 1.0, ('-FEAT-', 'Beautiful'): 1.0, ('-FEAT-', 'PREV:-BEGIN-'): 1.0, ('-FEAT-', 'NEXT:2'): 1.0, ('-FEAT-', '-CAPITALIZED-'): 1.0, ('-FEAT-', '-POST-CAPITALIZED-'): 0.0})
    phi_ = submission.nerFeatureFunction(0, '-BEGIN-', '-FEAT-', xs)
    grader.requireIsTrue( Counters.approximateEquals(phi, phi_) )

    phi = Counter({('-FEAT-', '-SIZE-'): 1.0, ('-SIZE-', 'PREV:Beautiful'): 1.0, ('-SIZE-', 'NEXT:bedroom'): 1.0, ('-SIZE-', '-PRE-CAPITALIZED-'): 1.0, ('-SIZE-', '2'): 1.0, ('-SIZE-', '-POST-CAPITALIZED-'): 0.0, ('-SIZE-', '-CAPITALIZED-'): 0.0})
    phi_ = submission.nerFeatureFunction(1, '-FEAT-', '-SIZE-', xs) 
    grader.requireIsTrue( Counters.approximateEquals(phi, phi_) )
    
    phi = Counter({('-SIZE-', '-SIZE-'): 1.0, ('-SIZE-', 'PREV:2'): 1.0, ('-SIZE-', 'bedroom'): 1.0, ('-SIZE-', 'NEXT:-END-'): 1.0, ('-SIZE-', '-CAPITALIZED-'): 0.0, ('-SIZE-', '-PRE-CAPITALIZED-'): 0.0})
    phi_ = submission.nerFeatureFunction(2, '-SIZE-', '-SIZE-', xs)
    grader.requireIsTrue( Counters.approximateEquals(phi, phi_) )

grader.addBasicPart('2a-0', part2a_0, 2)


############################################################
# -- 2b: Competition with features
grader.addManualPart('2b-0', 10)

############################################################
# -- 3a: Treewidth
grader.addManualPart('3a-0', 2)

############################################################
# -- 3b: Markov blanket for CRF
grader.addManualPart('3b-0', 2)

############################################################
# -- 3c: Gibbs sampling for CRF

def part3c_0():
    """
    The sample distribution and exact distribution should match fairly closely.
    """
    xs = exampleInput
    N = 3000

    difference = 0.0
    for ys, estimatedProb in submission.computeGibbsProbabilities( simpleCRF, 
            submission.getCRFBlocks,
            submission.chooseGibbsCRF,
            xs, N ).iteritems():
        trueProb = nerUtils.computeProbability( simpleCRF, xs, ys )
        difference = abs( trueProb - estimatedProb )
        grader.requireIsLessThan( 5e-2, difference )
grader.addBasicPart('3c-0', part3c_0, 0)

def part3c_1():
    """
    The estimated best sequence should be the right one!
    """
    xs = exampleInput
    ys = exampleTags
    N = 1000

    ys_ = submission.computeGibbsBestSequence(
            simpleCRF,
            submission.getCRFBlocks,
            submission.chooseGibbsCRF,
            xs, 
            N)
    grader.requireIsEqual( ys, ys_ )
grader.addBasicPart('3c-1', part3c_1, 0)

def part3c_2():
    """
    Your implementation should be fast enough. Make sure you are only using
    factors in the Markov blanket.
    * Done correctly, this takes about 0.5 seconds. 
    * Done naively, it can take ~2.5 seconds.
    """
    xs = "Werner & Co entered court today . Werner maintained that they were not guilty .".split()
    N = 10000

    submission.computeGibbsProbabilities( englishCRF,
            submission.getCRFBlocks,
            submission.chooseGibbsCRF,
            xs, N )
    grader.requireIsTrue(True)
grader.addBasicPart('3c-2', part3c_2, 0, 1)



############################################################
# -- 3d: Block Gibbs Sampling Markov Blanket
grader.addManualPart('3d-0', 2)

############################################################
# -- 3f: Block Gibbs Sampling 

def part3e_0():
    """
    Make sure you are getting the right blocks
    """
    xs = "A A B C B A C".split()
    blocks = submission.getLongRangeCRFBlocks(xs)
    
    # Make sure everything is there
    grader.requireIsEqual( set( it.chain.from_iterable( blocks ) ), set(xrange(len(xs))) )
    # Make sure that each block has identical symbols
    for block in blocks:
        grader.requireIsEqual( 1, len(set([xs[i] for i in block])) )
grader.addBasicPart('3e-0', part3e_0, 0)

def part3e_1():
    """
    If you handle long range dependencies you should get a different output than 
    the usual CRF.
    """
    # Run on a few examples and see that the constraints are being met.
    xs = "Werner & Co entered court today . Werner maintained that they were not guilty .".split()
    ys = "-ORG- -ORG- -ORG- -O- -O- -O- -O- -ORG- -O- -O- -O- -O- -O- -O- -O-".split()
    assert len(xs) == len(ys)

    N = 10000
    ysLongRangeGibbs = submission.computeGibbsBestSequence(
            englishCRF,
            submission.getLongRangeCRFBlocks,
            submission.chooseGibbsLongRangeCRF,
            xs, 
            N)
    grader.requireIsEqual( ys, ysLongRangeGibbs )
grader.addBasicPart('3e-1', part3e_1, 1)


if __name__ == "__main__":
    grader.grade()


# Submission

"""
CS221 Assignment 'ner'
Owner: Arun Chaganty
"""

import itertools as it
import math, random

from collections import Counter

import util
from util import Counters

BEGIN_TAG = '-BEGIN-'
END_TAG = '-END-'
CAP_TAG = '-CAPITALIZED-'
PREV_TAG = 'PREV:'
NEXT_TAG = 'NEXT:'
PRECAP_TAG = '-PRE-CAPITALIZED-'
POSTCAP_TAG = '-POST-CAPITALIZED-'

###############################################
# Problem 1. Linear Chain CRFs
###############################################

class LinearChainCRF(object):
    r"""
    This is a 'struct' that contains the specification of the CRF, namely
    the tags, featureFunction and parameters.
    """

    def __init__(self, tags, featureFunction, parameters = None ):
        r"""
        @param tags list string - The domain of y_t. For NER, these
               will be tags like PERSON, ORGANIZATION, etc.
        @param featureFunction function - Function that takes the time step
               t, previous tag y_{t-1}, current tag y_t, and observation
               sequence x, and returns a Counter representing the feature vector
               \phi_{local}(t, y_{t-1}, y_t, x).
               - E.g. unaryFeatureFunction, binaryFeatureFunction
        @param parameters Counter - parameters for the model (map from feature name to feature weight).
        """
        self.TAGS = tags
        self.featureFunction = featureFunction
        if parameters is None:
            parameters = Counter()
        self.parameters = parameters

    def G(self, t, y_, y, xs):
        r"""
        Computes one of the potentials in the CRF.
        @param t int - index in the observation sequence, 0-based.
        @param y_ string - value of of tag at time t-1 (y_{t-1}),
        @param y string - value of of tag at time t (y_{t}),
        @param xs list string - The full observation seqeunce.
        @return double - G_t(y_{t-1}, y_t ; x, \theta)
        """
        return math.exp( Counters.dot( self.parameters, self.featureFunction(t, y_, y, xs) ) )

####################################################3
# Problem 1a
def computeViterbi(crf, xs):
    """
    Compute the maximum weight assignment using the Viterbi algorithm.
    @params crf LinearChainCRF - the CRF model.
    @param xs list string - the sequence of observed words.
    @return list string - the most likely sequence of hidden TAGS.

    Tips:
    + Normalize Viterbi[i] at the end of every iteration (including 0!) to prevent numerical overflow/underflow.

    Possibly useful:
    - BEGIN_TAG
    - crf.TAGS
    - crf.G
    - Counter
    """

    # BEGIN_YOUR_CODE (around 27 lines of code expected)
    Viterbi = []
    Viterbi.append(1)

    V = []
    for tag in crf.TAGS:
        V.append(crf.G(0,BEGIN_TAG,tag,xs))
    V = [V[i]/sum(V) for i in range(len(V))]
    Viterbi.append(V)
    
    for t in range(1,len(xs)):
        V = []
        for tag in crf.TAGS:
            V.append(max([Viterbi[t][i]*crf.G(t,crf.TAGS[i], tag, xs) for i in range(len(Viterbi[t]))]))
        V = [V[i]/sum(V) for i in range(len(V))]
        Viterbi.append(V)
    
    y = [None for i in range(len(xs))]
    end_index = len(xs)-1
    y[end_index] = crf.TAGS[Viterbi[len(xs)].index(max(Viterbi[len(xs)]))]
    
    for t in [len(xs) - i for i in range(2,len(xs)+1)]:
        l = [Viterbi[t+1][i]*crf.G(t,crf.TAGS[i],y[t+1],xs) for i in range(len(Viterbi[t+1]))]
        y[t] = crf.TAGS[l.index(max(l))]
       
    return y
    # END_YOUR_CODE

####################################################3
# Problem 1b
def computeForward(crf, xs):
    r"""
    Computes the normalized version of 
        Forward_t(y_{t}) = \sum_{y_{t-1}} G_t(y_{t-1}, y_t; x, \theta) Forward{t-1}(y_{t-1}).

    @params crf LinearChainCRF - the CRF
    @param xs list string - the sequence of observed words
    @return (double, list Counter) - A tuple of the computed
    log-normalization constant (A), and the sequence Forward_t; each member
    of the list is a counter that represents Forward_t

    Example output: (5.881, [
                Counter({'-FEAT-': 0.622, '-SIZE-': 0.377}), 
                Counter({'-SIZE-': 0.761, '-FEAT-': 0.238}), 
                Counter({'-SIZE-': 0.741, '-FEAT-': 0.258})])

    Tips:
    * In this version, you will need to normalize the values so that at
    each t, \sum_y Forward_t(y_t) = 1.0. 
    * You will also need to collect the normalization constants z_t
      = \sum_{y_{t-1}} \sum_{y_{t-1}} G_t(y_{t-1}, y_{t}; x, \theta) * Forward_{t-1}(y_{t-1}) 
      to return the log partition function A = \sum_t \log(z_t). We need
      to take the log because this value can be extremely small or
      large.
    * Note that Forward_1(y_1) = G_1(-BEGIN-, y_1 ; x, \theta) before normalization.
    
    Possibly useful:
    - BEGIN_TAG
    - crf.G
    - crf.TAGS
    - Counter
    """
    A = 0.
    forward = [ None for _ in xrange(len(xs)) ]

    # BEGIN_YOUR_CODE (around 15 lines of code expected)
    forward_0 = 1
    
    #let's do forward_1:
    c = Counter()
    for tag in crf.TAGS:
        c[tag]=crf.G(0,BEGIN_TAG,tag,xs)
    z = sum(c.values())
    for key in c:
        c[key] = c[key]/z
    A = math.log(z)
    forward[0] = c
    
    #let's do all the rest:
    for t in range(1,len(xs)):
        c = Counter()
        for tag in crf.TAGS:
            c[tag] = sum([crf.G(t, last_tag, tag,xs)*forward[t-1][last_tag] for last_tag in forward[t-1]])
        z = sum(c.values())
        for key in c:
            c[key] = c[key]/z
        A = A + math.log(z)
        forward[t] = c
    
    # END_YOUR_CODE

    return A, forward

####################################################3
# More utility functions

def computeBackward(crf, xs):
    r"""
    Computes a normalized version of Backward. 

    @params crf LinearChainCRF - the CRF
    @param xs list string - the sequence of observed words
    @return list Counter - The sequence Backward_t; each member is a counter that represents Backward_t

    Example output: [
            Counter({'-SIZE-': 0.564, '-FEAT-': 0.435}),
            Counter({'-SIZE-': 0.567, '-FEAT-': 0.432}),
            Counter({'-FEAT-': 0.5, '-SIZE-': 0.5})]

    Tips:
    * In this version, you will need to normalize the values so that at
    each t, \sum_{y_t} Backward_t(y_t) = 1.0. 
    
    Possibly useful:
    - BEGIN_TAG
    - crf.G
    - crf.TAGS
    - Counter
    """

    backward = [ None for _ in xrange(len(xs)) ]

    backward[-1] = Counter( { tag : 1. for tag in crf.TAGS } ) 
    z = sum(backward[-1].values())
    for tag in backward[-1]:
        backward[-1][tag] /= z

    for t in xrange( len(xs)-1, 0, -1 ):
        backward[t-1] = Counter({ tag : 
                    sum( crf.G( t, tag, tag_, xs ) 
                        * backward[t][tag_] for tag_ in crf.TAGS )
                    for tag in crf.TAGS })
        z = sum(backward[t-1].values())
        for tag in backward[t-1]:
            backward[t-1][tag] /= z

    return backward

####################################################3
# Problem 1c
def computeEdgeMarginals(crf, xs):
    r"""
    Computes the marginal probability of tags, 
    p(y_{t-1}, y_{t} | x; \theta) \propto Forward_{t-1}(y_{t-1}) 
            * G_t(y_{t-1}, y_{t}; x, \theta) * Backward_{t}(y_{t}).

    @param xs list string - the sequence of observed words
    @return list Counter - returns a sequence with the probability of observing (y_{t-1}, y_{t}) at each time step

    Example output:
    T = [ Counter({('-BEGIN-', '-FEAT-'): 0.561, ('-BEGIN-', '-SIZE-'): 0.439}),
          Counter({('-FEAT-', '-SIZE-'): 0.463, ('-SIZE-', '-SIZE-'): 0.343, 
                   ('-SIZE-', '-FEAT-'): 0.096, ('-FEAT-', '-FEAT-'): 0.096}),
          Counter({('-SIZE-', '-SIZE-'): 0.590, ('-SIZE-', '-FEAT-'): 0.217,
                   ('-FEAT-', '-SIZE-'): 0.151, ('-FEAT-', '-FEAT-'): 0.041})
        ]

    Tips:
    * At the end of calculating f(y_{t-1}, y_{t}) = Forward_{t-1}(y_{t-1}) 
            * G_t(y_{t-1}, y_{t}; x, \theta) * Backward_{t}(y_{t}), you will
      need to normalize because p(y_{t-1},y_{t} | x ; \theta) is
      a probability distribution. 
    * Remember that y_0 will always be -BEGIN-; at this edge case,
        Forward_{0}(y_0) is simply 1. So, T[0] = p(-BEGIN-, y_1 | x ; \theta)
        = G_1(-BEGIN-, y_1; x, \theta) Backward_1(y_1).

    * Possibly useful:
    - computeForward
    - computeBackward
    """

    _, forward = computeForward(crf, xs)
    backward = computeBackward(crf, xs)

    T = [ None for _ in xrange( len(xs) ) ]

    # BEGIN_YOUR_CODE (around 17 lines of code expected)
    #let's do T[0]:
    c = Counter()
    for tag in crf.TAGS:
        c[(BEGIN_TAG,tag)] = crf.G(0, BEGIN_TAG, tag, xs)*backward[0][tag]
    z = sum(c.values())
    for key in c:
        c[key] = c[key]/z
    T[0] = c    
    
    #let's do the rest!
    for t in range(1,len(T)):
        c = Counter()
        for tag1 in crf.TAGS:
            for tag2 in crf.TAGS:
                c[(tag1,tag2)] = forward[t-1][tag1]*crf.G(t,tag1,tag2,xs)*backward[t][tag2]
        z = sum(c.values())
        for key in c:
            c[key] = c[key]/z
        T[t] = c
    # END_YOUR_CODE

    return T

###############################################
# Problem 2. NER 
###############################################

def unaryFeatureFunction(t, y_, y, xs):
    """
    Extracts unary features; 
        - indicator feature on (y, xs[t])
    @param t int - index in the observation sequence, 0-based.
    @param y_ string - value of of tag at time t-1 (y_{t-1}),
    @param y string - value of of tag at time t (y_{t}),
    @param xs list string - The full observation seqeunce.
    @return Counter - feature vector
    """
    phi = Counter({
        (y, xs[t]) : 1,
        })
    return phi

def binaryFeatureFunction(t, y_, y, xs):
    """
    Extracts binary features; 
        - everything in unaryFeatureFunction
        - indicator feature on (y_, y)
  @param t int - index in the observation sequence, 0-based.
    @param y_ string - value of of tag at time t-1 (y_{t-1}),
    @param y string - value of of tag at time t (y_{t}),
    @param xs list string - The full observation seqeunce.
    @return Counter - feature vector
    """
    phi = Counter({
        (y, xs[t]) : 1.0,
        (y_, y) : 1.0,
        })

    return phi

#################################
# Problem 2a
def nerFeatureFunction(t, y_, y, xs):
    """
    Extracts features for named entity recognition; 
        - everything from binaryFeatureFunction
        - indicator feature on y and the capitalization of xs[t]
        - indicator feature on y and previous word xs[t-1]; for t=0, use 'PREV:-BEGIN-'
        - indicator feature on y and next word xs[t+1]; for t=len(xs)-1, use 'NEXT:-END-'
        - indicator feature on y and capitalization of previous word xs[t-1]; assume 'PREV:-BEGIN-' is not capitalized.
        - indicator feature on y and capitalization of next word xs[t+1]; assume 'PREV:-BEGIN-' is not capitalized.
    Check the assignment writeup for more details and examples.

    @param t int - index in the observation sequence, 0-based.
    @param y_ string - value of of tag at time t-1 (y_{t-1}),
    @param y string - value of of tag at time t (y_{t}),
    @param xs list string - The full observation seqeunce.
    @return Counter - feature vector

    Possibly useful
    - Counter
    """
    # BEGIN_YOUR_CODE (around 18 lines of code expected)
    features = Counter()

    #Binary features
    bin = binaryFeatureFunction(t,y_,y,xs)
    features.update(bin)
    
    #Capitalized
    if(xs[t][0].isupper()):
        features[(y, CAP_TAG)] = 1.0
    
    #Last word
    if t == 0: features[(y,PREV_TAG+BEGIN_TAG)] = 1.0
    else: features[(y,PREV_TAG + xs[t-1])] = 1.0
    
    #Next word
    if t == len(xs)-1: features[(y, NEXT_TAG+END_TAG)] = 1.0
    else: features[(y,NEXT_TAG + xs[t+1])] = 1.0
    
    #Next and last capitalized
    if len(xs) == 1:  #if only 1 word, will have no next or last capitalized
        return features
    
    if t == 0:
        features[(y,POSTCAP_TAG)] = 1.0 if xs[t+1][0].isupper() else 0.0
    elif t == len(xs)-1:
        features[(y,PRECAP_TAG)] = 1.0 if xs[t-1][0].isupper() else 0.0            
    else:
        features[(y,PRECAP_TAG)] = 1.0 if xs[t-1][0].isupper() else 0.0
        features[(y,POSTCAP_TAG)] = 1.0 if xs[t+1][0].isupper() else 0.0
            
    return features
    
    
    # END_YOUR_CODE

#################################
# Problem 2b
def betterNerFeatureFunction(t, y_, y, xs):
    """
    Your own features for named entity recognition; 
    @param t int - index in the observation sequence, 0-based.
    @param y_ string - value of of tag at time t-1 (y_{t-1}),
    @param y string - value of of tag at time t (y_{t}),
    @param xs list string - The full observation seqeunce.
    @return Counter - feature vector

    Possibly useful
    - Counter
    """
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE


###############################################
# Problem 3. Gibbs sampling
###############################################

#################################
# Utility Functions

def gibbsRun(crf, blocksFunction, choiceFunction, xs, samples = 500 ):
    r"""
    Produce samples from the distribution using Gibbs sampling.
    @params crf LinearChainCRF - the CRF model.
    @params blocksFunction function - Takes the input sequence xs and
                returns blocks of variables that should be updated
                together.
    @params choiceFunction function - Takes 
                a) the crf model,
                b) the current block to be updated
                c) the input sequence xs and 
                d) the current tag sequence ys
                and chooses a new value for variables in the block based
                on the conditional distribution 
                p(y_{block} | y_{-block}, x ; \theta).
    @param xs list string - Observation sequence
    @param samples int - Number of samples to generate
    @return generator list string - Generates a list of tag sequences
    """

    # Burn in is the number iterations to run from the initial tag
    # you've chosen before you generate the samples. It basically
    # prevents you from being biased based on your starting tag.
    BURN_IN = 100

    # Intitial value
    ys = [random.choice(crf.TAGS) for _ in xrange(len(xs))]

    # Get blocks
    blocks = blocksFunction(xs)

    # While burning-in, don't actually return any of your samples.
    for _ in xrange(BURN_IN):
        # Pick a 'random' block
        block = random.choice(blocks)
        # Update its values
        choiceFunction( crf, block, xs, ys )

    # Return a sample every epoch here.
    for _ in xrange(samples):
        # Pick a 'random' block
        block = random.choice(blocks)
        # Update its values
        choiceFunction( crf, block, xs, ys )
        # Return a sample
        yield tuple(ys)

def getCRFBlocks(xs):
    """
    Groups variables into blocks that are updated simultaneously.
    In this case, each variable belongs in its own block.
    @params xs - observation sequence
    """
    return range(len(xs))

#################################
# Problem 3c
def chooseGibbsCRF(crf, t, xs, ys ):
    r"""
    Choose a new assignment for y_t from the conditional distribution
    p( y_t | y_{-t} , xs ; \theta).

    @param t int - The index of the variable you want to update, y_t.
    @param xs list string - Observation seqeunce
    @param ys list string - Tag seqeunce

    Tips:
    * You should only use the potentials between y_t and its Markov
      blanket.
    * You don't return anything from this function, just update `ys`
      in place.

    Possibly useful:
    - crf.G 
    - util.multinomial: Given a PDF as a list OR counter, util.multinomial draws
      a sample from this distribution; for example,
      util.multinomial([0.4, 0.3, 0.2, 0.1]) will return 0 with 40%
      probability and 3 with 10% probability.
      Alternatively you could use,
      util.multinomial({'a':0.4, 'b':0.3, 'c':0.2, 'd':0.1}) will return 'a' with 40%
      probability and 'd' with 10% probability.
    """
    # BEGIN_YOUR_CODE (around 17 lines of code expected)
    num = []
    for tag in crf.TAGS:
        if t == 0:
            m = crf.G(t, BEGIN_TAG, tag, xs)
            m = m * crf.G(t+1, tag, ys[t+1],xs)
        elif t == len(xs)-1:
            m = crf.G(t, ys[t-1], tag, xs)
        else:
            m = crf.G(t, ys[t-1], tag, xs)
            m = m * crf.G(t+1, tag, ys[t-1], xs)
                        
        num.append(m)
    num = [i/sum(num) for i in num]
    ys[t] = crf.TAGS[util.multinomial(num)]
                    
    # END_YOUR_CODE

#################################
# Problem 3c
def computeGibbsProbabilities(crf, blocksFunction, choiceFunction, xs, samples = 2000):
    """
    Empirically estimate the probabilities of various tag sequences. You
    should count the number of labelings over many samples from the
    Gibbs sampler.
    @param xs list string - Observation sequence
    @param samples int - Number of epochs to produce samples
    @return Counter - A counter of tag sequences with an empirical
                      estimate of their probabilities.
    Example output:
        Counter({
        ('-FEAT-', '-SIZE-', '-SIZE-'): 0.379, 
        ('-SIZE-', '-SIZE-', '-SIZE-'): 0.189, 
        ('-FEAT-', '-SIZE-', '-FEAT-'): 0.166, 
        ('-SIZE-', '-SIZE-', '-FEAT-'): 0.135, 
        ('-FEAT-', '-FEAT-', '-SIZE-'): 0.053, 
        ('-SIZE-', '-FEAT-', '-SIZE-'): 0.052, 
        ('-FEAT-', '-FEAT-', '-FEAT-'): 0.018, 
        ('-SIZE-', '-FEAT-', '-FEAT-'): 0.008})

    Possibly useful:
    * Counter
    * gibbsRun
    """
    # BEGIN_YOUR_CODE (around 2 lines of code expected)
    particles = Counter(gibbsRun(crf,blocksFunction,choiceFunction,xs,samples))
    Counters.scale(particles, 1.0/sum(particles.values()))
    return particles
    
    # END_YOUR_CODE

#################################
# Problem 3c
def computeGibbsBestSequence(crf, blocksFunction, choiceFunction, xs, samples = 2000):
    """
    Find the best sequence, y^*, the most likely sequence using samples
    from a Gibbs sampler. This gives the same output as crf.computeViterbi.
    @param xs list string - Observation sequence
    @param samples int - Number of epochs to produce samples
    @return list string - The most probable tag sequence estimated using Gibbs.
    Example output:
        ('-FEAT-', '-SIZE-', '-SIZE-')

    Possibly useful:
    * Counter.most_common
    * gibbsRun
    """
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    return Counter(gibbsRun(crf, blocksFunction, choiceFunction, xs, samples)).most_common(1)[0][0]
    # END_YOUR_CODE
            
#################################
# Problem 3e
def getLongRangeCRFBlocks(xs):
    """
    Constructs a list of blocks, where each block corresponds
    to the positions t with the same observed word x_t.
    @param xs list string - observation sequence
    @return list list int - A list of blocks; each block is a list
            of indices 't' which have the same x_t.
            Example: "A A B" would return: [[0,1],[2]].
    """
    # BEGIN_YOUR_CODE (around 7 lines of code expected)
    return [[i for i,word in enumerate(xs) if word == u_word] for u_word in set(xs)]
    # END_YOUR_CODE

#################################
# Problem 3e
def chooseGibbsLongRangeCRF(crf, block, xs, ys ):
    r"""
    Choose a new assignment for every variable in block from the
    conditional distribution p( y_{block} | y_{-block}, xs; \theta).

    @param block list int - List of variable indices that should be jointly updated.
    @param xs list string - Observation sequence
    @param ys list string - Tag sequence

    Tips:
    * In our model, we have a hard potential between all the variables in the
      block constraining them to be equal. You should only need to
      iterate through crf.TAGS once in order to choose a value for y_{block}
      (as opposed to |block| times).
    * You should only use the potentials between y_t and its Markov
      blanket.
    """
    #import nerUtils
    # BEGIN_YOUR_CODE (around 23 lines of code expected)
    nums = []
    for tag in crf.TAGS:
        num = 1
        if 0 in block:
            num = num * crf.G(0, BEGIN_TAG, tag, xs)
        for i in range(1, len(xs)):
            if (i in block) and (i-1 in block):
                num = num * crf.G(i, tag, tag, xs)
            elif (i in block) and (i-1 not in block):
                num = num * crf.G(i, ys[i-1], tag, xs)
            elif (i not in block) and (i-1 in block):
                num = num * crf.G(i, tag, ys[i], xs)
        nums.append(num)
    nums = [i/sum(nums) for i in nums]
    tag = crf.TAGS[util.multinomial(nums)]
    for t in block: ys[t] = tag
    # END_YOUR_CODE

######################
# Example to help you debug
simpleCRF = LinearChainCRF( ["-FEAT-", "-SIZE-"], 
        binaryFeatureFunction,
        Counter({
            ("-FEAT-", "-SIZE-") : 0.8,
            ("-SIZE-", "-FEAT-") : 0.5,
            ("-SIZE-", "-SIZE-") : 1.,
            ("-FEAT-", "Beautiful") : 1.,
            ("-SIZE-", "Beautiful") : 0.5,
            ("-FEAT-", "2") : 0.5,
            ("-SIZE-", "2") : 1.0,
            ("-FEAT-", "bedroom") : 0.5,
            ("-SIZE-", "bedroom") : 1.0,}))
exampleInput = "Beautiful 2 bedroom".split()
exampleTags = "-FEAT- -SIZE- -SIZE-".split()
