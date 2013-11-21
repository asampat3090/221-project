"""
This class deals with parsing the lyric files and extracting the features.
"""
from collections import Counter
import random

def getExamples(numTrain, numTest, files):
    '''
    Parses the files to get the number of required training and testing examples. Returns 2 lists, each of
    (lyrics, artist, genre) tuples and 2 sets: artsts and genre. The sets only have one of each artist or genre.
    
    @param number of files to use for training
    @param number of files to use for testing
    @param a list of files with the data inside
    
    @return (trainSongs, testSongs, artistLabels, genreLabels) where *examples are lists of (lyrics, artist, genre)
            and *Labels are lists of unique labels
    '''
    
    totalNum = numTrain + numTest
    percentTrain = 1.0*numTrain/totalNum
    
    testSongs = []
    trainSongs = []
    artistLabels = set()
    genreLabels = set()
    usedIndices = []

    for i in range(totalNum):
        #keep drawing random numbers until we hit one that we haven't already used
        while True:
            nextIndex = random.randint(0,len(files)-1)
            if not any(nextIndex == index for index in usedIndices): break
        usedIndices.append(nextIndex)
        
        #read in the song
        file = open(files[nextIndex], 'r')
        artist = file.readline().split('\n')[0]
        genre = file.readline().split('\n')[0]
        lyrics = file.read()
        
        #put it into test or train
        if len(trainSongs) < numTrain:
            trainSongs.append((lyrics, artist, genre))
        else:
            testSongs.append((lyrics, artist, genre))
        
        #add to set of genre and artist labels
        artistLabels.add(artist)
        genreLabels.add(genre)
    return trainSongs, testSongs, list(artistLabels), list(genreLabels)


def extractBigramFeatures(x):
    """
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
                        if wordList[i+1] not in punctuationSet:
                            newWord = word + " " + wordList[i+1]
                            bigrams.update([newWord]) #add all non-punctuation bigrams
    return bigrams


def extractUnigrams(x):
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
            trigrams.update(extractBigramFeatures(x)) # add bigram features     
            trigrams.update(["-BEGIN- "+"-BEGIN- "+wordList[0]]) # add first word 
            trigrams.update(["-BEGIN- "+wordList[0]+" "+wordList[1]])# add second word
            # Add the rest of the trigrams
            for i, word in enumerate(wordList[:-2]):
                if word not in punctuationSet: 
                    if wordList[i+1] not in punctuationSet and wordList[i+2] not in punctuationSet:
                        newWord = word + " " + wordList[i+1] + " " + wordList[i+2]
                    trigrams.update([newWord]) #add all non-punctuation trigrams            
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
            fourgrams.update(extractTrigramFeatures(x)) # add trigram features
            fourgrams.update(["-BEGIN- "+"-BEGIN- "+"-BEGIN- "+wordList[0]]) # add first word 
            fourgrams.update(["-BEGIN- "+"-BEGIN- "+wordList[0]+" "+wordList[1]])# add second word 
            fourgrams.update(["-BEGIN- "+wordList[0]+" "+wordList[1]+" "+wordList[2]]) # add third word 
            # Add the rest of the trigrams
            for i, word in enumerate(wordList[:-3]):
                if word not in punctuationSet: 
                    if wordList[i+1] not in punctuationSet and wordList[i+2] not in punctuationSet and wordList[i+3] not in punctuationSet:
                        newWord = word + " " + wordList[i+1] + " " + wordList[i+2] + " " + wordList[i+3]
                    fourgrams.update([newWord]) #add all non-punctuation trigrams
    return fourgrams