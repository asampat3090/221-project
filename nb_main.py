import glob, os, random
import sys, time
from features import *
from loadExamples import *
from nb import *

"""
ARGUMENTS:
numLabels:              0 means no preference. 1 - n means "only draw examples from numLabels most popular"
numTrainSongs:       how many songs to use for training
numTestSongs:        how many songs to use for testing
'artist' or 'genre'      which one to classify
"""

def nb():
    lastTime = time.clock()
    
    #If arguments were given, read them in:
    if len(sys.argv) == 5:
        numLabels = int(sys.argv[1])
        numTrainSongs = int(sys.argv[2])
        numTestSongs = int(sys.argv[3])
        if sys.argv[4] == 'artist':
            isArtist = 1
        elif sys.argv[4] == 'genre':
            isArtist = 0
        else:
            print "Error, last argument must be either 'genre' or 'artist'!"
    else:
        print "Main function takes 4 arguments: numLabels, numTrainSongs, numTestSongs, artist/genre"
        print "Using defaults instead: 5 200 100 'genre'"
        numLabels = 5
        numTrainSongs = 200
        numTestSongs = 100
        isArtist = 0
    
    #Load lyrics, genres, and artists
    if isArtist:
        os.chdir("lyrics/artist/")
        trainSongs, testSongs, labels = getExamples(numLabels, numTrainSongs, numTestSongs, glob.glob("*.txt"), isArtist)
    else:
        os.chdir("lyrics/genre/")
        trainSongs, testSongs, labels = getExamples(numLabels, numTrainSongs, numTestSongs, glob.glob("*.txt"), isArtist)

    thisTime = time.clock()
    print "Load examples: ", thisTime - lastTime, ' s'
    lastTime = thisTime
        
    #ARTIST!
    if isArtist:
        trainFeaturesAndLabels = [(extractUnigramFeatures(lyrics), artist) for (lyrics, artist) in trainSongs]
        testFeaturesAndLabels = [(extractUnigramFeatures(lyrics), artist) for (lyrics, artist) in testSongs]                                         
        
    #Genre!
    else:
        trainFeaturesAndLabels = [(extractUnigramFeatures(lyrics), genre) for (lyrics, genre) in trainSongs]
        testFeaturesAndLabels = [(extractUnigramFeatures(lyrics), genre) for (lyrics, genre) in testSongs] 
    
    thisTime = time.clock()
    print "Extract features: ", thisTime - lastTime, ' s'
    lastTime = thisTime    
        
    #Train classifier
    nbClassifier = nbTrain(trainFeaturesAndLabels, labels)
    
    print "LogProbY: ", nbClassifier.logProbY
    print "LogProbXGivenY: ", nbClassifier.logProbXGivenY
    
    thisTime = time.clock()
    print "Train Classifier: ", thisTime - lastTime, ' s'
    lastTime = thisTime
    
    #Test for errors
    trainError = nbClassifier.getErrorRate(trainFeaturesAndLabels)
    testError = nbClassifier.getErrorRate(testFeaturesAndLabels)
    
    thisTime = time.clock()
    print "Error checking: ", thisTime - lastTime, ' s'
    lastTime = thisTime
    
    print "Train Error: ", trainError     
    print "Test Error: ", testError, " with", len(labels), "labels"        
        
if __name__ == "__main__":
    nb()