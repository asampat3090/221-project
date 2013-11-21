import urllib2
from bs4 import BeautifulSoup
import time
import re

print "\n\nSTART"

file = open("lyrics/" + time.asctime() + ".txt", 'w')

request = urllib2.Request("http://www.metrolyrics.com/hey-jude-lyrics-beatles.html")
response = urllib2.urlopen(request)
soup = BeautifulSoup(response)

#Get artist
artist_string = soup.find(text=re.compile('artist'))       
start = artist_string.find('\"artist\":')
artist_string = artist_string[start+10:]
end = artist_string.find('\"')
artist_string = artist_string[:end]
file.write(artist_string)
file.write('\n')
        
#Get genre
genre_string = soup.find(text=re.compile('tag='))
start = genre_string.find('tag=');
genre_string = genre_string[start+4:]
end = genre_string.find(';')
genre_string = genre_string[:end]
file.write(genre_string)
file.write('\n')

#Get lyrics        
p_tags = soup.find_all('p')

for i, child in enumerate(p_tags):
    if len(child.attrs) > 0:
        if child.attrs['class'][0].find(u'verse') == 0:
            for string in child.stripped_strings:
                file.write(string)
                file.write('\n')

print "done"