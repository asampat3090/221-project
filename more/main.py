import glob, os, random, nb
import sys, time
from Classifier import *
from features import *
from loadExamples import *
from feature_selector import *

"""
ARGUMENTS:
numLabels:           0 means no preference. 1 - n means "only draw examples from numLabels most popular"
numTrainSongs:       how many songs to use for training
numTestSongs:        how many songs to use for testing
trainingIters:       number of iterations through all the training songs during SGD
alpha:               n int from 0 - 100 that will be devided by 100 to obtain the learning rate.
B:                   the regularization parameter, if set to something higher than 0, norm(w) will never exeed B
'artist' or 'genre'                        choose classification metric.
'unigram','bigram','trigram' or 'fourgram' which feature extractor to use.
'information_gain', 'pca','num_songs'      which feature selection mechanism to use.
(if 'num_songs' selection) 
    minNumSongs                            The minimum number of songs a feature must show up in to be used
    maxNumSongs                            The maximum number of songs a feature must show up in to be used
(if 'information_gain' or 'pca' selection) 
    numFeatures:                           how many features do we want to use? - if 0 then just take all.
'nb' or 'gd':                              Naive Bayes or Gradient Descents
(if 'gd' algorithm chosen)
    'log', 'hinge', 'perceptron'           which loss function to use with gradient descent.

"""

def main():
    lastTime = time.clock()
    
    #If arguments were given, read them in:
    if len(sys.argv) > 11:
        numLabels = int(sys.argv[1])
        numTrainSongs = int(sys.argv[2])
        numTestSongs = int(sys.argv[3])
        trainingIters = int(sys.argv[4])
        alpha = 1.0*int(sys.argv[5])/100
        B = int(sys.argv[6])
        isArtist = True if sys.argv[7] == 'artist' else False
        featureExtractor = sys.argv[8]
        featureSelectionMechanism = sys.argv[9]
        if(featureSelectionMechanism=='num_songs'):
            minNumSongs = int(sys.argv[10])
            maxNumSongs = int(sys.argv[11])
            useNB = True if sys.argv[12] == 'nb' else False
            if(useNB==False):
                if sys.argv[13] == 'perceptron': lossFunc = perceptronH
                elif sys.argv[13] == 'hinge': lossFunc = hingeH
                else: lossFunc = logisticH 
            else: 
                lossFunc="logistic"
            numFeatures = 0
        else: 
            numFeatures = int(sys.argv[10])
            useNB = True if sys.argv[11] == 'nb' else False
            if(useNB==False):
                if sys.argv[12] == 'perceptron': lossFunc = perceptronH
                elif sys.argv[12] == 'hinge': lossFunc = hingeH
                else: lossFunc = logisticH
            else: 
                lossFunc="logistic"
            minNumSongs = 0
            maxNumSongs = 0
    else:
        print "Main function takes 12, 13 or 14 arguments: There are 4 cases"
        print "numLabels, numTrainSongs, numTestSongs, trainingIters,\
        alpha, B, artist/genre uni/bi/tri/fourgram, featureSelectionMechanism, minNumSongs, maxNumSongs,(nb or gd)"        
        print "numLabels, numTrainSongs, numTestSongs, trainingIters,\
        alpha, B, artist/genre uni/bi/tri/fourgram, featureSelectionMechanism, minNumSongs, maxNumSongs,(nb or gd), (perceptron hinge or log)"
        print "numLabels, numTrainSongs, numTestSongs, trainingIters,\
        alpha, B, artist/genre uni/bi/tri/fourgram, featureSelectionMechanism, numFeatures, (nb or gd)"
        print "numLabels, numTrainSongs, numTestSongs, trainingIters,\
        alpha, B, artist/genre uni/bi/tri/fourgram, featureSelectionMechanism, numFeatures, (nb or gd),(perceptron hinge or log)"        
        print "Using defaults instead: 0 20 20 10 90 0 'genre' 'bigram' 'pca' 0 gd logistic"
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
        minNumSongs = 0
        maxNumSongs = 10000
    
    #Repeat inputs:
    print "Number of labels, train, and test songs:", numLabels, numTrainSongs, numTestSongs
    
    if isArtist: print "Classify artist"
    else: print "Classify genre"
    
    print "Feature extractor", featureExtractor
    print "Feature selector", featureSelectionMechanism
    
    if not useNB:
        print "Gradient Descent"
        print "Training iters, alpha, and B:", trainingIters, alpha, B
        if lossFunc == perceptronH: print "Perceptron loss"
        elif lossFunc == hingeH: print "Hinge loss"
        else: print "Logistic loss"
        if numFeatures: print "Use", numFeatures, "features"
    else:
        print "Naive Bayes"
    
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
    
    #FEATURE SELECTION 
    bestFeatures = featureSelection(trainFeaturesAndLabels, labels, featureSelectionMechanism,numFeatures,minNumSongs,maxNumSongs,trainSongs,featureExtractor)

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