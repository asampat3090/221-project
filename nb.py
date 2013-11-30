from collections import Counter
from numpy import *

def nbTrain(trainData, labels):
    """
    For K labels and n words in the vocabulary, trains K counters to have the log(p(x|y)).
    
    @param list of (counter, string) - the featureVector and label for each training sample
    @param list of strings - a list of the unique labels
    
    @return (logProbXGivenY, logP(Y)) 
    2D numpy array of size numLabels by numWords. The i,j entry corresponds to the log 
       of the conditional probability of the jth word in the vocabulary appearing given y = the ith label.
    Numpy array of size numLabels where the ith entry is the log(p(y = ith label))
    """
    trainData = list(trainData)
    labels = list(labels)
    
    #Get a list of each word in our vocab
    words = Counter()
    for (features, label) in trainData:
        words.update(features)
    
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
    
    return (logProbXGivenY, logProbY)



def nbClassify(featureVector, logProbXGivenY, logProbY):
    """
    Make a prediction of the label for the given featureVector
    
    @param Counter - a feature vector
    @param 2D numpy array of size numLables x numWords, logProbXGivenY i,j entry = log(p(x = jth word | y = ith label)) 
    @param Numpy array of size numLabels, ith entry = log(p(y = ith label))
    
    @return string - the predicted label
    """
    
    
    
    