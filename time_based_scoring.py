#score based on how many days since the user took the last study
#higher score = the user hasn't completed studies in a long time
#sort the list into descending order, so the higher score appears first

import datetime
from pymongo import MongoClient
import matplotlib.pyplot as plt
from numpy.random import normal
import sys
import pylab


connection = MongoClient()

db = connection["prolific_new"]

def get_database_record_linked_to_user(user, collection):
	user_id = user['_id']
	query = db[collection].find({'user' : user_id})
	return [document for document in query]

def get_submissions_for_user(user):
	return get_database_record_linked_to_user(user, 'submission')

def get_last_completed_study_time_for_user(user):
	if db['submission'].find_one({'participant' : user['_id']}):
		last_submission = db['submission'].find({'participant' : user['_id']}).sort("started_at", -1)[0]
		return last_submission['started_at']

def get_submission_period_days(user):
	last_study_time_for_user = get_last_completed_study_time_for_user(user)
	if  last_study_time_for_user is not None:
		current_time = datetime.datetime.now()
		b = datetime.datetime.now()
		diff = b - last_study_time_for_user
		return diff.days
	else:
		return 0

def assign_score(user):
	period = get_submission_period_days(user)
	user_score = period
	return user_score

# def get_num_participants_on_each_score(user):
# 	scores = assign_score(user)
# 	num_participants = len(scores)
# 	return num_participants
#
# for score in db.submission.find():
#	 print get_num_participants_on_score(score)

row_list = []

for participant in db.user.find():
	row = assign_score(participant)
	row_list.append(row)
	print assign_score(participant), participant['_id']


# n = len(row_list)
# plt.hist(row_list, range=[0, 300], bins = n)
# plt.title("Numbers of users on each score")
# pylab.ylim([0,800])
# plt.xlabel("Score")
# plt.ylabel("Number of users")
# plt.show()
