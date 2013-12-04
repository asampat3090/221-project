#Naive Bayes Parameter Sweeps
import os,subprocess
ITERS = 5
numLabels = 10

featureExtractors = ['unigram','bigram','trigram','fourgram']

# Run Naive Bayes on various results

# GENRE

print("SWEEPING GENRE PARAMETERS....writing to nb_parameter_genre_artist.txt")

# Open up the parameter sweep file
f_nb_genre = open("nb_parameter_sweep_genre.txt", "w")

# Run this set of commands multiple times to get an average for genre.
for it in range(0,ITERS):
    print "Run this command multiple times to calculate averages: %d" % it
    for numTrainExamples in range(100,1050,100):
	print "Sweeping over number of training examples: %d" % numTrainExamples
	subprocess.call(['python','nb_main.py','0',str(numTrainExamples),'200','genre'],stdout = f_nb_genre)

# Read input from output file

# Create graphs from results 

# ARTIST

print("SWEEPING ARTIST PARAMETERS....writing to nb_parameter_sweep_artist.txt")

# Open up the parameter sweep file
f_nb_artist = open("nb_parameter_sweep_artist.txt", "w")

# Run this set of commands multiple times to get an average for genre.
for it in range(0,ITERS):
    print "Run this command multiple times to calculate averages: %d" % it
    for numTrainExamples in range(100,850,100):
	print "Sweeping over number of training examples: %d" % numTrainExamples
	subprocess.call(['python','nb_main.py','12',str(numTrainExamples),'150','artist'],stdout = f_nb_artist)
	
# Read input from output file
	
# Create graphs from results 