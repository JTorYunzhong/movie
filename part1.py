import requests
import keys
import json
import sqlite3


def search_related_movies(movieName, key = keys.key_tastedive):
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
    for listRes in resp_json['Similar']['Results']:
        result.append(listRes['Name'])
    return result
    


def get_related_titles(list_input):
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
        A movie name..
    
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

def get_movie_rating(movieNameJson):
    str_rating = ""
    try:
        rating_ls = movieNameJson["Ratings"]
    except:
        rating_ls = []
    for typeRantingList in rating_ls:
        if typeRantingList["Source"] == "Rotten Tomatoes":
            str_rating = typeRantingList["Value"]
    if str_rating != "":
        try:
            int_rating = int(str_rating.split("%")[0])
        except:
            int_rating = 0
    else: int_rating = 0
    return int_rating

def get_sorted_recommendations(listMovieTitle):
    listMovie = get_related_titles(listMovieTitle)
    listMovie = sorted(listMovie, key = lambda movieName: (get_movie_rating(get_movie_data(listMovieTitle)), movieName), reverse=True)
    
    return listMovie

CACHE_FILENAME = "related_movies_cache.json"
def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def search_related_movies_withcache(movieName):
    cache_dict = open_cache()
    if movieName in cache_dict.keys():
        print("Using Cache")
        result = cache_dict[movieName]
    else:
        print("Fetching")
        result = search_related_movies(movieName)
        save_cache(cache_dict)
    return result

def load_data(ls_input):
    if ls_input != []:
        start = None
        count = 0
        conn = sqlite3.connect('info.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT max(id) FROM Movies' )
        if start is None : start = 0
        for a_input in ls_input:
            a_ls = get_related_titles(a_input)
            for a_movie_name in a_ls:
                title, year, genre, actor, plot, rottenTmatoes = None, None, None, None, None, None
                title = a_movie_name
                start = start + 1
                count = count + 1
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
                    actor = data_json["Actors"]
                except:
                    actor = None

                try:
                    plot = data_json["Plot"]
                except:
                    plot = None

                try:
                    rottenTomatoes = get_movie_rating(data_json)
                except:
                    rottenTomatoes = None

                cur.execute('''INSERT OR IGNORE INTO Movies (id, title, year, genre, actor, plot, rottenTomatoes)
                    VALUES ( ?, ?, ?, ?, ?, ?, ? )''', ( start, title, year, genre, actor, plot, rottenTomatoes))
                if count % 20 == 0 : conn.commit()
        cur.close()


#print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))