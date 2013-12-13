"""
This file contains the following methods:

parseSongFile(file) - takes in a song file, returns a song object
printPlayList(assignment, songLibrary, request) - takes in an asignment from
     the CSP and prints the playlist, including the reasons why the songs were
     chosen given the request.

Class: Song
Contains the important song features: title, artist, genre, and keywords (unigrams from lyrics)

Class: Request
Init - parses a request file into an Request object.
isRequestValid - looks at a request and considers all the reasons why it
    may not be consistent - for example, wanting at least 10 songs but only wanting
    a max of 2 songs from one artist and nothing else. 
"""

import re, string, urllib
from collections import Counter

def parseSongFile(file):
    """
    Takes in a song file, returns a song object.
    """
    #song title
    nameList = file.name[:-4].split('-')
    nameList = nameList[:nameList.index('lyrics')]
    name = " ".join(word for word in nameList)

    #artist
    artist = file.readline().split('\n')[0]
    artist = urllib.unquote(artist).decode()
    artist = re.sub(' ', '', artist)
    
    #genre
    genre = file.readline().split('\n')[0]
    
    #keywords from lyrics
    lyrics = file.read()
    lyrics = ''.join(char for char in lyrics if char not in set(string.punctuation))
    lyrics = lyrics.lower()              
    keywords = set()
    keywords.update(word for word in lyrics.split())
    
    return Song(name, artist, genre, keywords)

def printPlayList(optimalAssignment, songLibrary, request):
    """
    Prints out the artist-title playlist given the indices of the chosen songs.
    @param dict: the dictionary of variables and values of the optimal assignement
    @param list of song objects: all the songs in the library
    @param Request object: the user preferences as a request object, used to make the CSP
    
    @return nothing, just prints
    """
    numSongsInLib = len(songLibrary)
    chosenSongs = [i for i in optimalAssignment if (i in range(numSongsInLib)) and (optimalAssignment[i] == 1)]
    
    printGenre = True if request.genres or request.notGenres or request.onlyGenres else False
    printKeywords = True if request.keywords else False
    
    requestedKeywords = set([keyword for (keyword, weight) in request.keywords])

    for i, song in enumerate(chosenSongs):
        print repr(i+1) + ". " + songLibrary[song].artist + " - " + songLibrary[song].title
        if printGenre: print "Genre:", songLibrary[song].genre
        if printKeywords: 
            print "Keywords:",
            for keyword in requestedKeywords.intersection(songLibrary[song].keywords):
                print keyword,
            print "\n"


        
#Just an object to hold a song's properties and print them nicely
class Song(object):
    def __init__(self, title, artist, genre, keywords):
        #string, song title
        self.title = title
        
        #string, artist title
        self.artist = artist
        
        #string, genre
        self.genre = genre
        
        #set of strings, lowercase no punctuation words in the lyrics
        self.keywords = set(keywords)
    
    def __str__(self):
        return self.artist + " - " + self.title + " - " + self.genre
        



