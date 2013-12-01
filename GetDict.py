import glob, os, random
from collections import Counter
import string

os.chdir("lyrics/artist/")
files = glob.glob("*.txt")
totSongs = len(files)-1
vocab = Counter()

for i in range(len(files)-1):
       file = open(files[i], 'r')
       artist = file.readline().split('\n')[0]
       genre = file.readline().split('\n')[0]
       lyrics = file.read()
       
       if len(lyrics) < 10:
              print file.name
              continue
       
       #clean up the string
       lyrics = ''.join(char for char in lyrics if char not in set(string.punctuation))
       lyrics = lyrics.lower()       
       
       thisSong = set()
       thisSong.update(word for word in lyrics.split())
       vocab.update(thisSong)     

os.chdir("..")
os.chdir("genre/")
files = glob.glob("*.txt")
totSongs += len(files)-1
for i in range(len(files)-1):
       file = open(files[i], 'r')
       artist = file.readline().split('\n')[0]
       genre = file.readline().split('\n')[0]
       lyrics = file.read()
       
       if len(lyrics) < 10:
              print file.name
              continue
       
       #clean up the string
       lyrics = ''.join(char for char in lyrics if char not in set(string.punctuation))
       lyrics = lyrics.lower()       
       
       thisSong = set()
       thisSong.update(word for word in lyrics.split())
       vocab.update(thisSong)

#print list(vocab.most_common())
#print "Total number of words: ", len(vocab)
#print "Most common:", vocab.most_common(100)
#print "Least common:", vocab.most_common()[-100:]

#Grab words that show up in at least 2 songs, but not more than 1948 songs (half)
words = [word for word in vocab if 20 <= vocab[word]]
print words
print len(words)