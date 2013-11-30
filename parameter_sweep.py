import os,subprocess

featureExtractors = ['unigram','bigram','trigram','fourgram']
ITERS = 5

# Genre Classification

## Open up the parameter sweep file
#f_genre = open("parameter_sweep_genre.txt", "w")


## Run this based on the number of ITERS
#for iter in range(0,ITERS):
    #print "Classifiying Genres Iteration: %d" % iter
    ## Sweep over different feature extractors 
    #for feature in featureExtractors: 
	#print "Extracting %s features..." % feature
	## Sweep over different trainingIters
	#for i in range(1,6):
	    #print "Iterating %d times" % i
	    #subprocess.call(['python','main.py','0','1000','200',str(i),'100','0',"genre",feature],stdout = f_genre)

## Find the best featureExtractor & the best Training Iters & iterate over different alpha (learning rates)
#best_feature = 'trigram'
#best_iters = 5
#f_genre_best = open("best_parameter_sweep_genre.txt","w")
#for iter in range(0,ITERS):
    #for alpha in range(10, 100, 10):
	## Sweep over different alphas 
	#print "Sweeping over alphas..."
	#subprocess.call(['python','main.py','0','1000','200',best_iters,str(alpha),'0',"genre",best_feature],stdout = f_genre_best)
	
# Extra runs for best feature extractor
print "Extra runs for genre"
best_feature = 'trigram'
f_genre_extra = open("trigram_parameter_sweep_genre_extra.txt","w")
for iter in range(0,ITERS):
    print "Looping %d times" % iter 
    # Sweep over different trainingIters
    for i in range(6,12):
	print "Iterating %d times" % i
	subprocess.call(['python','main.py','0','1000','200',str(i),'100','0',"genre",best_feature],stdout = f_genre_extra)

# Artist Classification

## Open up the parameter sweep file
#f_artist = open("parameter_sweep_artist.txt", "w")

## Run this based on the number of ITERS
#for iter in range(0,ITERS):
    #print "Classifying Artists Iteration: %d" % iter
    ## Sweep over different feature extractors 
    #for feature in featureExtractors: 
	#print "Extracting %s features..." % feature
	## Sweep over different trainingIters
	#for i in range(1,6):
	    #print "Iterating %d times" % i 
	    ## Note: We are limiting to 12 labels (too many artists!)
	    #subprocess.call(['python','main.py','12','800','150',str(i),'100','0',"artist",feature],stdout = f_artist)
    
## Find the best featureExtractor & the best Training Iters & iterate over different alpha (learning rates)
#best_feature = 'trigram'
#best_iters = 5
#f_artist_best = open("best_parameter_sweep_artist.txt","w")
#for iter in range(0,ITERS):
    #for alpha in range(10, 100, 10):
	## Sweep over different alphas 
	#print "Sweeping over alphas..."
	#subprocess.call(['python','main.py','12','800','150',str(best_iters),str(alpha),'0',"artist",best_feature],stdout = f_artist_best)
	
# Extra runs for best feature extractor artist
print "Extra runs for artist"
best_feature = 'trigram'
f_artist_extra = open("trigram_parameter_sweep_artist_extra.txt","w")
for iter in range(0,ITERS):
    print "Looping %d times" % iter 
    # Sweep over different trainingIters
    for i in range(6,12):
	print "Iterating %d times" % i
	subprocess.call(['python','main.py','12','800','150',str(i),'100','0',"artist",best_feature],stdout = f_artist_extra)