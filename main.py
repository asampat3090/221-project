import glob, os, random, nb
import sys, time
from Classifier import *
from features import *
from loadExamples import *
from feature_selector import *

"""
ARGUMENTS:
numLabels:              0 means no preference. 1 - n means "only draw examples from numLabels most popular"
numTrainSongs:       how many songs to use for training
numTestSongs:        how many songs to use for testing
trainingIters:            number of iterations through all the training songs during SGD
alpha:                      an int from 0 - 100 that will be devided by 100 to obtain the learning rate.
B:                            the regularization parameter, if set to something higher than 0, norm(w) will never exeed B
'artist' or 'genre'       which one to classify
'unigram','bigram','trigram' or 'fourgram' which feature extractor to use.
numFeatures:           how many features do we want to use? - if 0 then just take all.
'nb' or 'gd':              Naive Bayes or Gradient Descents
'log', 'hinge', 'perceptron'   which loss function to use with gradient descent.
'information_gain', 'pca' which feature selection mechanism to use.

"""

def main():
    lastTime = time.clock()
    
    #If arguments were given, read them in:
    #Arguments are: numTrain, numTest, trainingIter, alpha, regularization constant,
    #artist or genre, unigram/bigram/trigram/fourgram, number of features, nb or gd
    #log hinge or perceptron
    if len(sys.argv) == 13:
        numLabels = int(sys.argv[1])
        numTrainSongs = int(sys.argv[2])
        numTestSongs = int(sys.argv[3])
        trainingIters = int(sys.argv[4])
        alpha = 1.0*int(sys.argv[5])/100
        B = int(sys.argv[6])
        isArtist = True if sys.argv[7] == 'artist' else False
        featureExtractor = sys.argv[8]
        numFeatures = int(sys.argv[9])
        useNB = True if sys.argv[10] == 'nb' else False
        if sys.argv[11] == 'perceptron': lossFunc = perceptronH
        elif sys.argv[11] == 'hinge': lossFunc = hingeH
        else: lossFunc = logisticH
        featureSelectionMechanism = sys.argv[12]
        
    else:
        print "Main function takes 10 arguments: numLabels, numTrainSongs, numTestSongs, trainingIters, alpha, B, artist/genre uni/bi/tri/fourgram numFeatures (nb or gd) (perceptron hinge or log)"
        print "Using defaults instead: 0 20 20 10 90 0 'genre' 'bigram' 0 gd logistic pca  (alpha = 90/100 = .9)"
        numLabels = 0 #no preference
        numTrainSongs = 20
        numTestSongs = 20
        trainingIters = 10
        alpha = 0.9
        B = 0
        isArtist = 0
        featureExtractor = 'bigram'
        numFeatures = 0
        useNB = False
        lossFunc = logisticH
        featureSelectionMechanism = 'pca'
    
    #Repeat inputs:
    if useNB: print "Naive Bayes,", numLabels, "labels,", numTrainSongs, "training songs,", numTestSongs, "testing songs,",
    else: print "Gradient descent with", lossFunc, "loss function,", numLabels, "labels,", numTrainSongs, "training songs,", numTestSongs,\
        "testing songs", featureExtractor, "features, use", numFeatures, "features, alpha =", alpha, "B =", B, 
    if isArtist: print "predict artist."
    else: print "predict genre."
    
    #LOAD SONGS
    if isArtist:
        os.chdir("lyrics/artist/")
        trainSongs, testSongs, labels = getExamples(numLabels, numTrainSongs, numTestSongs, glob.glob("*.txt"), isArtist)
    else:
        os.chdir("lyrics/genre/")
        trainSongs, testSongs, labels = getExamples(numLabels, numTrainSongs, numTestSongs, glob.glob("*.txt"), isArtist)

    thisTime = time.clock()
    print "Load examples: ", thisTime - lastTime, ' s'
    lastTime = thisTime
        
    #FEATURE EXTRACTION
    #Gradient Descent:
    #if not useNB:
    if True:
        #Classifying by artist:
        if isArtist:
            if featureExtractor == 'unigram':
                trainFeaturesAndLabels = [(extractUnigramFeatures(lyrics), artist) for (lyrics, artist) in trainSongs]
                testFeaturesAndLabels = [(extractUnigramFeatures(lyrics), artist) for (lyrics, artist) in testSongs]
            elif featureExtractor == 'bigram':
                trainFeaturesAndLabels = [(extractBigramFeatures(lyrics), artist) for (lyrics, artist) in trainSongs]
                testFeaturesAndLabels = [(extractBigramFeatures(lyrics), artist) for (lyrics, artist) in testSongs]                         
            elif featureExtractor == 'trigram':
                trainFeaturesAndLabels = [(extractTrigramFeatures(lyrics), artist) for (lyrics, artist) in trainSongs]
                testFeaturesAndLabels = [(extractTrigramFeatures(lyrics), artist) for (lyrics, artist) in testSongs]                  
            else: 
                trainFeaturesAndLabels = [(extractFourgramFeatures(lyrics), artist) for (lyrics, artist) in trainSongs]
                testFeaturesAndLabels = [(extractFourgramFeatures(lyrics), artist) for (lyrics, artist) in testSongs]
        
        #Classifying by genre:
        else: 
            if featureExtractor == 'unigram':
                trainFeaturesAndLabels = [(extractUnigramFeatures(lyrics), genre) for (lyrics, genre) in trainSongs]
                testFeaturesAndLabels = [(extractUnigramFeatures(lyrics), genre) for (lyrics, genre) in testSongs]                         
            elif featureExtractor == 'bigram':
                trainFeaturesAndLabels = [(extractBigramFeatures(lyrics), genre) for (lyrics, genre) in trainSongs]
                testFeaturesAndLabels = [(extractBigramFeatures(lyrics), genre) for (lyrics, genre) in testSongs]                        
            elif featureExtractor == 'trigram':
                trainFeaturesAndLabels = [(extractTrigramFeatures(lyrics), genre) for (lyrics, genre) in trainSongs]
                testFeaturesAndLabels = [(extractTrigramFeatures(lyrics), genre) for (lyrics, genre) in testSongs]     
            else: 
                trainFeaturesAndLabels = [(extractFourgramFeatures(lyrics), genre) for (lyrics, genre) in trainSongs]
                testFeaturesAndLabels = [(extractFourgramFeatures(lyrics), genre) for (lyrics, genre) in testSongs]         

    thisTime = time.clock()
    print "Extract features: ", thisTime - lastTime, ' s'
    lastTime = thisTime
    
    #FEATURE SELECTION - only for gradient descent
    if useNB: bestFeatures = nb.loadDict()
    elif numFeatures != 0: bestFeatures = featureSelection(trainFeaturesAndLabels, labels, featureSelectionMechanism,numFeatures) 
    
    if bestFeatures:
        #Reduce features in train and test sets to only those in bestFeatures
        trainData = []
        for (features, label) in trainFeaturesAndLabels:
            newFeatures = Counter()
            for feature in features:
                if feature in bestFeatures: newFeatures[feature] = features[feature]
            trainData.append((newFeatures, label))
        trainFeaturesAndLabels = trainData
            
        testData = []
        for (features, label) in testFeaturesAndLabels:
            newFeatures = Counter()
            for feature in features:
                if feature in bestFeatures: newFeatures[feature] = features[feature]
            testData.append((newFeatures, label))
        testFeaturesAndLabels = testData
        
        thisTime = time.clock()
        print "Rearrange data: ", thisTime - lastTime, ' s'
        lastTime = thisTime
    
    #TRAINING AND CLASSIFICATION
    #Naive Bayes
    if useNB:
        classifier = nb.nbTrain(trainFeaturesAndLabels, labels, bestFeatures)
    
    #Gradient Descent    
    else:
        classifier = trainMultiClassClassifier(trainFeaturesAndLabels, labels, lossFunc, trainingIters, alpha, B)
    
    thisTime = time.clock()
    print "Train Classifier: ", thisTime - lastTime, ' s'
    lastTime = thisTime    
    
    #Test for errors
    trainError = classifier.getErrorRate(trainFeaturesAndLabels)
    testError = classifier.getErrorRate(testFeaturesAndLabels)
   
    thisTime = time.clock()
    print "Error checking: ", thisTime - lastTime, ' s'
    lastTime = thisTime
    
    print "Train Error: ", trainError     
    print "Test Error:", testError, "with", len(labels), "labels"        
    
if __name__ == "__main__":
    main()