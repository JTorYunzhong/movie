#still under process. Unfinished#

# movie
	Data sources:
a.	Origin: 
a)	Tastedive API: https://tastedive.com/read/api
Formats: JSON
Access: use API key and pass parameters through params_dict to access related movie title about certain input.  Caching is used.
b)	OMDB API: http://www.omdbapi.com/
Formats: JSON
Access: similar as the above. No cache. Stored at SQLite DB.
Summary of data: # records available 280,000 # records retrieved 6,000
 Table Movies: id PRIMARY KEY, title TEXT, year INTEGER, genre TEXT, actor TEXT, plot BLOB, rottenTomatoes TEXT, Table Actors: id, name,(others)
c)	Wikipedia page about a movie eg: https://en.wikipedia.org/wiki/The_Walk_(2015_film)
Formats: HTML
Access: Use BeautifulSoup to parse HTML data to get detailed plot (for word cloud visualization). No cache. 
	Data Structure
Create tree(graph) data structure to represent movies that have a same actor and tree depth is build according to release year of corresponding movies.
From table Actors, select certain actor and then connect to Cast (many to many) and Movies table to filter a series movies that an actor cast at. Then build tree according to movie release year.
	Interaction and Presentation Plans
Use command line prompts to provide options for user. 
a.	Movie list that are related to user input 
b.	Movie recommendation according to scores of user input(like IMDb) 
c.	Word cloud (use D3-Data driven documents JavaScript library) that could show most common words of detail plot about a movie 







