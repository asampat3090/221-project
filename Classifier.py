import math
from collections import Counter
import random

def trainMultiClassClassifier(trainingData, labels, hypothesisFunc, trainingIters, alpha, B):
    '''
    @param list of (featureVector (as a counter), label): the (image features, label) data used to train the classifier
    @param list of strings: a list of the labels, one classifier will be made for each
    @param function(weights, featureVector): the hypothesis function, returns 1 or 0.
    @param int: trainingIters is the number of times to cycle through all the data.
    @param float: the learning rate, (0,1]
    @param int: the normalization constant. If 0, does nothing.
    
    @return a multiclass classier object that has been trained on the training data and is ready
    to classify new feature vectors.
    '''
    print "B = ", B
    #Make a list of weight vectors, one for each label
    #weights = [zeros((len(trainingData[0][0]))) for i in range(len(labels))]
    weights = [Counter() for i in range(len(labels))]
    
    #For each label, for each training data (x,y), calculate the loss function and update if
    #the loss function is positive.
    for i, posLabel in enumerate(labels):
        for j in range(trainingIters):
            for (featureVector, label) in trainingData:
                y = 1 if posLabel == label else 0
                incrementSparseVector(weights[i], alpha*(y - hypothesisFunc(weights[i], featureVector, y)), featureVector)
            #After each iteration, regulate and shuffle
            if B > 0:
                norm = math.sqrt(sparseVectorDotProduct(weights[i], weights[i]))
                if norm > B:
                    weights[i] = incrementSparseVector(Counter(), B/norm, weights[i])
                   
            random.shuffle(trainingData)
    
    print "Average norm = ", sum([math.sqrt(sparseVectorDotProduct(w,w)) for w in weights])/len(weights)
    return MultiClassClassifier(labels, weights)
    
class MultiClassClassifier(object):
    def __init__(self, labels, weights):
        '''
        @param list of strings: list of all the labels
        @param list of counters: the weight vectors associated with each label
        '''
        self.labels = labels
        self.weights = weights
        
    def classify(self, featureVector):
        '''
        Takes the dot product between each weight in self.weights and the feature vector and returns
        the label associated with the maximum score.
        
        @param numpy array: the feature vector to classify
        
        @return string: the label it is classified with
        '''
        return max([(self.labels[i], sparseVectorDotProduct(self.weights[i],featureVector)) for i in range(len(self.labels))], key = lambda x: x[1])[0]
    
    def getErrorRate(self, labels, data):
        """
        Classify each feature vector given and compare result to label. Return the error rate (out of 1)
        @param a list of (feature vector, label) tuples
        @param a list of unique labels

        @return float: error rate [0-1]
        """
        errors = [[0 for i in range(len(labels))] for i in range(len(labels))]
        numErrors = 0
        for (featureVector, label) in data:
            prediction = self.classify(featureVector)
            errors[labels.index(label)][labels.index(prediction)] += 1
            if prediction != label:
                numErrors += 1
                
        #print confusion matrix
        print "\t",
        for label in labels: 
            if label == "electronic": print "elec\t",
            else: print label, "\t",
        print ""
        for i, label in enumerate(labels):
            if label == "electronic": print "elec\t",
            else: print label, "\t",
            for j,x in enumerate(labels):
                print errors[i][j], "\t",
            print ""
            
                
        return 1.0*numErrors/len(data)    
    
def perceptronH(weightVector, featureVector, y):
    '''
    Perceptron hypothesis function: returns 1(weight dot feature >= 0)
    
    @param numpy array: weight vector
    @param numpy array: feature vector
    @param int: y, +1 if this feature vector should be positive, 0 otherwise
    
    @return int: the hypothesis, 1 or 0
    '''    
    return 1.0 if dot(weightVector, featureVector) >= 0 else 0

def hingeH(weightVector, featureVector, y):
    '''
    Hinge hypothesis function: if y = 1, returns 1(weight dot x > 1)
                               if y = 0, returns 1 - 1(weight dot x < -1)
    
    @param numpy array: weight vector
    @param numpy array: feature vector
    @param int: y, +1 if this feature vector should be positive, 0 otherwise
    
    @return int: the hypothesis, 1 or 0
    '''    
    if y:
        return 1.0 if dot(weightVector,featureVector) >= 1 else 0
    else:
        return 0 if dot(weightVector, featureVector) <= -1 else 1.0

def logisticH(weightVector, featureVector, y):
    '''
    Logistic hypothesis function: 1/(1+exp(- weight dot x))
    
    @param numpy array: weight vector
    @param numpy array: feature vector
    @param int: y, +1 if this feature vector should be positive, 0 otherwise
    
    @return int: the hypothesis, 1 or 0
    '''  
    #Was getting a math overflow error, so changing it to this:  
    d = sparseVectorDotProduct(weightVector,featureVector)
    
    if d > 500:
        return 1.0
    elif d < 500:
        return 0.0
    else:
        return 1.0/(1.0 + math.exp(-1.0*d))
    
def sparseVectorDotProduct(v1, v2):
    if (len(v1) > len(v2)):
        v1, v2 = v2, v1
    return sum(v1[x]*v2[x] for x in v1.keys())

def incrementSparseVector(v1, scale, v2):
    """
    Given two sparse vectors |v1| and |v2|, perform v1 += scale * v2.
    """
    scaled = Counter()
    for key in v2.keys():
        v1[key] += v2[key]*scale
    return v1