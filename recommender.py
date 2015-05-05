import csv
import numpy as np
import cPickle as pickle

percentage = 0.5
most_similar = 5
u2m = 'user_to_movie'
m2u2r = 'movie_to_user_to_rating'
user_to_movie = {}
movie_to_user_to_rating = {}
movie_to_user_to_rating_predicted = {}
movie_to_user_to_rating_true = {}


def loadData(title):
    with open(str(title)+'.p', 'rb') as fp:
        data = pickle.load(fp)
    return data


def prepData():
    max_movie = max(movie_to_user_to_rating.keys())
    cutoff_movie = int(percentage * float(max_movie))
    max_user = max(user_to_movie.keys())
    cutoff_user = int(percentage * float(max_user))
    
    for mid, val in movie_to_user_to_rating.items():
    #based on data set guarantee that user has reviewed >10 movies
        if mid > cutoff_movie:
            movie_to_user_to_rating_predicted[mid] = {}
            movie_to_user_to_rating_true[mid] = {}
            for user in val.keys():                
                movie_to_user_to_rating_predicted[mid][user] = -1
                movie_to_user_to_rating_true[mid][user] = movie_to_user_to_rating[mid][user]
                del movie_to_user_to_rating[mid][user]
                user_to_movie[user].remove(mid)

    
if __name__ == '__main__':
    user_to_movie = loadData(u2m)
    movie_to_user_to_rating = loadData(m2u2r)
    
    prepData()
    
    for mid in movie_to_user_to_rating_true.keys():
        for uid in movie_to_user_to_rating_true[mid].keys():
            for mid_rated in user_to_movie[uid]:
                #get similarity score
                    #calculate mean score for each movie    
                #get most_similar movies
                similarity(mid, mid_rated)
                #calculate rating
                #assign rating into movie_to_user_to_rating_predicted
                #DONE

    
    
    