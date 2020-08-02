# import important libraries 

import numpy as np     # for multidemisional arrays
import pandas as pd    # for handling excel file and making dataFrames
import math


def DataInDataFrame(queyMovieName):
    # read files
    pd_tags=pd.read_csv('ml-latest-small/tags.csv')   #pandas read tags file and store it as data frame  
    pd_movies=pd.read_csv('ml-latest-small/movies.csv')     #pandas read movies file and store it as data frame 
    
    pdRows,pdColumn=pd_movies.shape    #number of rows and number of columns
    moviesDict=dict()        # for storing movie genres in list against movie name
    genresSet=set()          # for storing unique genres 
    for i in range(pdRows):
        li=pd_movies.loc[i,"genres"]    # extracting movie genres from data frame
        li=list(li.split("|"))
        moviesDict[pd_movies.loc[i,"title"]]=li
        for x in li:
            genresSet.add(x)            # adding genres in set
    
    totalMovies=len(moviesDict)        # number of movies 
    genresList=list(genresSet)         #converting genersSet to list for using index           
    genresList.append("movie name")    # genersList will become column of data frame

    df_final = pd.DataFrame(index=range(totalMovies), columns=genresList)   #making an empty dataFrame with just genres
    df_final = df_final.fillna(0) # with 0s rather than NaNs
    #df_final.head()
    
    #appending movies name in DataFrame
    movieList=list(moviesDict.keys())
    for i in range(totalMovies):
        df_final.loc[i,"movie name"]=movieList[i]
        
    # if a movie has genres then making it bool true if not making it false
    for i in range(totalMovies):
        movieName=df_final.loc[i,"movie name"]
        genresLength=len(genresList)-1    #for only exploring genre columns and leaving movie name column
        for g in range(genresLength):
            movieGenre=genresList[g]
            if((movieGenre in moviesDict[movieName])):
                df_final.loc[i,movieGenre]=1
    
    # row number from movie name
    query_movie=list(df_final.iloc[df_final.loc[df_final['movie name']==queyMovieName].index[0]])  # will get row of query movie
    query_movie.pop()    #poping movie name from that row
    distanceList=list()
    for i in range(totalMovies):
        movie=list(df_final.iloc[df_final.loc[df_final['movie name']==df_final.loc[i,"movie name"]].index[0]])
        movie.pop()     #poping movie name from that row
        d=eucaldainDistance(query_movie,movie)
        distanceList.append((d,i,(df_final.loc[i,"movie name"])))
    return distanceList
# function for calculating eucaldian distance between two movies

def eucaldainDistance(x,y):
    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
    return distance  
    
def main():
    distanceList=DataInDataFrame("Spartan (2004)")
    # sort in ascending order and pick most 10 related movies
    distanceList = sorted(distanceList)[:10]   
    return distanceList

if __name__ == '__main__': 
    recomendedMovies=main()
    print(recomendedMovies)