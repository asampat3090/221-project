from collections import Counter
from numpy import *

def nbTrain(trainData, labels):
    """
    For K labels and n words in the vocabulary, trains K counters to have the log(p(x|y)).
    
    @param list of (counter, string) - the featureVector and label for each training sample
    @param list of strings - a list of the unique labels
    
    @return NBClassfier object
    """
    trainData = list(trainData)
    labels = list(labels)
    
    #Get a list of each word in our vocab
    words = Counter()
    for (features, label) in trainData:
        words.update(features)
    words = list(words)
    
    #get some numbers
    numLabels = len(labels)
    numExamples = len(trainData)    
    numWords = len(words)
    
    #Separate data:
    labeledData = []
    for i in labels:
        labeledData.append([(features, label) for (features, label) in trainData if label == i])
    
    #Calcuate logProbY:
    logProbY = array([len(i) for i in labeledData])
    logProbY = log(logProbY*1.0/numExamples)
    
    #Calculate logProbXGivenY:
    logProbXGivenY = zeros((numLabels, numWords))    
    for i, data in enumerate(labeledData):
        totWords = sum([sum(features.values() for (featuures,label) in data)]) + numWords 
        for j, word in enumerate(words):
            logProbXGivenY[i,j] = log((sum([features[word] for (features, label) in data])+1)*1.0/totWords)
    
    return NBClassifier(labels, logProbXGivenY, logProbY, words)

class NBClassifier(object):
    def __init__(self, labels, logProbXGivenY, logProbY, words):
        '''
        @param list of string - a unique list of labels
        @param 2D numpy array of size numLables x numWords, logProbXGivenY i,j entry = log(p(x = jth word | y = ith label)) 
        @param Numpy array of size numLabels, ith entry = log(p(y = ith label))
        @param List of strings - a list of all the words in the vocab
        '''
        self.labels = labels
        self.logProbXGivenY = logProbXGivenY
        self.logProbY = logProbY
        self.words = words
        
    def classify(self, featureVector):
        """
        Make a prediction of the label for the given featureVector
        
        @param Counter - a feature vector
               
        @return string - the predicted label
        """
        numLabels = len(self.labels)
        
        probYGivenX = [(0, label) for label in self.labels]
        for i in range(numLabels):
            for feature in featureVector:            
                probYGivenX[i][0] += featureVector[feature]*self.logProbXGivenY[i, words.index(feature)]
            probYGivenX[i][0] += self.logProbY[i]
                
        return max(probYGivenX, key= lambda x: x[0])[1]
    
    def getErrorRate(self, data):
        """
        Classify each feature vector given and compare result to label. Return the error rate (out of 1)
        @param a list of (feature vector, label) tuples

        @return float: error rate [0-1]
        """
        numLabels = len(self.labels)
        errors = [[0 for i in range(numLabels)] for i in range(numLabels)]
        numErrors = 0
        for (featureVector, label) in data:
            prediction = self.classify(featureVector)
            errors[labels.index(label)][labels.index(prediction)] += 1
            if prediction != label:
                numErrors += 1
                
        #print confusion matrix
        print "\t",
        for label in labels: 
            print label, "\t",
        print "Wanted"
        for i, label in enumerate(labels):
            print label, "\t",
            for j,x in enumerate(labels):
                print errors[i][j], "\t",
            print sum(errors[i])
        print "Got\t",
        for j, label in enumerate(labels):
            print sum([errors[i][j] for i in range(len(labels))]), "\t",
        print sum([sum(errors[i]) for i in range(len(labels))])
        print ""
                
        return 1.0*numErrors/len(data) 
    
    
    
    
    