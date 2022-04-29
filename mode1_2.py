import requests
import keys
import json
import sqlite3


def search_related_movies(movieName, key = keys.key_tastedive):
    """
    search related movies using TasteDive API
    
    Parameters
    ----------
    movieName: str
        A string input
    
    Returns
    -------
    A list contain related movie name.
    """
    baseurl="https://tastedive.com/api/similar"
    params_dict = {}
    params_dict["q"]= movieName  # movie
    params_dict["type"]= "movies"
    params_dict["limit"] = "20"
    params_dict["k"]= key
    resp = requests.get(baseurl, params = params_dict)
    print(resp.url)
    resp_json = resp.json()
    result=[]
    try:
        results = resp_json['Similar']['Results']
    except:
        results =[]
    for a_result in results:
        result.append(a_result['Name'])
    return result
    


def get_related_titles(list_input):
    """
    Retirieve realted movie name from a list of input
    
    Parameters
    ----------
    list_input: list
        A movie name..
    
    Returns
    -------
    A list contain related movie name.
    """
    if list_input != []:
        auxList=[]
        relatedList=[]
        for movieName in list_input:
            auxList = search_related_movies(movieName)
            for movieNameAux in auxList:
                if movieNameAux not in relatedList:
                    relatedList.append(movieNameAux)
        
        return relatedList
    return list_input

def get_movie_data(movieName, key = keys.OMDb_API_key):
    """
    Retirieve json data about a movie using OMDb API.
    
    Parameters
    ----------
    movieName: string.
        A movie name.
    
    Returns
    -------
    Json data about that movie.
    """
    baseurl= "http://www.omdbapi.com/"
    params_dict = {}
    params_dict["t"]= movieName
    params_dict["apikey"]= key
    params_dict["r"]= "json"
    resp = requests.get(baseurl, params = params_dict)
    print(resp.url)
    respDic = resp.json()
    return respDic

def get_movie_rating(movieJson):
    """
    Get movie IMDb score from json data about the movie.
    
    Parameters
    ----------
    movieJson: Json
        Json data about the movie
    
    Returns
    -------
    IMDb score(float) about the movie.
    """
    str_rating = ""
    try:
        str_rating = movieJson["imdbRating"]
    except:
        str_rating = ""
 
    if str_rating != "":
        try:
            float_rating = float(str_rating)
        except:
            float_rating = 0
    else:
        float_rating = 0
    return float_rating

def get_sorted_recommendations(listMovieTitle):
    """
    Print sorted_recommendations based on IMDb score of movie.
    
    Parameters
    ----------
    listMovieTitle: list
        A list of movie titles.
    
    Returns
    -------
    """
    score={}
    conn = sqlite3.connect('info.sqlite')
    cur = conn.cursor()
    for a_movie in listMovieTitle:
        cur.execute('''SELECT Id,ImdbRating From Movies WHERE Title = ?  ''', (a_movie, ))
        row = cur.fetchall()
        if row != None:
            try:
                score[a_movie] = float(row[0][1])
            except:
                score[a_movie] = 0
        else:
            load_data([a_movie])
            cur.execute('''SELECT Id,ImdbRating From Movies WHERE Title = ?  ''', (a_movie, ))
            row = cur.fetchall()
            if row != None:
                try:
                    score[a_movie] = float(row[0][1])
                except:
                    score[a_movie] = 0
            else:
                print("Rate limit reach.Please try another list of movie or use this function later")
                cur.close()
                return
    cur.close()
    print(dict(sorted(score.items(), key = lambda x: x[1], reverse = True)))



def load_data(ls_input):
    """
    Take a list of input. Get related movie names about each input.  
    Load movie data into info.sqlite. Updata Movies, Actors and Movies_actors table.
    
    Parameters
    ----------
    listMovieTitle: list
        A list of input.
    
    Returns
    -------
    """
    if ls_input != []:
        #start = None
        conn = sqlite3.connect('info.sqlite')
        cur = conn.cursor()
        for a_input in ls_input:
            a_ls = get_related_titles(a_input)
            for a_movie_name in a_ls:
                title, year, genre, plot, imdbRating = None, None, None, None, None
                title = a_movie_name
                data_json = get_movie_data(a_movie_name)

                try:
                    year = data_json["Year"]
                except:
                    year = None
                
                try:
                    genre = data_json["Genre"]
                except:
                    genre = None

                try:
                    plot = data_json["Plot"]
                except:
                    plot = None

                try:
                    imdbRating = get_movie_rating(data_json)
                except:
                    imdbRating = None

                cur.execute('''INSERT OR IGNORE INTO Movies (title, year, genre, plot, imdbRating)
                    VALUES ( ?, ?, ?, ?, ?)''', (title, year, genre, plot, imdbRating))
                conn.commit()
                cur.execute('''SELECT ID From Movies WHERE Title = ? AND Year = ? 
                AND Genre = ? AND Plot = ?  ''', (title, year, genre, plot))
                row = cur.fetchall()
                try:
                    movie_id = row[0][0]
                except:
                    movie_id = None
                print("movieid", movie_id)
                if movie_id == None:
                    continue 
                try:
                    actor = data_json["Actors"]
                except:
                    actor = None
                print("actor_rawdata:", actor)
                if actor != None:
                    actor = actor.split(",")
                    for an_actor in actor:
                        an_actor = an_actor.strip()
                        cur.execute('''INSERT OR IGNORE INTO Actors (Name)
                        VALUES (?)''', (an_actor,) )
                        conn.commit()
                        cur.execute('''SELECT ID From Actors WHERE Name = ? ''', (an_actor,))
                        row = cur.fetchall()
                        actor_id = row[0][0]
                        print("actor_id",actor_id)
                        cur.execute('''INSERT OR IGNORE INTO Movies_actors (Movie_id, Actor_id )
                            VALUES ( ?, ?)''', (movie_id, actor_id))
                        #if count % 5 == 0 : conn.commit()
                        conn.commit()
        cur.close()
    return

