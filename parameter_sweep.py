import os,subprocess

featureExtractors = ['bigram','trigram','fourgram']
# Sweep over different feature extractors 
for feature in featureExtractors: 
    # Sweep over different trainingIters
    for i in range(1,5):
        subprocess.call(['python','main.py','0','1000','200',str(i),'100','0',feature])
    
