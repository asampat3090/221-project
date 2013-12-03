#Naive Bayes Parameter Sweeps
import os,subprocess
ITERS = 5
numLabels = 10

featureExtractors = ['unigram','bigram','trigram','fourgram']

# Run Naive Bayes on variuos results
# Open up the parameter sweep file
f_nb_genre = open("nb_parameter_sweep_genre.txt", "w")

# Run this set of commands multiple times to get an average.
for it in range(0,ITERS):
    print "Run this command multiple times to calculate averages: %d" % it
    # Sweep over different feature extractors 
    for feature in featureExtractors: 
	print "Extracting %s features..." % feature
	# Sweep over different numbers of labels 
	for numLabel in range(0,numLabels):
	    print "Sweeping over number of labels: %d" % numLabel
	    subprocess.call(['python','nb_main.py',str(numLabel),'1000','200',"genre"],stdout = f_nb_genre)

# Read input from output file


# Create graphs from results 