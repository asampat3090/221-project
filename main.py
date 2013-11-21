import glob, os, random
import sys, time
from Classifier import *
from loadExamples import *

def main():
    lastTime = time.clock()
    
    #If arguments were given, read them in:
    #Arguments are: numTrain, numTest, trainingIter, alpha
    if len(sys.argv) == 5:
        numTrainSongs = int(sys.argv[1])
        if (numTrainSongs > 1400):
            print 'Too many songs requested!'
            return
        numTestSongs = int(sys.argv[2])
        if (numTestSongs + numTrainSongs > 1400):
            print 'Too many songs requested!'
            return
        trainingIters = int(sys.argv[3])
        alpha = 1.0*int(sys.argv[4])/100
    else:
        print "Main function takes 4 arguments: numTrainSongs, numTestSongs, trainingIters, and alpha"
        print "Using defaults instead: 20 20 10 90 (alpha = 90/100 = .9)"
        numTrainSongs = 20
        numTestSongs = 20
        trainingIters = 10
        alpha = 0.9
    
    #Load lyrics, genres, and artists
    os.chdir("lyrics/")
    trainSongs, testSongs, artistLabels, genreLabels = getExamples(numTrainSongs, numTestSongs, glob.glob("*.txt"))
    thisTime = time.clock()
    print "Load examples: ", thisTime - lastTime, ' s'
    lastTime = thisTime
    print "Genres: ", genreLabels

    #ARTIST!
    ##Extract features
    #artistTrainFeaturesAndLabels = [(extractBigramFeatures(lyrics), artist) for (lyrics, artist, genre) in trainSongs]
    #artistTestFeaturesAndLabels = [(extractBigramFeatures(lyrics), artist) for (lyrics, artist, genre) in testSongs]
    #thisTime = time.clock()
    #print "Extract artist features: ", lastTime - thisTime, ' s'
    #lastTime = thisTime
        
    ##Train classifier
    #artistClassifier = trainMultiClassClassifier(artistTrainFeaturesAndLabels, artistLabels, logisticH, trainingIters, alpha)
    #thisTime = time.clock()
    #print "Train Artist Classifier: ", thisTime - lastTime, ' s'
    #lastTime = thisTime
    
    ##Test for errors
    #aTrainError = artistClassifier.getErrorRate(artistTrainFeaturesAndLabels)
    #aTestError = artistClassifier.getErrorRate(artistTestFeaturesAndLabels)
    #thisTime = time.clock()
    #print "Error checking: ", testTime - trainTime, ' s'
    #lastTime = thisTime
        
    #GENRE!
    #Features
    genreTrainFeaturesAndLabels = [(extractBigramFeatures(lyrics), genre) for (lyrics, artist, genre) in trainSongs]
    genreTestFeaturesAndLabels = [(extractBigramFeatures(lyrics), genre) for (lyrics, artist, genre) in testSongs]
    thisTime = time.clock()
    print "Extract genre features: ", thisTime - lastTime, ' s'
    lastTime = thisTime
        
    #Train classifier
    genreClassifier = trainMultiClassClassifier(genreTrainFeaturesAndLabels, genreLabels, logisticH, trainingIters, alpha)
    thisTime = time.clock()
    print "Train genre Classifier: ", thisTime - lastTime, ' s'
    lastTime = thisTime
    
    #Test for errors
    gTrainError = genreClassifier.getErrorRate(genreTrainFeaturesAndLabels)
    gTestError = genreClassifier.getErrorRate(genreTestFeaturesAndLabels)
    thisTime = time.clock()
    print "Error checking: ", thisTime - lastTime, ' s'    
    lastTime = thisTime
    
    #print "Artist Train Error: ", aTrainError     
    #print "Artist Test Error: ", aTestError
    print "Genre Train Error: ", gTrainError
    print "Genre Test Error: ", gTestError, " with", len(genreLabels), "genre labels"

if __name__ == "__main__":
    main()