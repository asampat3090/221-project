# CODE TO CALCULATE TOTAL NUMBER OF FEATURES (FOR POSTER)
    # Calculate all of the features (not just those from the example)  
    allFeatures = Counter()
    trainArray = []
    trainArray = [fs for (fs, label) in trainFeaturesAndLabels]
    for trainSet in trainArray :
        allFeatures.update(trainSet)
    testArray = []
    testArray = [fs for (fs,label) in testFeaturesAndLabels]
    for testSet in testArray :
        allFeatures.update(testSet)
    
    print "THE TOTAL NUMBER OF FEATURES IS: %d" % len(allFeatures)
    
    #Feature Selection