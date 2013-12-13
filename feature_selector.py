# import all files in order to classify 
import glob, os, random
import sys, time
from numpy import *
from Classifier import *
from features import *
from loadExamples import *
from collections import Counter
from array import array
import numpy as np
import mdp

# Calculate information gain for a given feature 
def informationGain(trainData,allFeatures,feature,labels):
    """
    For K labels, calculates the information gain for the given feature
    
    @param list of training data
    @param feature of interest
    @param list of strings - a list of the unique labels
    
    """ 
    # get some numbers
    numLabels = len(labels)
    numExamples = len(trainData)
    numFeatures = sum([allFeatures[f] for f in allFeatures])
    
    # Separate data:
    labeledData = []
    for i in labels:
        labeledData.append([(features, label) for (features, label) in trainData if label == i])    
    
    # Calculate logProbY (logP(Y) = [logP(y1),logP(y2),....logP(yk)])
    logProbY = [float(len(i)) for i in labeledData]
    # Ensure no divide by zero error
    logProbY = log(multiply(logProbY,1.0)/numExamples)
    
    # Calculate logProbFGivenY  
    logProbFGivenY = zeros((numLabels,1))
    for i, data in enumerate(labeledData):
        # Calculate this value only for the feature given
        totFeatures = sum([features[feature] for (features,label) in data]) + numFeatures
        logProbFGivenY[i] = log((sum([features[feature] for (features, label) in data])+1)*1.0/totFeatures)
        #print logProbFGivenY[i]
    # Calculate logJointProbFY
    logProbY = transpose(tile(logProbY, (logProbFGivenY.shape[1],1)))
    if logProbY.all() == 0:
        logJointProbFY = log(multiply(exp(logProbFGivenY),exp(logProbY)))
    else: 
        logJointProbFY = zeros(len(logProbY))
    # Calculate logProbF (logP(f))
    # sum up all of the features
    logProbF = allFeatures[feature]
    # Ensure no divide by zero error
    if numFeatures != 0:
        logProbF = log(logProbF*1.0/numFeatures)
    else: 
        logProbF = 0
    
    # Calculate the log term of the mutual information
    # Ensure no divide by zero errors
    logTerm = log(exp(logJointProbFY)/(exp(logProbF)*exp(logProbY)))
    
    # Calculate the mutual information term
    mutualInformation = sum(multiply(exp(logJointProbFY),logTerm))

    return mutualInformation
        
        
# Return featureLibrary with the number of features we want to consider.
def featureSelection(trainData,labels,featureSelectionMechanism,numFeatures):
    """
    Given the feature set of example, will give a reduced feature set.
    
    @param list of training data
    @param list of strings - a list of the unique labels
    @param number of features we want to choose
    """
    informationGains = []
    featureNames = []
    featureLibraryInfo = []
    featureLibrary = []
    
    # Calculate all of the features (not just those from the example)  
    print("Calculate all of the given features")
    allFeatures = Counter()
    featureArray = []
    featureArray = [fs for (fs, label) in trainData]
    for featureSet in featureArray :
        allFeatures.update(featureSet)
    if(numFeatures<len(allFeatures)):
        if(featureSelectionMechanism=="information_gain"):
            # Loop through all of the features and calculate the information gain for each 
            for feature in allFeatures: 
                informationGains.append(informationGain(trainData,allFeatures,feature, labels))
                featureNames.append(feature) 
            informationGains = np.array(informationGains)
            sortedargs = np.argsort(informationGains)
            featureNames = [featureNames[i] for i in sortedargs]
            print informationGains
            #informationGains.reverse()
            #featureNames.reverse()
            # Add the top numFeatures to the counter.   
            # if requesting too many features change number of requested features.
            if(numFeatures>len(featureNames)):
                numFeatures = len(featureNames)
            for i in range(0,numFeatures):
                selected_features_info.append(informationGains[i])
                selected_features.append(featureNames[i])
            # print featureLibraryInfo        
        else: 
            # Create a matrix with he relevant labels
            allFeaturePairList = list(allFeatures.items());
            allFeatureKeyList = [pair[0] for pair in allFeaturePairList];
            index = 0;
            data_features_matrix = np.zeros((len(trainData),len(allFeatures)));
            print("Creating the matrix for PCA input")
            for (features,label) in trainData: 
                # Loop through each feature and populate matrix
                for feature in features:
                    data_features_matrix[index][allFeatureKeyList.index(feature)] = allFeatures[feature]
                index=index+1
        
            # Run PCA to reduce feature size.
            # print(data_features_matrix)
            
            print("Using PCA to reduce the number of features")
            reduced_features = mdp.pca(transpose(data_features_matrix),output_dim = 2, svd = True)
            u1 = reduced_features[:,1]
            order = np.argsort(u1)[::-1]
            order = order[1:numFeatures]
            print("Populate the selected_features based on representation in first principal component")
            selected_features = [allFeatureKeyList[index] for index in order]
            print(selected_features)
    else:
        for feature in allFeatures:
            featureNames.append(feature)
        selected_features = featureNames    
       
    # Return the selected features regardless of algorithm used.
    return selected_features   