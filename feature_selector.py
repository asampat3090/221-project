# import all files in order to classify 
import glob, os, random
import sys, time
import numpy as np
from Classifier import *
from features import *
from loadExamples import *

# Calculate information gain for a given feature 
def informationGain(trainData,feature,labels):
    """
    For K labels, calculates the information gain for the given feature
    
    @param list of training data
    @param list of features
    @param feature of interest
    @param list of strings - a list of the unique labels
    
    """
    
    # get all of the features
    allFeatures = Counter()
    featureArray = []
    featureArray = [features for (features, label) in trainData]
    for featureSet in featureArray :
        allFeatures.update(featureSet) 
    
    # get some numbers
    numLabels = len(labels)
    numExamples = len(trainData)
    numFeatures = sum([allFeatures[feature] for feature in allFeatures])
    
    # Separate data:
    labeledData = []
    for i in labels:
        labeledData.append([(features, label) for (features, label) in trainData if label == i])    
    
    # Calculate logProbY (logP(Y) = [logP(y1),logP(y2),....logP(yk)])
    logProbY = array([len(i) for i in labeledData])
    logProbY = log(logProbY*1.0/numExamples)
    
    # Calculate logProbFGivenY  
    logProbFGivenY = zeros((numLabels,numWords))
    for i, data in enumerate(labeledData):
        totFeatures = sum([sum(features.values() for (features,label) in data)]) + numFeatures 
        # Calculate this value only for the feature given
        logProbFGivenY[i] = log((sum([features[feature] for (features, label) in data])+1)*1.0/totFeatures)
    
    # Calculate logJointProbFY
    logJointProbFY = log(np.multiply(exp(np.array(logProbFGivenY)),exp(np.array(logProbY))))
    
    # Calculate logProbF (logP(f))
    # sum up all of the features
    logProbF = allFeatures[feature]
    logProbF = log(logProbF*1.0/numFeatures)
    
    # Calculate the log term of the mutual information
    logTerm = log(exp(logJointProbFY)/(exp(logProbF)*exp(logProbY)))
    
    # Calculate the mutual information term
    mutualInformation = sum(np.multiply(exp(logJointProbFY),logTerm))

return mutualInformation
      
    
# Use mutual information to select 

def featureSelection(trainExample,numFeatures):
    """
    
    """


