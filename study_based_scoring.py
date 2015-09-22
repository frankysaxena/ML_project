from pymongo import MongoClient

connection = MongoClient()

db = connection["prolific_new"]

def get_database_record_linked_to_user(user, collection):
	user_id = user['_id']
	query = db[collection].find({'user' : user_id})
	return [document for document in query]

def get_submissions_for_user(user):
	return get_database_record_linked_to_user(user, 'submission')

def get_total_number_of_submissions(user):
	total = get_submissions_for_user(user)
	total_submissions = len(total)
	return total_submissions

def get_rejected_submissions(user):
	submissions = get_submissions_for_user(user)
	return [submission.get('is_approved', 'False') for submission in submissions]

def get_num_rejected_submissions(user):
	rejected = get_rejected_submissions(user)
	num_rejected = len(rejected)
	return num_rejected

def get_fraction_rejected(user):
	reject = get_num_rejected_submissions(user)
	tot = get_total_number_of_submissions(user)
	while True:
		try:
			fraction = reject / tot
			return fraction
		except ZeroDivisionError:
			return  0

def assign_score(user):
    fraction = get_fraction_rejected(user)
    score = fraction
    return score


X = db.submission.find_one()

user = db.user.find({'_id' : X['participant']})


for a in user:
	print assign_score(user)
# for user in X:
# 	print assign_score(user)
