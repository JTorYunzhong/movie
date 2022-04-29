# movie
# package
python: requests

JavaScript: d3.layout.cloud.js, d3.v2.js
# How to run this project
My own API keys are included in keys.py. Due to rate limit of API. I suggest other uses to register their own API key. 

For first time running, run model.py to initialize info.sqlite for future use.

This project mainly interacts with user through command line prompts. I provide 4 options here. Details can be seen in Interaction and Presentation Options section.Run main.py to seeactual effect.

# Data sources:
## a)Tastedive API: https://tastedive.com/read/api
Formats: JSON
Access:  Create an account of the website mentioned above and get an API key. Use API key and pass parameters through params_dict to access related movie title about certain input. 

## b)OMDB API: http://www.omdbapi.com/
Formats: JSON
Access: similar as the above. Stored each new record data into SQLite DB. If it is a piece of old data, look it up directly at database.
Summary of data: # records available 170,000 # records retrieved 2765
Table Movies: id PRIMARY KEY, Title TEXT, Year INTEGER, Genre TEXT, Plot BLOB, ImdbRating TEXT, 
Table Actors: id PRIMARY KEY, name; 
Table Movies_actors: FOREIGN KEY Movie_id, FOREIGN KEY Actor_id. Record many-to-many relationship between movie and actor. 

# Data Structure
In KevinBacon.py, I provide a function that construct a graph that each node represents a movie or an actor or actress from data of database, a function using BFS that compute Kevin Bacon number of two actor or actress and average Kevin Bacon number of the whole connected graph.

# Interaction and Presentation Options
Use command line prompts to provide options for user. 

a.	Movie list that are related to user input 

b.	Movie recommendation according to IMDb scores

c.	Word cloud (use D3-Data driven documents JavaScript library) that could show most common word of plot about searched movies. The visual function in word_visual.py is going to generate a JavaScript file about most common 100 word and its corresponding font size. Then user need to open word_visual.html (JavaScript code call d3 library and read word_visual.js to display word cloud) to see actual visualization results.  

d.	Kevin Bacon number of two input actors or actresses and average Kevin Bacon number of connected graph taking the first name as start node. Under main menu, user could select mode 1, mode 3 and mode 4(user have to run a round of mode 1 before enter mode 2). Under each mode, user would see instructions about the functionality and how to use each mode in the form of command line prompt. 









