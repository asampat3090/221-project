import glob, os, random
import sys, time
from Classifier import *
from features import *
from loadExamples import *
from features import *

"""
ARGUMENTS:
numLabels:              0 means no preference. 1 - n means "only draw examples from numLabels most popular"
numTrainSongs:       how many songs to use for training
numTestSongs:        how many songs to use for testing
trainingIters:            number of iterations through all the training songs during SGD
alpha:                      an int from 0 - 100 that will be devided by 100 to obtain the learning rate.
B:                            the regularization parameter, if set to something higher than 0, norm(w) will never exeed B
'artist' or 'genre'      which one to classify

"""

def main():
    lastTime = time.clock()
    
    #If arguments were given, read them in:
    #Arguments are: numTrain, numTest, trainingIter, alpha
    if len(sys.argv) == 8:
        numLabels = int(sys.argv[1])
        numTrainSongs = int(sys.argv[2])
        numTestSongs = int(sys.argv[3])
        trainingIters = int(sys.argv[4])
        alpha = 1.0*int(sys.argv[5])/100
        B = int(sys.argv[6])
        if sys.argv[7] == 'artist':
            isArtist = 1
        elif sys.argv[7] == 'genre':
            isArtist = 0
        else:
            print "Error, last argument must be either 'genre' or 'artist'!"
    else:
        print "Main function takes 7 arguments: numLabels, numTrainSongs, numTestSongs, trainingIters, alpha, B, artist/genre"
        print "Using defaults instead: 0 20 20 10 90 0 'genre' (alpha = 90/100 = .9)"
        numLabels = 0 #no preference
        numTrainSongs = 20
        numTestSongs = 20
        trainingIters = 10
        alpha = 0.9
        B = 0
        isArtist = 0
    
    #Load lyrics, genres, and artists
    if isArtist:
        os.chdir("lyrics/artist/")
        trainSongs, testSongs, artistLabels = getExamples(numLabels, numTrainSongs, numTestSongs, glob.glob("*.txt"), isArtist)
    else:
        os.chdir("lyrics/genre/")
        trainSongs, testSongs, genreLabels = getExamples(numLabels, numTrainSongs, numTestSongs, glob.glob("*.txt"), isArtist)

    thisTime = time.clock()
    print "Load examples: ", thisTime - lastTime, ' s'
    lastTime = thisTime

    #ARTIST!
    if isArtist:
        #Extract features

        artistTrainFeaturesAndLabels = [(extractTrigramFeatures(lyrics), artist) for (lyrics, artist) in trainSongs]
        artistTestFeaturesAndLabels = [(extractTrigramFeatures(lyrics), artist) for (lyrics, artist) in testSongs]

        thisTime = time.clock()
        print "Extract artist features: ", thisTime - lastTime, ' s'
        lastTime = thisTime
            
        #Train classifier
        artistClassifier = trainMultiClassClassifier(artistTrainFeaturesAndLabels, artistLabels, logisticH, trainingIters, alpha, B)
        thisTime = time.clock()
        print "Train Artist Classifier: ", thisTime - lastTime, ' s'
        lastTime = thisTime
        
        #Test for errors
        aTrainError = artistClassifier.getErrorRate(artistLabels, artistTrainFeaturesAndLabels)
        aTestError = artistClassifier.getErrorRate(artistLabels, artistTestFeaturesAndLabels)
        thisTime = time.clock()
        print "Error checking: ", thisTime - lastTime, ' s'
        lastTime = thisTime
        
        print "Artist Train Error: ", aTrainError     
        print "Artist Test Error: ", aTestError, " with", len(artistLabels), "artist labels"        
        
    #GENRE!
    else:
        #Features
        genreTrainFeaturesAndLabels = [(extractBigramFeatures(lyrics), genre) for (lyrics, genre) in trainSongs]
        genreTestFeaturesAndLabels = [(extractBigramFeatures(lyrics), genre) for (lyrics, genre) in testSongs]
        thisTime = time.clock()
        print "Extract genre features: ", thisTime - lastTime, ' s'
        lastTime = thisTime
            
        #Train classifier
        genreClassifier = trainMultiClassClassifier(genreTrainFeaturesAndLabels, genreLabels, logisticH, trainingIters, alpha, B)
        thisTime = time.clock()
        print "Train genre Classifier: ", thisTime - lastTime, ' s'
        lastTime = thisTime
        
        #Test for errors
        gTrainError = genreClassifier.getErrorRate(genreLabels, genreTrainFeaturesAndLabels)
        gTestError = genreClassifier.getErrorRate(genreLabels, genreTestFeaturesAndLabels)
        thisTime = time.clock()
        print "Error checking: ", thisTime - lastTime, ' s'    
        lastTime = thisTime
      
        print "Genre Train Error: ", gTrainError
        print "Genre Test Error: ", gTestError, " with", len(genreLabels), "genre labels"

if __name__ == "__main__":
    main()