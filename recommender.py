import csv
import numpy as np
import cPickle as pickle
import math

percentage = 0.5
k_most_similar = 5
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
                #MAYBE OMIT THIS BECAUSE THE SPARSE POPULARIZATION OF -1s
                movie_to_user_to_rating_predicted[mid][user] = -1
                movie_to_user_to_rating_true[mid][user] = movie_to_user_to_rating[mid][user]
                del movie_to_user_to_rating[mid][user]
                user_to_movie[user].remove(mid)

def similarity (movie_id_1, movie_id_2):
    product = 0.0
    magnitude1 = 0.0
    magnitude2 = 0.0

    # Movie to be predicted
    for user in movie_to_user_to_rating[movie_id_1]:
        if user in movie_to_user_to_rating[movie_id_2]:
            product = product + float(movie_to_user_to_rating[movie_id_1][user])*float(movie_to_user_to_rating[movie_id_2][user])
        magnitude1 = magnitude1 + movie_to_user_to_rating[movie_id_1][user]**2

    # Movie that it is being compared with
    max_user = max(user_to_movie.keys())
    cutoff_user = int(percentage * float(max_user))
    for user in movie_to_user_to_rating[movie_id_2]:
        if user <= cutoff_user:
            magnitude2 = magnitude2 + movie_to_user_to_rating[movie_id_2][user]**2

    return product/float((math.sqrt(magnitude1) + math.sqrt(magnitude2)))

def predicted_rating (most_similar, uid):

    numerator = 0.0
    denominator = 0.0
    for tupl in most_similar:
        numerator = numerator + movie_to_user_to_rating[tupl[1]][uid]*tupl[0]
        denominator = denominator + tupl[0]
    return numerator/denominator
    
if __name__ == '__main__':
    user_to_movie = loadData(u2m)
    movie_to_user_to_rating = loadData(m2u2r)
    
    print("getting data")
    prepData()
    
    print("crunch time")
    maxSimilarities = []
    for mid in movie_to_user_to_rating_true.keys():
        for uid in movie_to_user_to_rating_true[mid].keys():
            #guaranteed at least 10 reviews
            for mid_rated in user_to_movie[uid]:
                #get similarity score
                    #calculate mean score for each movie    
                #get most_similar movies
                sim_score = similarity(mid, mid_rated)
                if len(maxSimilarities) < k_most_similar:
                    maxSimilarities.append((sim_score, mid_rated))
                else:                                
                    min_max_sim_score = min(maxSimilarities)
                    if sim_score > min_max_sim_score:
                        maxSimilarities.append((sim_score, mid_rated))
                        maxSimilarities.remove(min_max_sim_score)
                        
                #calculate rating and assign rating into movie_to_user_to_rating_predicted
            movie_to_user_to_rating_predicted[mid][uid] = predicted_rating(maxSimilarities, uid)
                #DONE

print "test"
addition = 0
for mid in movie_to_user_to_rating_predicted.keys():
    for uid in movie_to_user_to_rating_predicted[mid]:
        sum += (movie_to_user_to_rating_predicted[mid][uid] - movie_to_user_to_rating_true[mid][uid])**2
        
RMSE = math.sqrt(addition)
print RMSE