#An object for parsing and holding the user's request 
class Request():
    def __init__(self, path):
        """
        @param filepath: the path to the file the user wrote of preferences
        
        Supports:
        minSongs #; maxSongs #
             - assumes they are ints. 
             - gefaults to 5 and 5 if not specified
             - if max is bigger than min or vice versa, updated to equal one another.
             eg:
                      minSongs 6
                      maxSongs 10
             
        genre:
            - only (genre): will only select songs in this genre. one genre per line, can do it multiple times.
            - not (genre): will not select any songs from this genre. one genre per line, can do it multiple times.
            - (genre) [min (#)] [max (#)] [weight]: can specify a min and/or max number of songs to take from
                    a particular genre, and put a weight (a positive int!) on how much you want that genre to be included.
            eg:
                      genre only hiphop
                      genre only rock min 0 max 5
                      genre only alternative max 10 20
                      genre not rap
                      genre electronic min 3   -->(this conflicts with the "only"lines, meant to be separate example)
        
        artist: (works the same as genre)
            - only (artist): will only select songs from this artist. one artist per line, can do it multiple times.
            - not (artist): will not select any songs from this artist. one artist per line, can do it multiple times.
            - (artist) [min (#)] [max (#)] [weight]: can specify a min and/or max number of songs to take from
                    a particular artist, and put a weight (a positive int!) on how much you want that artist to be included.
            eg:
                      artist only hiphop
                      artist only rock min 0 max 5
                      artist only alternative max 10 20
                      artist not rap
                      artist electronic min 3   -->(this conflicts with the "only"lines, meant to be separate example)
        
        keywords:
            - keywords (word)+: keywords can be followed by any number of words, all will be given weight 2
            - keyword (word) (weight): keyword can be followed by one 1 and it's weight (integer only). Make it greater than 1
               to have it take precendence over not mentioned keywords, and greater than 2 to take precendence over
               other mentioned by non-weighted keywords.
               No repeats, non-ints, or values less than 1.
            eg:
                     keywords a the love     --> (a, 2) (the, 2) (love, 2)
                     keyword heart 5           --> (heart, 5)
        """
        
        #Defaults
        self.minSongs = 5
        self.maxSongs = 5
        self.genres = [] #holds tuples of (genre, min, max, weight)
        self.onlyGenres = []
        self.notGenres = []
        self.artists = [] #holds tuples of (artist, min, max, weight)
        self.onlyArtists = []
        self.notArtists = []        
        self.keywords = []
        
        for line in open(path):
            m = re.match('minSongs (.+)', line)
            if m:
                self.minSongs = int(m.group(1))
                if self.maxSongs < self.minSongs: self.maxSongs = self.minSongs
                continue
            
            m = re.match('maxSongs (.+)', line)
            if m:
                self.maxSongs = int(m.group(1))
                if self.minSongs > self.maxSongs: self.minSongs = self.maxSongs
                continue

            m = re.match('genre ((only|not) )?(\S+)( min (\S+))?( max (\S+))?( weight (.+))?', line)
            if m:
                #Handle only and not case
                if m.group(1) == 'not ': 
                    self.notGenres.append(m.group(3))                
                    continue #ignore anything else after a "not" line
                
                if m.group(1) == 'only ': self.onlyGenres.append(m.group(3))
                
                #Handle max and min case
                minSongs = 0
                maxSongs = float('+inf')
                weight = 1
                if m.group(5): minSongs = int(m.group(5))
                if m.group(7): maxSongs = int(m.group(7))
                if m.group(9): weight = int(m.group(9))
                if minSongs or (maxSongs != float('+inf')) or (weight != 1):
                    self.genres.append((m.group(3), minSongs, maxSongs, weight))
                continue
            
            m = re.match('artist ((only|not) )?(\S+)( min (\S+))?( max (\S+))?( weight (.+))?', line)
            if m:
                #Handle only and not case
                if m.group(1) == 'not ': 
                    self.notArtists.append(m.group(3))                
                    continue #ignore anything else after a "not" line
                
                if m.group(1) == 'only ': self.onlyArtists.append(m.group(3))
                
                #Handle max and min case
                minSongs = 0
                maxSongs = float('+inf')
                weight = 1
                if m.group(5): minSongs = int(m.group(5))
                if m.group(7): maxSongs = int(m.group(7))
                if m.group(9): weight = int(m.group(9))
                if minSongs or (maxSongs != float('+inf')) or (weight != 1):
                    self.artists.append((m.group(3), minSongs, maxSongs, weight))
                continue            

            m = re.match('keywords (.+)', line)
            if m:
                self.keywords.extend([(word, 2) for word in m.group(1).split()])
                continue
            
            m = re.match('keyword (\S+)( \S+)?', line)
            if m:
                self.keywords.append((m.group(1), int(m.group(2))))
                continue
            
            #If got here, the line didn't match!
            if len(line.split()): print "Line not matched: ", line[:-1]
            
        
        print "Number of songs: ", self.minSongs, "-", self.maxSongs
        print "Genres:",
        print self.genres
        print "Only:",
        print self.onlyGenres
        print "Not:",
        print self.notGenres
        print "Artists:",
        print self.artists
        print "Only:",
        print self.onlyArtists
        print "Not:",
        print self.notArtists       
        print "Keywords:", self.keywords
    
    def isRequestValid(self, allGenres, allArtists):
        """
        Makes sure the request CAN be satisfied.
        @param list of strings - a list of all the genres in our library
        
        @return True or False - True if it is ok
        """        
        ##GENRE##
        #Make sure all genres are actual genres
        for (genre, minSongs, maxSongs, weight) in self.genres:
            if genre not in allGenres:
                print "Genre:", genre, "not in our list of genres"
                print "Available genres:", allGenres
                return False
        for genre in self.onlyGenres:
            if genre not in allGenres:
                print "Genre:", genre, "not in our list of genres"
                print "Available genres:", allGenres
                return False
        for genre in self.notGenres:
            if genre not in allGenres:
                print "Genre:", genre, "not in our list of genres"
                print "Available genres:", allGenres
                return False            
        
        #Make sure each list has no duplicates
        genreCounter = Counter([genre for (genre, minSongs, maxSongs, weight) in self.genres])
        if any(val > 1 for val in genreCounter.values()):
            print "Duplicate entry in self.genres"
            return False
        genreCounter = Counter(self.onlyGenres)
        if any(val > 1 for val in genreCounter.values()):
            print "Duplicate entry in self.onlyGenres"
            return False
        genreCounter = Counter(self.notGenres)
        if any(val > 1 for val in genreCounter.values()):
            print "Duplicate entry in self.notGenres"
            return False                   
            
        #Make sure all the mins and maxes are positive and weights are greater than 1
        for (genre, minSongs, maxSongs, weight) in self.genres:
            if minSongs < 0:
                print "Genre:", genre, "has a negative minSong"
                return False
            if maxSongs < 0:
                print "Genre:", genre, "has a negative maxSong"
                return False
            if minSongs > maxSongs:
                print "Genre:", genre, "has a larger minSong than maxSong"
                return False
            if weight < 1:
                print "Genre: ", genre, "has weight", weight, "which is less than 1"
                return False

        #Make sure no genre is in both notGenre and with nonzero min in genre:
        for (genre, minSongs, maxSongs, weight) in self.genres:
            if minSongs > 0 and genre in self.notGenres:
                print "Conflict with genre:", genre, "with nonzero min and in self.notGenre"
                return False  

        #Make sure the sum of maxs of songs in onlyGenres is bigger than self.minSongs:
        #But if onlyGenre has any genres that AREN"T in self.genres, skip (because those genres have no maxes)
        if self.onlyGenres and self.genres:
            if not any (genre not in [genre for (genre, minSongs, maxSongs, weight) in self.genres] for genre in self.onlyGenres):
                if sum([maxSongs for (genre, minSongs, maxSongs, weight) in self.genres if genre in self.onlyGenres]) < self.minSongs:
                    print "Sum of maxSongs for songs in onlyGenres is less than self.minSongs", self.minSongs
                    return False        
        
        #Make sure the sum of genre mins is less than the max songs requested:
        if sum([minSongs for (genre, minSongs, maxSongs, weight) in self.genres]) > self.maxSongs:
            print "Conflict with sum of genre minSongs being greater than self.maxSongs: ", self.maxSongs
            return False        

        ##ARTIST##
        #Make sure all artists are actual artists
        for (artist, minSongs, maxSongs, weight) in self.artists:
            if artist not in allArtists:
                print "Artist:", artist, "not in our list of artists"
                print "Available artists:", allArtists
                return False
        for artist in self.onlyArtists:
            if artist not in allArtists:
                print "Artist:", artist, "not in our list of artists"
                print "Available artists:", allArtists
                return False
        for artist in self.notArtists:
            if artist not in allArtists:
                print "Artist:", artist, "not in our list of artists"
                print "Available artists:", allArtists
                return False            
        
        #Make sure each artist list has no duplicates
        artistCounter = Counter([artist for (artist, minSongs, maxSongs, weight) in self.artists])
        if any(val > 1 for val in artistCounter.values()):
            print "Duplicate entry in self.artists"
            return False
        artistCounter = Counter(self.onlyArtists)
        if any(val > 1 for val in artistCounter.values()):
            print "Duplicate entry in self.onlyArtists"
            return False
        artistCounter = Counter(self.notArtists)
        if any(val > 1 for val in artistCounter.values()):
            print "Duplicate entry in self.notArtists"
            return False        

        #Make sure all the artist mins and maxes are positive and weights are greater than 1
        for (artist, minSongs, maxSongs, weight) in self.artists:
            if minSongs < 0:
                print "Artist:", artist, "has a negative minSong"
                return False
            if maxSongs < 0:
                print "Artist:", artist, "has a negative maxSong"
                return False
            if minSongs > maxSongs:
                print "Artist:", artist, "has a larger minSong than maxSong"
                return False
            if weight < 1:
                print "Artist: ", artist, "has weight", weight, "which is less than 1"
                return False        
        
        #Make sure no artist is in both nonArtist and with nonzero min in artists:
        for (artist, minSongs, maxSongs, weight) in self.artists:
            if minSongs > 0 and artist in self.notArtists:
                print "Conflict with artist:", artist, "with nonzero min and in self.notArtist"
                return False

        #Make sure the sum of maxs of songs in onlyArtists is bigger than self.minSongs:
        #But if onlyArtist has any artists that AREN"T in self.artists, skip (because those artists have no maxes)
        if self.onlyArtists and self.artists:
            if not any (artist not in [artist for (artist, minSongs, maxSongs, weight) in self.artists] for artist in self.onlyArtists):
                if sum([maxSongs for (artist, minSongs, maxSongs, weight) in self.artists if artist in self.onlyArtists]) < self.minSongs:
                    print "Sum of maxSongs for songs in onlyArtists is less than self.minSongs", self.minSongs
                    return False
        
        #Make sure the sum of artist mins is less than the max songs requested:
        if sum([minSongs for (artist, minSongs, maxSongs, weight) in self.artists]) > self.maxSongs:
            print "Conflict with sum of artist minSongs being greater than self.maxSongs: ", self.maxSongs
            return False

        ##KEYWORDS##
        #Make sure keywords has no repeats
        keywordCounter = Counter([keyword for (keyword, weight) in self.keywords])
        if any(val > 1 for val in keywordCounter.values()):
            print "Duplicate entry in self.keywords"
            return False        
        
        #Make sure none of the keywords have weights less than 2:
        if any(weight < 2 for (keyword, weight) in self.keywords):
            print "Keyword weights must all be an integer greater than 2"
            return False
                
        return True        
            