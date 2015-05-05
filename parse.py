import csv
import numpy as np
import cPickle as pickle

# Global variables


def read_movies():
	count = 0
	with open("data/movies.csv") as moviefile:
		a = csv.reader(moviefile)
		for row in a:
			#print ', '.join(row)
			print row[1]
			count += 1
			if count == 30:
				break

def read_ratings():
	with open("data/ratings.csv") as ratingsfile:

		highest_movie_id = 0
		highest_user_id = 0

		a = csv.reader(ratingsfile)
		next(a)
		for row in a:
			if int(row[0]) > highest_user_id:
				highest_user_id = int(row[0])
			if int(row[1]) > highest_movie_id:
				highest_movie_id = int(row[1])

		user_to_movie = {}
		movie_to_user_to_rating = {}

		ratingsfile.seek(0)
		next(a)
		for row in a:
			user = int(row[0])
			movie = int(row[1])
			rating = float(row[2])

			if user not in user_to_movie:
				user_to_movie[user] = [movie]
			else:
				user_to_movie[user].append(movie)

			if movie not in movie_to_user_to_rating:
				movie_to_user_to_rating[movie] = {}
				movie_to_user_to_rating[movie][user] = rating
			else:
				movie_to_user_to_rating[movie][user] = rating

	ratingsfile.close()

	print len(user_to_movie)
	print len(movie_to_user_to_rating)

	# with open("data/ratings.csv") as ratingsfile:

	# 	a = csv.reader(ratingsfile)
	# 	next(a)
	# 	for row in a:

def dumpData(title, data):
    with open(str(title)+'.p', 'wb') as fp:
        pickle.dump(data, fp)
        
def loadData(title):
    with open(title, 'rb') as fp:
        data = pickle.load(fp)
    return data

if __name__ == '__main__':
	read_ratings()