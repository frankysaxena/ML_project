#get the ratio of participants that are eligible to the studies Available
#link the white_list (if a user is eligible for a study, and try to assign a score depending on the study)
from pymongo import MongoClient
import matplotlib.pyplot as plt
from numpy.random import normal
import sys
import pylab

connection = MongoClient()


db = connection["prolific_new"]

def get_database_record_linked_to_study(study, collection):
	study_id = study['_id']
	query = db[collection].find({'study' : study_id})
	return [document for document in query]

def get_studies_data(study):
	return get_database_record_linked_to_study(study, 'study')

def get_available_places(study):
	study_data = get_studies_data(study)
	return study.get('total_available_places', '')

def get_number_of_eligible_participants(study):
	studies = get_studies_data(study)
	total = study.get('_number_of_eligible_participants', '')
	if total == '':
		return 0
	else:
		return total

def get_white_list_eligible(study):
	study_data = get_studies_data(study)
	


def get_ratio_of_available_to_eligible(study):
	available_places = float(get_available_places(study))
	eligible_participants = float(get_number_of_eligible_participants(study))
	while True:
		try:
			fraction = available_places / eligible_participants
			return fraction
		except ZeroDivisionError:
			return  0

X = db.study.find()

for study in X:
	# A = get_available_places(study), get_number_of_eligible_participants(study)
	B = float(get_available_places(study)), float(get_number_of_eligible_participants(study)), float(get_ratio_of_available_to_eligible(study))
	C = float(get_ratio_of_available_to_eligible(study))
	print C
