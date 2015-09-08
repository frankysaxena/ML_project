#score based on how many days since the user took the last study
#higher score = the user hasn't completed studies in a long time
#sort the list into descending order, so the higher score appears first

import datetime
from pymongo import MongoClient

connection = MongoClient()

db = connection["prolific_new"]

def get_database_record_linked_to_user(user, collection):
	user_id = user['_id']
	query = db[collection].find({'user' : user_id})
	return [document for document in query]

def get_submissions_for_user(user):
	return get_database_record_linked_to_user(user, 'submission')

# def get_completed_studies_date_for_user(user):
#     submissions = get_submissions_for_user(user)
#     return [submission.get('completed_at', '').order_by('participant', '-completed_at') for submission in submissions]

def get_last_completed_study_time_for_user(user):
    if db['submission'].find_one({'participant' : user['_id']}):
        last_submission = db['submission'].find({'participant' : user['_id']}).sort("started_at", -1)[0]
        return last_submission['started_at']

def get_submission_period_days(user):
    last_study_time_for_user = get_last_completed_study_time_for_user(user)
    current_time = datetime.datetime.now()
    # print type(last_study_time_for_user)
    b = datetime.datetime.now()
    diff = b - last_study_time_for_user
    return diff.days

def assign_score(user):
    period = get_submission_period_days(user)
    user_score = period
    return user_score


X = db.submission.find_one()

user = db.user.find_one({'_id' : X['participant']})

print assign_score(user)
