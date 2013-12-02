"""
This class deals with parsing the lyric files and extracting the features.
"""
from collections import Counter
import random

def getExamples(numLabels, numTrain, numTest, files, isArtist):
    '''
    Parses the files to get the number of required training and testing examples. Returns 2 lists, each of
    (lyrics, label) tuples and a set of unique labels (artists or genres). The sets only have one of each artist or genre.
    
    @param number of files to use for training
    @param number of files to use for testing
    @param a list of files with the data inside
    @param int: 1 if looking at artist, 0 if looking at genre
    
    @return (trainSongs, testSongs, labels) where *Songs are lists of (lyrics, labels)
            and labels are lists of unique labels
    '''
    #Read in all the files with lyric length > 10
    songs = []
    labels = set()
    labelCounter = Counter()
    
    for i in range(len(files)-1):
        file = open(files[i], 'r')
        artist = file.readline().split('\n')[0]
        genre = file.readline().split('\n')[0]
        lyrics = file.read()
        
        if len(lyrics) < 10:
            print file.name
            continue
        
        if len(artist) > 5:
            artist = artist[0:5]
        if len(genre) > 5:
            genre = genre[0:5]
        
        if isArtist:
            songs.append((lyrics, artist))
            labels.add(artist)
            labelCounter.update([artist])
            
        else:
            songs.append((lyrics, genre))
            labels.add(genre)
            labelCounter.update([genre])
    
    #if numLabels is a reasonable number, make a list of the top numLabels most popular labels
    if 0 < numLabels <= len(labels):
        useLabels = [label for (label, count) in labelCounter.most_common(numLabels)]
    
    #otherwise just use all labels with at least 20 songs
    else:
        useLabels = [label for label in labelCounter if labelCounter[label] > 19]
        
    #Print labels and their counts, add up total number of usable songs
    numUsableSongs = 0
    for label in useLabels:
        print label, labelCounter[label]
        numUsableSongs += labelCounter[label]
        
    #Make sure we have enough songs...
    totSongs = numTest + numTrain
    percentTrain = numTrain*1.0/totSongs
    if totSongs > numUsableSongs:
        print "Requested", totSongs, "but only have", numUsableSongs
        return
    
    usedIndices = []
    trainSongs = []
    testSongs = []

    #randomly select songs, make sure they are ok, and put them in test and train songs.
    while (len(trainSongs) + len(testSongs) < totSongs):  
        #randomly get a new index
        while True:
            nextIndex = random.randint(0,len(songs)-1)
            if not any(nextIndex == index for index in usedIndices): break
        usedIndices.append(nextIndex)
        
        #ignore song and start over if label is one of the labels to ignore
        if songs[nextIndex][1] not in useLabels: continue
        
        #otherwise add it to test or train
        if len(trainSongs) < numTrain:
            trainSongs.append((songs[nextIndex][0], songs[nextIndex][1]))
        else:
            testSongs.append((songs[nextIndex][0], songs[nextIndex][1]))
    
    return (trainSongs, testSongs, useLabels)