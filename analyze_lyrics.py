import glob, os, random
from collections import Counter

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

class Classifier(object):
    def __init__(self, labels):
        """
        @param (string, string): Pair of positive, negative labels
        @return string y: either the positive or negative label
        """
        self.labels = labels

    def classify(self, text):
        """
        @param string text: e.g. email
        @return double y: classification score; >= 0 if positive label
        """
        raise NotImplementedError("TODO: implement classify")

    def classifyWithLabel(self, text):
        """
        @param string text: the text message
        @return string y: either 'ham' or 'spam'
        """
        if self.classify(text) >= 0.:
            return self.labels[0]
        else:
            return self.labels[1]

class WeightedClassifier(Classifier):
    def __init__(self, labels, featureFunction, params):
        """
        @param (string, string): Pair of positive, negative labels
        @param func featureFunction: function to featurize text, e.g. extractUnigramFeatures
        @param dict params: the parameter weights used to predict
        """
        super(WeightedClassifier, self).__init__(labels)
        self.featureFunction = featureFunction
        self.params = params

    def classify(self, x):
        """
        @param string x: the text message
        @return double y: classification score; >= 0 if positive label
        """
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        return sparseVectorDotProduct(self.featureFunction(x),self.params)
        # END_YOUR_CODE
        
def learnWeightsFromPerceptron(trainExamples, featureExtractor, labels, iters = 20):
    """
    @param list trainExamples: list of (x,y) pairs, where
      - x is a string representing the text message, and
      - y is a string representing the label ('ham' or 'spam')
    @params func featureExtractor: Function to extract features, e.g. extractUnigramFeatures
    @params labels: tuple of labels ('positive', 'negative'), e.g. ('spam', 'ham').
    @params iters: Number of training iterations to run.
    @return dict: parameters represented by a mapping from feature (string) to value.
    """
    # BEGIN_YOUR_CODE (around 15 lines of code expected)
    w = Counter()
    for i in range(0,iters):
        for (x,y) in trainExamples:
            wC = WeightedClassifier(labels,featureExtractor, w)
            score = wC.classify(x)
            yPred = labels[0] if (score >= 0) else labels[1]
            if yPred != y:
                if (score < 0): incrementSparseVector(w, 1, featureExtractor(x))
                else:
                    incrementSparseVector(w, -1, featureExtractor(x))    
    return w
    # END_YOUR_CODE

def extractBigramFeatures(x):
    """
    Extract unigram + bigram features for a text document $x$. 

    @param string x: represents the contents of an email message.
    @return dict: feature vector representation of x.
    """
    # BEGIN_YOUR_CODE (around 12 lines of code expected)

    punctuationSet = set('!@#$%^&*()_+-={}[]|\:;/?.,><~`')
    endOfSentanceSet = set('.?!')
    bigrams = Counter()
    
    #Split on sentences
    sentenceList = x.split('.')
    for sentence in sentenceList:
        wordList = sentence.split()
        if (len(wordList) > 0):
            bigrams.update([x for x in wordList if x not in punctuationSet]) #add unigrams
            firstWord = "-BEGIN- " + wordList[0]; #add first word
            bigrams.update([firstWord])
            for i, word in enumerate(wordList[:-1]): #add bigrams
                    if word not in punctuationSet: 
                        if wordList[i+1] not in punctuationSet:
                            newWord = word + " " + wordList[i+1]
                            bigrams.update([newWord]) #add all non-punctuation bigrams
    return bigrams

class MultiClassClassifier(object):
    def __init__(self, labels, classifiers):
        """
        @param list string: List of labels
        @param list (string, Classifier): tuple of (label, classifier); each classifier is a WeightedClassifier that detects label vs NOT-label
        """
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        self.labels = labels
        self.classifiers = classifiers
        # END_YOUR_CODE

    def classify(self, x):
        """
        @param string x: the text message
        @return list (string, double): list of labels with scores 
        """
        raise NotImplementedError("TODO: implement classify")

    def classifyWithLabel(self, x):
        """
        @param string x: the text message
        @return string y: one of the output labels
        """
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        (label, score) = max(self.classify(x), key = lambda x: x[1])
        return label
        # END_YOUR_CODE

class OneVsAllClassifier(MultiClassClassifier):
    def __init__(self, labels, classifiers):
        """
        @param list string: List of labels
        @param list (string, Classifier): tuple of (label, classifier); the classifier is the one-vs-all classifier
        """
        super(OneVsAllClassifier, self).__init__(labels, classifiers)

    def classify(self, x):
        """
        @param string x: the text message
        @return list (string, double): list of labels with scores 
        """
        # BEGIN_YOUR_CODE (around 4 lines of code expected)
        return [(label, classifier.classify(x)) for (label, classifier) in self.classifiers]
        # END_YOUR_CODE

