import random
from loadExamples import *
import time
import string
from collections import Counter

"""
This class deals with parsing the lyric files and extracting the features.
"""
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
            bigrams.update([x for x in wordList if x not in set(string.punctuation)]) #add unigrams
            firstWord = "-BEGIN- " + wordList[0]; #add first word
            bigrams.update([firstWord])
            for i, word in enumerate(wordList[:-1]): #add bigrams
                    if word not in set(string.punctuation): 
                        # add bigrams
                        if wordList[i+1] not in set(string.punctuation):
                            newWord = word + " " + wordList[i+1]
                            bigrams.update([newWord]) #add all non-punctuation bigrams 
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
  
def getDict(minNumberOfSongs, maxNumberOfSongs, trainSongs, gram):
    """
    Get a dictionary of features that appear in [minNumberOfSongs, maxNumberOfSongs]
    @param int min number of songs
    @param int max number of songs
    @param list of song objects training songs
    @param string unigram, bigram, trigram, or fourgram
    """

    print "Total songs = ", len(trainSongs)
    vocab = Counter()
    
    for song in trainSongs:
        if gram == 'unigram':
            thisSong = list(extractUnigramFeatures(song[0]))
        elif gram == 'bigram':
            thisSong = list(extractBigramFeatures(song[0]))
        elif gram == 'trigram':
            thisSong = list(extractTrigramFeatures(song[0]))
        elif gram == 'fourgram':
            thisSong = list(extractFourgramFeatures(song[0]))        
        vocab.update(thisSong)     
        
    #Grab words that show up in at least 2 songs, but not more than 1948 songs (half)
    words = [word for word in vocab if minNumberOfSongs <= vocab[word] <= maxNumberOfSongs]
    print "number of words was ", len(vocab), "and is now", len(words)
    return words