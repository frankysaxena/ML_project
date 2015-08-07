#! /usr/bin/env python

"""Creates the user's profile to input into ML"""

from __future__ import division
from pymongo import MongoClient
import random
from bson.objectid import ObjectId
from random import randint
import numpy as np

from sklearn.feature_extraction import DictVectorizer

random.seed(4)

connection = MongoClient()

db = connection["prolific_new"]
user = db["user"]
# digital_finger_print = db["digital_finger_print"]
ip_info = db["ip_info"]
ip = db["ip"]

#x = db.user.find({"is_facebook_email_verified_stored" : True }).count()

#a = randint(0,x)

A = db.user.find_one({"is_banned" : True })
#B = db.user.find({"is_banned" : False }).limit(-1).skip(a).next()

# db.digital_finger_print.find().limit(-1).skip(a).next()

# D = db.ip_info.find().limit(-1).skip(a).next()

def get_database_record_linked_to_user(user, collection):
	user_id = user['_id']
	query = db[collection].find({'user' : user_id})
	return [document for document in query]

def get_digital_finger_prints_for_user(user):
	return get_database_record_linked_to_user(user, 'digital_finger_print')

def get_ip_infos_for_user(user):
	return get_database_record_linked_to_user(user, 'ip_info')

def get_submissions_for_user(user):
	return get_database_record_linked_to_user(user, 'submission')

def get_userdata_for_user(user):
	return get_database_record_linked_to_user(user, 'user')

def get_phone_verification_for_user(user):
	return get_database_record_linked_to_user(user, 'phone_verification')

def get_database_record_linked_to_ip(ip, collection):
	ip_id = ip['_id']
	query = db[collection].find({'ip' : ip_id})
	return [document for document in query]

def unique(l):
	return np.unique(l).tolist()
#
# def get_users_for_ip(ip):
# 	return get_database_record_linked_to_ip(ip, 'user')
#
# def get_participants_on_ip(ip):
# 	participants_to_ip = ip.get('participants', -1)
# 	return participants_to_ip
#
# def get_num_participants_on_ip(ip):
# 	participants = get_participants_on_ip(ip)
# 	num_participants = len(participants)
# 	return num_participants

#
# def get_each_user_for_ip(ip):
# 	each_ip = ip.get('ip')
# 	return each_ip

def get_distinct_devices():
	device_distinct = db.digital_finger_print.distinct('device')
	return device_distinct

def get_num_fb_friends(user):
	num_friends = user.get('num_facebook_friends_stored', -1)
	return num_friends

def get_digital_finger_print_values_for_user(user, k, default = "UNKNOWN"):
	digital_finger_prints = get_digital_finger_prints_for_user(user)
	return unique([dfp.get(k, default) for dfp in digital_finger_prints])

def get_devices(user):
	return get_digital_finger_print_values_for_user(user, "device")

def get_browsers(user):
	return get_digital_finger_print_values_for_user(user, "browser")

def get_browser_versions(user):
	return get_digital_finger_print_values_for_user(user, "browser_version")

def get_browser_lang(user):
	return get_digital_finger_print_values_for_user(user, "browser_lang")

def get_ips_for_user(user):
	ip_infos = get_ip_infos_for_user(user)
	return [ip_info.get('ip','') for ip_info in ip_infos]

def get_num_ips_for_user(user):
	ip_infos = get_ips_for_user(user)
	num_ips = len(ip_infos)
	return num_ips

def get_ips_orgs_for_user(user):
	ip_infos = get_ip_infos_for_user(user)
	return [ip_info.get('org','') for ip_info in ip_infos]

def get_locations_for_user(user):
	userdata = get_userdata_for_user(user)
	return [user.get('_locations','') for user in userdata]

def get_emails_for_user(user):
	userdata = get_userdata_for_user(user)
	return [user.get('email','') for user in userdata]

def get_num_emails_for_user(user):
	emails_for_user = get_emails_for_user(user)
	num_emails = len(emails_for_user)
	return num_emails

def get_fb_verification(user):
	userdata = get_userdata_for_user(user)
	return [user.get('is_facebook_email_verified_stored', '') for user in userdata]

