"""
This class deals with parsing the lyric files and extracting the features.
"""
from collections import Counter
import random

def getExamples(numTrain, numTest, files, isArtist):
    '''
    Parses the files to get the number of required training and testing examples. Returns 2 lists, each of
    (lyrics, artist, genre) tuples and 2 sets: artsts and genre. The sets only have one of each artist or genre.
    
    @param number of files to use for training
    @param number of files to use for testing
    @param a list of files with the data inside
    @param int: 1 if looking at artist, 0 if looking at genre
    
    @return (trainSongs, testSongs, labels) where *Songs are lists of (lyrics, labels)
            and labels are lists of unique labels
    '''
    
    totalNum = numTrain + numTest
    percentTrain = 1.0*numTrain/totalNum
    
    testSongs = []
    trainSongs = []
    labels = set()
    usedIndices = []
    labelCounter = []
    
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
        
        #Add the label to the label counter and put the (lyric, label) tuple into
        #test or train data. Update the labels set.
        if isArtist: 
            labelCounter.append(artist)
            if len(trainSongs) < numTrain:
                trainSongs.append((lyrics, artist))
            else:
                testSongs.append((lyrics, artist))   
            labels.add(artist)

        else: 
            labelCounter.append(genre)
            if len(trainSongs) < numTrain:
                trainSongs.append((lyrics, genre))
            else:
                testSongs.append((lyrics, genre))   
            labels.add(genre)            
    
    #Print the counter so we know how many of each label we have        
    labelCounter = Counter(labelCounter)
    for label in labelCounter:
        print label, labelCounter[label]
        
    return trainSongs, testSongs, list(labels)