def learnOneVsAllClassifiers( trainExamples, featureFunction, labels, perClassifierIters = 10 ):
    """
    Split the set of examples into one label vs all and train classifiers
    @param list trainExamples: list of (x,y) pairs, where
      - x is a string representing the text message, and
      - y is a string representing the label (an entry from the list of labels)
    @param func featureFunction: function to featurize text, e.g. extractUnigramFeatures
    @param list string labels: List of labels
    @param int perClassifierIters: number of iterations to train each classifier
    @return list (label, Classifier)
    """
    labelClassifierList = []
    for label in labels:
        #get weights
        weights = learnWeightsFromPerceptron([(x, 'NOT'+y if label != y else y) for (x,y) in trainExamples], featureFunction, (label, 'NOT'+label),perClassifierIters)
        #make a weighted classifier
        labelClassifierList.append((label, WeightedClassifier((label, 'NOT'+label), featureFunction, weights)))
    return labelClassifierList

def getExamples(percentForTraining, files):
    '''
    @param number from 0 to 1 saying how many of the files should be training examples
    @param a list of files with the data inside
    @return (trainExamples, devExamples, artistLabels, genreLabels) where *examples are lists of (lyrics, artist, genre)
            and *Labels are lists of unique labels
    '''
    
    trainExamples = []
    devExamples = []
    artistLabels = []
    genreLabels = []
    
    for fileName in files:
        file = open(fileName, 'r')
        artist = file.readline().split('\n')[0]
        genre = file.readline().split('\n')[0]
        lyrics = file.read()
        
        if(random.random() < percentForTraining):
            trainExamples.append((lyrics, artist, genre))
        else:
            devExamples.append((lyrics, artist, genre))
            
        if genreLabels.count(genre) is 0: genreLabels.append(genre)
        if artistLabels.count(artist) is 0: artistLabels.append(artist)  
        
    artistLabels.sort()
    genreLabels.sort()
    return (trainExamples, devExamples, artistLabels, genreLabels)

def getErrorRate(examples, artistClassifier, genreClassifier):
    """
    @param a list of (lyrics, artist, genre) tuples
    @param an artist classifier
    @param a genra classifier
    @return (genreErrorRate, artistErroRate) - runs the classiers on the examples
    and reports back error rates 
    """
    genreErrors = artistErrors = 0
    for (lyrics, artist, genre) in examples:
        if genreClassifier.classifyWithLabel(lyrics) != genre:
            print "Got " + repr(genreClassifier.classifyWithLabel(lyrics)) + ", Wanted: " + repr(genre)
            genreErrors+=1
        if artistClassifier.classifyWithLabel(lyrics) != artist:
            print "Got " + repr(artistClassifier.classifyWithLabel(lyrics)) + ", Wanted: " + repr(artist)
            artistErrors+=1
    return (1.0*genreErrors/len(examples), 1.0*artistErrors/len(examples))    

def main():
    os.chdir("lyrics/")
    (trainExamples, devExamples, artistLabels, genreLabels) = getExamples(0.5, glob.glob("*.txt"))
    print "Train = " + repr(len(trainExamples)) + ", Dev = " + repr(len(devExamples))
    
    print artistLabels
    print genreLabels
    
    #Split up the data into appropriate lists
    genreTrainExamples = [(lyrics, genre) for (lyrics, artist, genre) in trainExamples]
    artistTrainExamples = [(lyrics, artist) for (lyrics, artist, genre) in trainExamples]
    
    #Make a genre and an artist One vs All classifier
    genreClassifiers = learnOneVsAllClassifiers(genreTrainExamples, extractBigramFeatures, genreLabels)
    genreClassifier = OneVsAllClassifier(genreLabels, genreClassifiers)
    
    artistClassifiers = learnOneVsAllClassifiers(artistTrainExamples, extractBigramFeatures, artistLabels)
    artistClassifier = OneVsAllClassifier(artistLabels, artistClassifiers)
    
    #Evaluate the classifier
    genreError, artistError = getErrorRate(trainExamples, artistClassifier, genreClassifier)
    print "TRAINING EXAMPLES:"
    print "Genre Error Rate = " + repr(genreError)
    print "Artist Error Rate = " + repr(artistError)
    
    genreError, artistError = getErrorRate(devExamples, artistClassifier, genreClassifier)
    print "DEV EXAMPLES:"
    print "Genre Error Rate = " + repr(genreError)
    print "Artist Error Rate = " + repr(artistError)    

if __name__ == "__main__":
    main()