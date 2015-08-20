#! /usr/bin/env python
# coding: utf-8

# In[12]:



"""Creates the user's profile to input into ML. First matrix only banned,
second of only unbanned"""

from __future__ import division
from pymongo import MongoClient
import random
from bson.objectid import ObjectId
from random import randint
import numpy as np

from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer

import re

random.seed(4)

connection = MongoClient()

db = connection["prolific_new"]
# user = db["user"]
# digital_finger_print = db["digital_finger_print"]
# ip_info = db["ip_info"]
# ip = db["ip"]
# referral = db["referral"]

# x = db.user.find({"is_facebook_email_verified_stored" : True }).limit(10)
#
# print x


#a = randint(0,x)

# A = db.user.find({"is_banned" : True }).count()

#B = db.user.find({"is_banned" : False }).limit(-1).skip(a).next()

# db.digital_finger_print.find().limit(-1).skip(a).next()

# D = db.ip_info.find().limit(-1).skip(a).next()


# In[13]:

def get_database_record_linked_to_user(user, collection):
	user_id = user['_id']
	query = db[collection].find({'user' : user_id})
	return [document for document in query]

def get_database_record_linked_to_ip(ip, collection):
	ip_id = ip['_id']
	query = db[collection].find({'ip' : ip_id})
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

def get_participants_on_ip(ip):
	return get_database_record_linked_to_ip(ip, 'participants')


# In[14]:
def get_user_id_for_user(user):
	return get_database_record_linked_to_user(user, '_id')

def get_referrals_for_user(user):
	return get_database_record_linked_to_user(user, 'referral')

def get_prescreening_for_user(user):
	return get_database_record_linked_to_user(user, 'answer')

def get_email_for_user(user):
	return get_database_record_linked_to_user(user, 'email')

def unique(l):
	return np.unique(l).tolist()

def get_num_participants_on_ip(ip):
	participants = get_participants_on_ip(ip)
	num_participants = len(participants)
	return num_participants

def get_num_fb_friends(user):
	num_friends = user.get('num_facebook_friends_stored', -1)
	return num_friends

def get_digital_finger_print_values_for_user(user, k, default = "UNKNOWN"):
	digital_finger_prints = get_digital_finger_prints_for_user(user)
	return unique([dfp.get(k, default) for dfp in digital_finger_prints])


# In[15]:

def get_prescreening_answers_for_user(user, k, default = "UNKNOWN"):
	prescreening_answers = get_prescreening_for_user(user)
	return unique([psc.get(k, default) for psc in prescreening_answers])

def get_all_referrals_for_user(user, k, default = "UNKNOWN"):
	referrals = get_referrals_for_user(user)
	return unique([ref.get(k, default) for ref in referrals])

def get_respondant_answer(user):
	return get_prescreening_answers_for_user(user, "respondant")


# In[16]:

def get_num_deleted_prescreening_responses(user):
	num_deleted_responses = db.answer.find({ 'id' : user} , {'deleted': True}).count()
	return num_deleted_responses

def get_content_deleted_prescreening_responses(user):
	deleted_responses = db.answer.find({ 'id' : user} , {'deleted': True})
	return deleted_responses

def get_devices(user):
	return get_digital_finger_print_values_for_user(user, "device")

def get_browsers(user):
	return get_digital_finger_print_values_for_user(user, "browser")

def get_browser_versions(user):
	return get_digital_finger_print_values_for_user(user, "browser_version")

def get_browser_lang(user):
	return get_digital_finger_print_values_for_user(user, "browser_lang")

def get_referrals(user):
	referrals = get_referrals_for_user(user)
	return [referral.get('referred', '') for referral in referrals]

def num_referrals(user):
	num = get_referrals(user)
	num_referrals = len(num)
	return num_referrals

def get_banned_referrals(user):
	referredlist = get_all_referrals_for_user(user, "referred")
	num_banned = db.user.find( { 'id': { '$in': ['referredlist' , 'is_banned : True']}}).count()
	return num_banned

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
	while True:
		try:
			fraction = reject / tot
			return fraction
		except ZeroDivisionError:
			return  0

def get_current_country_of_residence(user):
	userdata = get_userdata_for_user(user)
	return [user.get('_current_country_of_residence' , '') for user in userdata]

def get_current_country_consistent_with_ip(user):
	userdata = get_userdata_for_user(user)
	return [user.get('_is_current_country_of_residence_consistent' , '') for user in userdata]

