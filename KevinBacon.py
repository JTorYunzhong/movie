import pathlib
from queue import Queue
import sqlite3
import string

""""
# Definition for a Node.
class Node:
    def __init__(self, name, neighbors = None):
        self.name = name
        self.neighbors = neighbors if neighbors is not None else []
"""
def create_graph():
    '''create graph file from data of info.sqlite 
        -------------------
        
        Returns
        -------
        movie_2_actor
                     key: movie name, value: list of actor name
        actor_2_movie  
                     key: actor name, value: list of movie name
    '''
    conn = sqlite3.connect('info.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT Movies.Title,Actors.Name
            FROM Movies,Movies_actors,Actors
            WHERE Movies.Id = Movies_actors.Movie_id and Movies_actors.Actor_id = Actors.Id''')
    rows = cur.fetchall()
    movie_2_actor = {} 
    actor_2_movie = {} 
    for row in rows :
        movie_name = row[0]
        actor_name = row[1]
        if movie_name not in movie_2_actor.keys():
            movie_2_actor[movie_name] = [actor_name]
        else:
            movie_2_actor[movie_name].append(actor_name)
        if actor_name not in actor_2_movie.keys():
            actor_2_movie[actor_name] = [movie_name]
        else:
            actor_2_movie[actor_name].append(movie_name)

    return movie_2_actor, actor_2_movie


def kevin_bacon(movie2actor, actor2movie, start, dest):
    '''given the name of an actor(dest), to find his/her Kevin-Bacon-number(start-number) and 
       the shortest alternating sequence of actor-movie pairs that lead to
       Kevin Bacon. And, to find the average distance of all actors to KB.
        -------------------

        Returns
        -------
        None
    '''
    # key: movie name or actor name, val: list, first item is name of previous node, second item is distanc. 
    record = {}
    # whether this node has been visited
    visited = set()
    q = Queue(0)
    distance = -1
    q.put(start)
    visited.add(start)
    record[start] =[start]
    Unreachable = False 
    while(not q.empty()):
        size = q.qsize()
        distance += 1
        for i in range(size):
            if distance > 20:
                Unreachable = True
                print("Unreachable. Please input more movie so than Kevin Bacon number is more accurate")
            cur_actor = q.get()
            record[cur_actor].append(distance)
            for j in actor2movie[cur_actor]:
                if j not in visited:
                    visited.add(j)
                    q.put(j)
                    record[j] = [cur_actor]
        if Unreachable == True:
            break
        size = q.qsize()
        distance += 1
        for i in range(size):
            cur_movie = q.get()
            record[cur_movie].append(distance)
            for j in movie2actor[cur_movie]:
                if j not in visited:
                    visited.add(j)
                    q.put(j)
                    record[j] = [cur_movie]
    if Unreachable == True:
        return
    try:
        number = record[dest][1]
    except:
        print("Unreachable. Please input more movie so than Kevin Bacon number is more accurate")
        return
    print(start,"-number of",dest,"is",number/2)

    print("shortest path:")
    cur_actor = dest
    while(True):
        print(cur_actor, "was in", record[cur_actor][0])
        cur_movie = record[cur_actor][0]
        print("with",record[cur_movie][0],".")
        if record[cur_movie][0] == start:
            break
        else:
            cur_actor = record[cur_movie][0]

    print("average distance of all actors and actressres to", start,":")
    sum_dist, count = 0, 0
    for name in actor2movie.keys():
        if name in record.keys():
            count += 1
            sum_dist += record[name][1]
    ave_dist = 0.5 * sum_dist / (count - 1) # minus start node 
    print(ave_dist)

def run():
    movie2actor, actor2movie = create_graph()
    print("Please enter two names of actors, separate by / Like:A/B. This program gonna show you A-number of B, shortest path, and average distance of all actors to A.")
    print("Or enter quit to end the program" )        
    while(True):
        val = input("--")
        if val == "quit":
            break
        val = val.split("/")
        if len(val) < 2:
            print("Invalid input. Please enter again.")
            continue
        A, B = val[0], val[1]
        if A not in actor2movie.keys() or B not in actor2movie.keys():
            print("Invalid input. Please enter again.")
        else:
            kevin_bacon(movie2actor, actor2movie, A, B)


