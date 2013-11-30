import random
from loadExamples import *
import time


"""
This class deals with parsing the lyric files and extracting the features.
"""
from collections import Counter

def extractBigramFeatures(x):
    """
    artistTestFeaturesAndLabels = [(ex
    Extract unigram + bigram features for a text document $x$. 

    @param string x: represents the contents of an email message.
    @return dict: feature vector representation of x.
    """
    # BEGIN_YOUR_CODE (around 12 lines of code expected)

    punctuationSet = set('!@#$%^&*()_+-={}[]|\:;/?.,><~`')
    endOfSentenceSet = set('.?!')
    bigrams = Counter()
    
    #Split on sentences
    sentenceList = x.split('\n')
    for sentence in sentenceList:
        wordList = sentence.split()
        if (len(wordList) > 0):
            bigrams.update([x for x in wordList if x not in punctuationSet]) #add unigrams
            firstWord = "-BEGIN- " + wordList[0]; #add first word
            bigrams.update([firstWord])
            for i, word in enumerate(wordList[:-1]): #add bigrams
                    if word not in punctuationSet: 
                        # add bigrams
                        if wordList[i+1] not in punctuationSet:
                            newWord = word + " " + wordList[i+1]
                            bigrams.update([newWord]) #add all non-punctuation bigrams 
    return bigrams


def extractUnigramFeatures(x):
    unigrams = Counter()
    unigrams.update([word for word in x.split()])
    return unigrams

def extractTrigramFeatures(x):
    """
    Extract trigram features for a text document $x$. 

    @param string x: represents the contents of an email message.
    @return dict: feature vector representation of x.
    """    
    
    punctuationSet = set('!@#$%^&*()_+-={}[]|\:;/?.,><~`')
    endOfSentenceSet = set('.?!')    
    trigrams = Counter()
    
    #Split on newlines 
    lines = x.split('\n')
    for line in lines:
        wordList = line.split()
        if len(wordList)>0: 
            # add unigram features features
            trigrams.update([x for x in wordList if x not in punctuationSet]) #add unigrams
            trigrams.update(["-BEGIN- " + wordList[0]]) # add bigram first word
            trigrams.update(["-BEGIN- "+"-BEGIN- "+wordList[0]]) # add first word 
        if len(wordList)>1:
            trigrams.update(["-BEGIN- "+wordList[0]+" "+wordList[1]])# add second word
        if len(wordList)>2:
            # Add the rest of the trigrams
            for i, word in enumerate(wordList[:-2]):
                if word not in punctuationSet: 
                    # add bigrams 
                    if wordList[i+1] not in punctuationSet:
                        newWord = word + " " + wordList[i+1]
                        trigrams.update([newWord]) #add all non-punctuation bigrams          
                    # add trigrams
                    if wordList[i+1] not in punctuationSet and wordList[i+2] not in punctuationSet:
                        newWord = word + " " + wordList[i+1] + " " + wordList[i+2]
                        trigrams.update([newWord]) #add all non-punctuation trigrams
            # add final bigram 
            trigrams.update([wordList[-2]+" "+wordList[-1]])
    return trigrams

def extractFourgramFeatures(x):
    """
    Extract fourgram features for a text document $x$. 

    @param string x: represents the contents of an email message.
    @return dict: feature vector representation of x.
    """
    punctuationSet = set('!@#$%^&*()_+-={}[]|\:;/?.,><~`')
    endOfSentenceSet = set('.?!') 
    fourgrams = Counter()
    
    #Split on newLines
    lines = x.split('\n')
    for line in lines:
        wordList = line.split()
        if len(wordList) > 0:
            fourgrams.update([x for x in wordList if x not in punctuationSet]) #add unigrams
            fourgrams.update(["-BEGIN- "+wordList[0]]) # add bigram first word 
            fourgrams.update(["-BEGIN- "+"-BEGIN- "+wordList[0]]) # add trigram first word 
            fourgrams.update(["-BEGIN- "+"-BEGIN- "+"-BEGIN- "+wordList[0]]) # add fourgram first word 
        if len(wordList) > 1:
            fourgrams.update(["-BEGIN- "+wordList[0]+" "+wordList[1]])# add trigram second word
            fourgrams.update(["-BEGIN- "+"-BEGIN- "+wordList[0]+" "+wordList[1]])# add fourgram second word 
        if len(wordList) > 2:
            fourgrams.update(["-BEGIN- "+wordList[0]+" "+wordList[1]+" "+wordList[2]]) # add third word 
        if len(wordList) > 3:
            # Add the rest of the trigrams
            for i, word in enumerate(wordList[:-3]):
                if word not in punctuationSet: 
                    # add bigrams 
                    if wordList[i+1] not in punctuationSet:
                        newWord = word + " " + wordList[i+1]
                        fourgrams.update([newWord]) #add all non-punctuation bigrams           
                    # add trigrams
                    if wordList[i+1] not in punctuationSet and wordList[i+2] not in punctuationSet:
                        newWord = word + " " + wordList[i+1] + " " + wordList[i+2]
                        fourgrams.update([newWord]) #add all non-punctuation trigrams   
                    # add fourgrams
                    if wordList[i+1] not in punctuationSet and wordList[i+2] not in punctuationSet and wordList[i+3] not in punctuationSet:
                        newWord = word + " " + wordList[i+1] + " " + wordList[i+2] + " " + wordList[i+3]
                        fourgrams.update([newWord]) #add all non-punctuation trigrams
            # Add the final Trigram
            fourgrams.update([wordList[-3] + " " + wordList[-2]+" "+wordList[-1]])
            # Add the two final Bigrams
            fourgrams.update([wordList[-3] + " " + wordList[-2]])
            fourgrams.update([wordList[-2]+" "+wordList[-1]])
    return fourgrams

            
            
            
    