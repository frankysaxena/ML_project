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

def get_completed_studies_date_for_user(user):
    submissions = get_submissions_for_user(user)
    return [submission.get('completed_at', '') for submission in submissions]

def get_last_completed_study_time_for_user(user):
    all_studies = get_completed_studies_date_for_user(user)
    last_study = all_studies.order_by('participant','-completed_at')
    return last_study

def get_submission_period_days(user):
    last_study_time_for_user = get_last_completed_study_time_for_user(user)
    current_time = datetime.datetime.now()
    a = datetime.datetime.strptime(last_study_time_for_user, '%Y-%m-%d %H:%M')
    b = datetime.datetime.now()
    diff = b - a
    return diff.days

def assign_score(user):
    period = get_submission_period_days(user)
    user_score = period
    return user_score

print assign_score('5363606dfdf99b56c3a59bf3')