def get_feature_dict_for_user(user):
	feature_dict = {}
	feature_dict['num_facebook_friends'] = get_num_fb_friends(user)
	# feature_dict['firstname'] = user.get("firstname")
	# feature_dict['browsers'] = get_browsers(user)
	# feature_dict['devices'] = get_devices(user)
	# feature_dict['browser_version'] = get_browser_versions(user)
	feature_dict['browser_lang'] = get_browser_lang(user)
	feature_dict['num_ip'] = get_num_ips_for_user(user)
	feature_dict['ip_org'] = get_ips_orgs_for_user(user)
	feature_dict['current_country_of_residence'] = get_current_country_of_residence(user)
	feature_dict['is_email_verified'] = user.get("is_email_verified")
	# feature_dict['locations of user'] = get_locations_for_user(user)
	# feature_dict['number_of_emails'] =  get_num_emails_for_user(user)
	feature_dict['_is_current_country_of_residence_consistent_with_phone_location'] = get_is_current_country_of_residence_consistent_with_phone_location(user)
	feature_dict['is_phone_verified'] = get_phone_verification(user)
	feature_dict['is_facebook_verified'] = get_fb_verification(user)
	feature_dict['total_number_of_submissions'] = get_total_number_of_submissions(user)
	feature_dict['get_num_rejected_submissions'] = get_num_rejected_submissions(user)
 	feature_dict['get_fraction_rejected'] = get_fraction_rejected(user)
	feature_dict['get_num_participants_on_ip'] = get_num_participants_on_ip(user)
	feature_dict['num_referrals'] = num_referrals(user)
	feature_dict['prescreening_answers'] = get_respondant_answer(user)
	feature_dict['get_banned_referrals'] = get_banned_referrals(user)
	feature_dict['get_num_deleted_prescreening_responses'] = get_num_deleted_prescreening_responses(user)
 	feature_dict['get_content_deleted_prescreening_responses'] = get_content_deleted_prescreening_responses(user)
	feature_dict['is_current_country_of_residence_consistent_with_ip'] = get_current_country_consistent_with_ip(user)
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
	except (IndexError):
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
		feature_dict['current_country_of_residence'] = get_current_country_of_residence(user)[0]
	except IndexError:
		feature_dict['current_country_of_residence'] = "UNKNOWN"
	try:
		feature_dict['is_phone_verified'] = get_phone_verification(user)[0]
	except IndexError:
		feature_dict['is_phone_verified'] = "UNKNOWN"
	try:
		feature_dict['is_facebook_verified'] = get_fb_verification(user)[0]
	except IndexError:
		feature_dict['is_facebook_verified'] = "UNKNOWN"
	try:
		feature_dict['prescreening_answers'] = get_respondant_answer(user)[0]
	except IndexError:
		feature_dict['prescreening_answers'] = "UNKNOWN"
	try:
		feature_dict['get_content_deleted_prescreening_responses'] = get_content_deleted_prescreening_responses(user)[0]
	except IndexError:
		feature_dict['get_content_deleted_prescreening_responses'] = "UNKNOWN"
	try:
		feature_dict['is_current_country_of_residence_consistent_with_ip'] = get_current_country_consistent_with_ip(user)[0]
	except IndexError:
		feature_dict['is_current_country_of_residence_consistent_with_ip'] = 'UNKNOWN'
	return feature_dict
#
# def get_banned_users(user):
# 	userdata = get_userdata_for_user(user)
# 	return [user.get('is_banned', 'True') for user in userdata]
#
#
# def get_unbanned_users(user):
# 	userdata = get_userdata_for_user(user)
# 	return [user.get('is_banned', 'False') for user in userdata]

def get_list_of_feature_dicts(banned_users):
	feature_dicts = []
	for user in banned_users:
		feature_dicts.append(get_feature_dict_for_user(user))
	return feature_dicts

banned_users = [u for u in db.user.find({"is_banned" : True})] #Only banned users
random.shuffle(banned_users)

unbanned_users = [u for u in db.user.find({"is_banned" : False})] #unbanned users
random.shuffle(unbanned_users)

vec = DictVectorizer()

def get_list_of_banned_user_id(user):
	banned_users = [u for u in db.user.find({"is_banned" : True})]
	return [user.get('_id', '') for user in banned_users]

def get_list_of_unbanned_user_id(user):
	unbanned_users = [u for u in db.user.find({"is_banned" : False})]
	return [user.get('_id', '') for user in unbanned_users]

num = 5

banned_ids = get_list_of_banned_user_id(banned_users)[:num]

unbanned_ids = get_list_of_unbanned_user_id(unbanned_users)[:num]

banned_sample =   get_list_of_feature_dicts(banned_users[:num])

unbanned_sample = get_list_of_feature_dicts(unbanned_users[:num])


X = vec.fit_transform(banned_sample + unbanned_sample).toarray()
Y = np.array([1] * len(banned_sample) + [0] * len(unbanned_sample))
Z = np.array(banned_ids + unbanned_ids)


# print Z

# Z = vec.fit_transform(X + Yy).toarray()


# In[37]:

assert X.shape[0] == Y.shape[0] == Z.shape[0]
# assert X.shape[0] == Z.shape[0]

np.savetxt('features.dat', X, fmt='%-7.2f')
np.savetxt('response.dat', Y, fmt='%-7.2f')
np.savetxt('user_ids.dat', Z, fmt='%s')


# In[ ]:
