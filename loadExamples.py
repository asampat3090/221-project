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