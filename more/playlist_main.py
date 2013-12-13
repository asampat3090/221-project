import glob, os, random, string
import sys, time, re
from playlist_util import *
from playlist_csp import *

"""
This is the main function. Parameters:
numSongsInLibrary - integer, usually 20. Reason: The CSP takes a long
                 time to solve with more than 20 nodes. Uses clever tricks
                 to make sure only relavent songs get put into the CSP in the
                 first place.
requestPath - usually just "request.txt", the file name of the request.
"""
def make_playlist():
    lastTime = time.clock()
    
    #Read arguments:
    if len(sys.argv) == 3:
        numSongsInLib = int(sys.argv[1])
        requestPath = sys.argv[2]
    else:
        print "Main function takes 2 arguments: numSongsInLibrary, requestPath"
        print "Using defaults instead: 10, 'request.txt'"
        numSongsInLib = 10
        requestPath = 'request.txt'
    
    #Read in all the songs we have a make lists of artists, genres, keywords:
    os.chdir("lyrics/genre/")
    files = glob.glob("*.txt")
    
    allSongs = []        
    for i in range(len(files)-1):    
        allSongs.append(parseSongFile(open(files[i], 'r')))
    random.shuffle(allSongs)
    
    thisTime = time.clock()
    print "Read in songs from genre: ", thisTime - lastTime, ' s'
    lastTime = thisTime     

    #Make lists of genres, artists, and keywords for checking requests for validity
    allGenres = sorted(set([song.genre for song in allSongs]))
    allArtists = sorted(set([song.artist for song in allSongs]))
    allKeywords = set()
    for song in allSongs:
        allKeywords.update(song.keywords)
    
    thisTime = time.clock()
    print "Assemble genre, artist, keyword sets: ", thisTime - lastTime, ' s'
    lastTime = thisTime     
        
    #Parse prefs file and check for obvious problems
    os.chdir("..")
    os.chdir("..")    
    request = Request(requestPath)
    if not request.isRequestValid(allGenres, allArtists): return
    
    thisTime = time.clock()
    print "Parse request: ", thisTime - lastTime, ' s'
    lastTime = thisTime     
    
    #Load the songs
    songLibrary = []
    secondChoiceSongLibrary = []

    for nextSong in allSongs:
        #check genre:
        if nextSong.genre in request.notGenres: continue
        if request.onlyGenres:
            if nextSong.genre not in request.onlyGenres: continue
        
        #check artist:
        if nextSong.artist in request.notArtists: continue
        if request.onlyArtists:
            if nextSong.artist not in request.onlyArtists: continue
        
        #check keywords:
        if request.keywords:
            if len(nextSong.keywords.intersection([keyword for (keyword, weight) in request.keywords])) < 1: 
                secondChoiceSongLibrary.append(nextSong)
                continue

        songLibrary.append(nextSong)
    
        if len(songLibrary) == numSongsInLib: break

    #If we didn't get enough songs, add second choice songs:
    if len(songLibrary) != numSongsInLib:
        print "Only got", len(songLibrary), "songs, using second choice songs"
        for song in secondChoiceSongLibrary:
            songLibrary.append(song)
            if len(songLibrary) == numSongsInLib: break
    
    #If we STILL didn't get enough songs, let user know and move on
    if len(songLibrary) != numSongsInLib:
        print "Couldn't find as many songs as requested"
        print "Have:", len(songLibrary), "Wanted:", numSongsInLib
      
    thisTime = time.clock()
    print "Assemble song library:", thisTime - lastTime, ' s'
    lastTime = thisTime        
    
    #Turn the request into a CSP
    csp = createPlaylistCSP(request, songLibrary)
    
    thisTime = time.clock()
    print "Add variables: ", thisTime - lastTime, ' s'
    lastTime = thisTime    
    
    alg = BacktrackingSearch()
    alg.solve(csp, True, True, True)
    printPlayList(alg.optimalAssignment, songLibrary, request)
    
    thisTime = time.clock()
    print "Run search: ", thisTime - lastTime, ' s'
    lastTime = thisTime    

if __name__ == "__main__":
    make_playlist()