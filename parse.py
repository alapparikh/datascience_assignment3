import csv
import numpy as np

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

		utility_matrix = np.zeros((highest_user_id, highest_movie_id))

		ratingsfile.seek(0)
		next(a)
		for row in a:
			utility_matrix[int(row[0])][int(row[1])] = int(row[2])

	ratingsfile.close()

	print utility_matrix 

	# with open("data/ratings.csv") as ratingsfile:

	# 	a = csv.reader(ratingsfile)
	# 	next(a)
	# 	for row in a:


if __name__ == '__main__':
	read_ratings()