def get_is_current_country_of_residence_consistent_with_phone_location(user):
	userdata = get_userdata_for_user(user)
	return [user.get("_is_current_country_of_residence_consistent_with_phone_location",'') for user in userdata]

def get_phone_verification(user):
	phonedata = get_phone_verification_for_user(user)
	return [user.get('is_verified','') for user in phonedata]

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
	value = float('nan')
	if tot != 0:
		fraction = reject / tot
		return fraction
	else:
		return  value

def get_feature_dict_for_user(user):
	feature_dict = {}
	feature_dict['num_facebook_friends'] = get_num_fb_friends(user)
	feature_dict['firstname'] = user.get("firstname")
	feature_dict['ethnicity'] = user.get("_ethnicity")
	feature_dict['browsers'] = get_browsers(user)
	feature_dict['devices'] = get_devices(user)
	feature_dict['browser_version'] = get_browser_versions(user)
	feature_dict['browser_lang'] = get_browser_lang(user)
	feature_dict['num_ip'] = get_num_ips_for_user(user)
	feature_dict['ip_org'] = get_ips_orgs_for_user(user)
	feature_dict['current_country_of_residence'] = user.get("_current_country_of_residence")
	feature_dict['is_email_verified'] = user.get("is_email_verified")
	feature_dict['locations of user'] = get_locations_for_user(user)
	feature_dict['number_of_emails'] =  get_num_emails_for_user(user)
	feature_dict['_is_current_country_of_residence_consistent_with_phone_location'] = get_is_current_country_of_residence_consistent_with_phone_location(user)
	feature_dict['is_phone_verified'] = get_phone_verification(user)
	feature_dict['is_facebook_verified'] = get_fb_verification(user)
	feature_dict['total_number_of_submissions'] = get_total_number_of_submissions(user)
	feature_dict['get_num_rejected_submissions'] = get_num_rejected_submissions(user)
 	feature_dict['get_fraction_rejected'] = get_fraction_rejected(user)
	# feature_dict['get_num_participants_on_ip'] = get_num_participants_on_ip(user)
	try:
		feature_dict['devices'] = get_devices(user)[0]
	except IndexError:
		feature_dict['devices'] = "UNKNOWN"
	try:
		feature_dict['browsers'] = get_browsers(user)[0]
	except IndexError:
		feature_dict['browsers'] = "UNKNOWN"
	try:
		feature_dict['browser_lang'] = get_browser_lang(user)[0]
	except IndexError:
		feature_dict['browser_lang'] = "UNKNOWN"
	try:
		feature_dict['ip_org'] = get_ips_orgs_for_user(user)[0]
	except IndexError:
		feature_dict['ip_org'] = "UNKNOWN"
	try:
		feature_dict['browser_version'] = get_browser_versions(user)[0]
	except IndexError:
		feature_dict['browser_version'] = "UNKNOWN"
	try:
		feature_dict['locations of user'] = get_locations_for_user(user)[0]
	except IndexError:
		feature_dict['locations of user'] = "UNKNOWN"
	try:
		feature_dict['_is_current_country_of_residence_consistent_with_phone_location'] = get_is_current_country_of_residence_consistent_with_phone_location(user)[0]
	except IndexError:
		feature_dict['_is_current_country_of_residence_consistent_with_phone_location'] = "UNKNOWN"
	try:
		feature_dict['is_phone_verified'] = get_phone_verification(user)[0]
	except IndexError:
		feature_dict['is_phone_verified'] = "UNKNOWN"
	try:
		feature_dict['is_facebook_verified'] = get_fb_verification(user)[0]
	except IndexError:
		feature_dict['is_facebook_verified'] = "UNKNOWN"
	return feature_dict


#print get_feature_dict_for_user(A)

def get_list_of_feature_dicts(users):
	feature_dicts = []
	for user in users:
		feature_dicts.append(get_feature_dict_for_user(user))
	return feature_dicts


users = [u for u in db.user.find({"is_banned" : True})] #Only banned users
random.shuffle(users)

#print get_list_of_feature_dicts(users[:10])

vec = DictVectorizer()

sample =   get_list_of_feature_dicts(users[:10])

print vec.fit_transform(sample).toarray()

print vec.get_feature_names()
