#Feature Selection Parameter Sweeps - Perceptron
import os,subprocess
ITERS = 5
numLabels = 10

featureExtractors = ['unigram','bigram','trigram','fourgram']

#GENRE CLASSIFICATION W/ FEATURE SELECTION

# Open up the feature selection parameter sweep file
f_fs_genre = open("fs_parameter_sweep_genre.txt", "w")

# Run this based on the number of ITERS
for iter in range(0,ITERS):
    print "Classifiying Genres Iteration: %d" % iter
    # Sweep over different feature extractors 
    for feature in featureExtractors: 
	print "Extracting %s features..." % feature
	# Sweep over different numbers of features selected
	for numFeatures in range(100,2050,100):
	    print "Extracting %d of the most relevant features" % numFeatures
	    subprocess.call(['python','main.py','0','100','200','5','100','0',"genre",feature,str(numFeatures)],stdout = f_fs_genre)