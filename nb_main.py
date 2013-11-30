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
featureExtractor       which feature extractor to use (unigram, bigram, etc)
"""

def nb():
    lastTime = time.clock()
    
    #If arguments were given, read them in:
    if len(sys.argv) == 6:
        numLabels = int(sys.argv[1])
        numTrainSongs = int(sys.argv[2])
        numTestSongs = int(sys.argv[3])
        if sys.argv[4] == 'artist':
            isArtist = 1
        elif sys.argv[4] == 'genre':
            isArtist = 0
        else:
            print "Error, 2nd to last argument must be either 'genre' or 'artist'!"
        featureExtractor = sys.argv[5]
    else:
        print "Main function takes 4 arguments: numLabels, numTrainSongs, numTestSongs, artist/genre"
        print "Using defaults instead: 5 200 100 'genre' 'trigram'"
        numLabels = 5
        numTrainSongs = 200
        numTestSongs = 100
        isArtist = 0
        featureExtractor = 'trigram'
    
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
        #Extracted features based on system arg 
        if featureExtractor == 'unigram':
            artistTrainFeaturesAndLabels = [(extractUnigramFeatures(lyrics), artist) for (lyrics, artist) in trainSongs]
            artistTestFeaturesAndLabels = [(extractUnigramFeatures(lyrics), artist) for (lyrics, artist) in testSongs]   
        elif featureExtractor == 'bigram':
            artistTrainFeaturesAndLabels = [(extractBigramFeatures(lyrics), artist) for (lyrics, artist) in trainSongs]
            artistTestFeaturesAndLabels = [(extractBigramFeatures(lyrics), artist) for (lyrics, artist) in testSongs]                
        elif featureExtractor == 'trigram':
            artistTrainFeaturesAndLabels = [(extractTrigramFeatures(lyrics), artist) for (lyrics, artist) in trainSongs]
            artistTestFeaturesAndLabels = [(extractTrigramFeatures(lyrics), artist) for (lyrics, artist) in testSongs]                  
        else: 
            artistTrainFeaturesAndLabels = [(extractFourgramFeatures(lyrics), artist) for (lyrics, artist) in trainSongs]
            artistTestFeaturesAndLabels = [(extractFourgramFeatures(lyrics), artist) for (lyrics, artist) in testSongs]                                      
        thisTime = time.clock()
        print "Extract artist features: ", thisTime - lastTime, ' s'
        lastTime = thisTime
            
        #Train classifier
        logProbXGivenY, logProbY = nbTrain(artistTrainFeaturesAndLabels, artistLabels)
        print "Train Artist Classifier: ", thisTime - lastTime, ' s'
        lastTime = thisTime
        
        #Test for errors
        aTrainError = 0
        aTestError = 0
        thisTime = time.clock()
        print "Error checking: ", thisTime - lastTime, ' s'
        lastTime = thisTime
        
        print "Artist Train Error: ", aTrainError     
        print "Artist Test Error: ", aTestError, " with", len(artistLabels), "artist labels"        
        
    #GENRE!
    else:
        #Features
        #Extracted features based on system arg 
        if featureExtractor == 'unigram':
            genreTrainFeaturesAndLabels = [(extractUnigramFeatures(lyrics), genre) for (lyrics, genre) in trainSongs]
            genreTestFeaturesAndLabels = [(extractUnigramFeatures(lyrics), genre) for (lyrics, genre) in testSongs]     
        elif featureExtractor == 'bigram':
            genreTrainFeaturesAndLabels = [(extractBigramFeatures(lyrics), genre) for (lyrics, genre) in trainSongs]
            genreTestFeaturesAndLabels = [(extractBigramFeatures(lyrics), genre) for (lyrics, genre) in testSongs]                
        elif featureExtractor == 'trigram':
            genreTrainFeaturesAndLabels = [(extractTrigramFeatures(lyrics), genre) for (lyrics, genre) in trainSongs]
            genreTestFeaturesAndLabels = [(extractTrigramFeatures(lyrics), genre) for (lyrics, genre) in testSongs]                      
        else: 
            genreTrainFeaturesAndLabels = [(extractFourgramFeatures(lyrics), genre) for (lyrics, genre) in trainSongs]
            genreTestFeaturesAndLabels = [(extractFourgramFeatures(lyrics), genre) for (lyrics, genre) in testSongs]                        
        thisTime = time.clock()
        print "Extract genre features: ", thisTime - lastTime, ' s'
        lastTime = thisTime
            
        #Train classifier
        
        thisTime = time.clock()
        print "Train genre Classifier: ", thisTime - lastTime, ' s'
        lastTime = thisTime
        
        #Test for errors
        gTrainError = 0
        gTestError = 0
        thisTime = time.clock()
        print "Error checking: ", thisTime - lastTime, ' s'    
        lastTime = thisTime
      
        print "Genre Train Error: ", gTrainError
        print "Genre Test Error: ", gTestError, " with", len(genreLabels), "genre labels"

if __name__ == "__main__":
    nb()