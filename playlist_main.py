import glob, os, random, string
import sys, time, re
from playlist_util import *

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
        
    #Parse prefs file and check for obvious problems
    request = Request(requestPath)
    if not request.checkRequest(): return
    
    thisTime = time.clock()
    print "Parse request: ", thisTime - lastTime, ' s'
    lastTime = thisTime     
    
    #Load the songs
    songLibrary = []

    os.chdir("lyrics/artist/")
    files = glob.glob("*.txt")
    
    for i in range(len(files)-1):
        nextSong = parseSongFile(open(files[i], 'r'))
        
        #check genre:
        if nextSong.genre in request.notGenres: continue
        if request.onlyGenres:
            if nextSong.genre not in request.onlyGenres: continue
        
        songLibrary.append(nextSong)
    
        if len(songLibrary) == numSongsInLib: break
    
    for song in songLibrary: print song

    #os.chdir("..")
    #os.chdir("genre/")
    #files = glob.glob("*.txt")
    
    #for i in range(len(files)-1):    
        #songs.append(parseSongFile(open(files[i], 'r')))
    
    thisTime = time.clock()
    print "Load examples: ", thisTime - lastTime, ' s'
    lastTime = thisTime        
    
    #Create a CSP and add the variables
    csp = CSP()
    
    for i in range(numSongsInLib):
        csp.add_variable(i, [0,1])
    
    #Make sure only numSongs get added
    sumVar = get_sum_variable(csp, 'totSongs', range(numSongsInLib), request.maxSongs)
    csp.add_unary_potential(sumVar, lambda x: request.minSongs <= x <= request.maxSongs)
    
    #Add genre constraints
    for (genre, minSongs, maxSongs) in request.genres:
        if maxSongs > request.maxSongs: maxSongs = request.maxSongs
        sumVar = get_sum_variable(csp, genre, [i for i in range(numSongsInLib) if songLibrary[i].genre == genre], maxSongs)
        csp.add_unary_potential(sumVar, lambda x: minSongs <= x <=maxSongs)
    
    thisTime = time.clock()
    print "Add variables: ", thisTime - lastTime, ' s'
    lastTime = thisTime    
    
    alg = BacktrackingSearch()
    alg.solve(csp, True, True, True)
    chosenSongs = [i for i in alg.optimalAssignment if (i in range(numSongsInLib)) and (alg.optimalAssignment[i] == 1)]
    printPlayList(chosenSongs, songLibrary)
    
    thisTime = time.clock()
    print "Run search: ", thisTime - lastTime, ' s'
    lastTime = thisTime    

if __name__ == "__main__":
    make_playlist()