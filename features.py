import random
from loadExamples import *
import time
import string


"""
This class deals with parsing the lyric files and extracting the features.
"""
from collections import Counter

def extractUnigramFeatures(x):
    #Clean up the string x
    x = ''.join(char for char in x if char not in set(string.punctuation))
    x = x.lower()
    
    unigrams = Counter()
    unigrams.update([word for word in x.split()])

    return unigrams

def extractBigramFeatures(x):
    """
    Extract unigram + bigram features for a text document $x$. 

    @param string x: represents the contents of lyrics.
    @return dict: feature vector representation of x.
    """
    #Clean up string
    x = ''.join(char for char in x if char not in set(string.punctuation))
    x = x.lower()    

    bigrams = Counter()
    bigrams.update([word for word in x.split()]) #do unigrams
    
    #Split on sentences
    sentenceList = x.split('\n')
    for sentence in sentenceList:
        wordList = sentence.split()
        if (len(wordList) > 0):
            bigrams.update([''.join(ch for ch in x if ch not in punctuationSet) for x in wordList if x not in punctuationSet]) #add unigrams
            firstWord = "-BEGIN- " + wordList[0]; #add first word
            bigrams.update([''.join(ch for ch in firstWord if ch not in punctuationSet)])
            for i, word in enumerate(wordList[:-1]): #add bigrams
                    if word not in punctuationSet: 
                        # add bigrams
                        if wordList[i+1] not in punctuationSet:
                            newWord = word + " " + wordList[i+1]
                            bigrams.update([''.join(ch for ch in newWord if ch not in punctuationSet)]) #add all non-punctuation bigrams 
    return bigrams

def extractTrigramFeatures(x):
    """
    Extract trigram features for a text document $x$. 

    @param string x: represents the contents of an email message.
    @return dict: feature vector representation of x.
    """    
    
    #Clean up string
    x = ''.join(char for char in x if char not in set(string.punctuation))
    x = x.lower()      

    trigrams = Counter()
    trigrams.update([word for word in x.split()]) #do unigrams
    
    #Split on newlines 
    lines = x.split('\n')
    for line in lines:
        wordList = line.split()
        if len(wordList) == 0: continue
        trigrams.update(["-BEGIN- " + wordList[0]]) # add bigram first word
        trigrams.update(["-BEGIN- "+"-BEGIN- "+wordList[0]]) # add trigram first word
        if len(wordList) == 1: continue
        trigrams.update(["-BEGIN- " + wordList[0] + wordList[1]]) #trigram second word
        if len(wordList) == 2: continue

        # Add the rest of the trigrams
        for i, word in enumerate(wordList[:-2]): 
            # add bigrams 
            trigrams.update([word + " " + wordList[i+1]])
            # add trigrams
            trigrams.update([word + " " + wordList[i+1] + " " + wordList[i+2]]) #add all non-punctuation trigrams
        # add final bigram 
        trigrams.update([wordList[-2]+" "+wordList[-1]])
    return trigrams

def extractFourgramFeatures(x):
    """
    Extract fourgram features for a text document $x$. 

    @param string x: represents the contents of an email message.
    @return dict: feature vector representation of x.
    """
    #Clean up string
    x = ''.join(char for char in x if char not in set(string.punctuation))
    x = x.lower() 
    
    fourgrams = Counter()
    fourgrams.update([word for word in x.split()]) #do unigrams
    
    #Split on newLines
    lines = x.split('\n')
    for line in lines:
        wordList = line.split()
        if len(wordList) > 0:
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
                # add bigrams 
                newWord = word + " " + wordList[i+1]
                fourgrams.update([newWord]) #add all non-punctuation bigrams           
                # add trigrams
                newWord = word + " " + wordList[i+1] + " " + wordList[i+2]
                fourgrams.update([newWord]) #add all non-punctuation trigrams   
                # add fourgrams
                newWord = word + " " + wordList[i+1] + " " + wordList[i+2] + " " + wordList[i+3]
                fourgrams.update([newWord]) #add all non-punctuation trigrams
            
            # Add the final Trigram
            fourgrams.update([wordList[-3] + " " + wordList[-2]+" "+wordList[-1]])
            # Add the two final Bigrams
            fourgrams.update([wordList[-3] + " " + wordList[-2]])
            fourgrams.update([wordList[-2]+" "+wordList[-1]])

    return fourgrams

            
            
            
    