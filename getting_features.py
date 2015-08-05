#! /usr/bin/env python 

"""long winded procedure, without the cursor, but works nonetheless to 
show 10 random unbanned accounts."""

from pymongo import MongoClient
import random
from bson.objectid import ObjectId
from random import randint
import numpy as np

random.seed(4)

connection = MongoClient()

db = connection["prolific_new"]
user = db["user"]
# digital_finger_print = db["digital_finger_print"]
ip_info = db["ip_info"]

x = db.user.find({"is_facebook_email_verified_stored" : True }).count()

a = randint(0,x)

A = db.user.find_one({"_id" : ObjectId("5367e53cfdf99b05d1acaabd")})
B = db.user.find({"is_banned" : False }).limit(-1).skip(a).next()

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

C = get_digital_finger_prints_for_user(A)
# print C

def get_distinct_devices():
	device_distinct = db.digital_finger_print.distinct('device')
	return device_distinct

def get_num_fb_friends(user):
	num_friends = user.get('num_facebook_friends_stored', -1)
	return num_friends

# print get_num_fb_friends(A)

def unique(l):
	return np.unique(l).tolist()


def get_digital_finger_print_values_for_user(user, k, default = "UNKNOWN"):
	digital_finger_prints = get_digital_finger_prints_for_user(user)
	return unique([dfp.get(k, default) for dfp in digital_finger_prints])

def get_devices(user):
	return get_digital_finger_print_values_for_user(user, "device")

def get_browsers(user):
	return get_digital_finger_print_values_for_user(user, "browser")

def get_browser_versions(user):
	return get_digital_finger_print_values_for_user(user, "browser_version")

def get_ips_for_user(user):
	ip_infos = get_ip_infos_for_user(user)
	return [ip_info.get('ip',' ') for ip_info in ip_infos]

# print get_devices(A)
# print get_browsers(A)
# print get_browser_versions(A)
# print get_ips_for_user(A)



def get_feature_dict_for_user(user):
	feature_dict = {}
	feature_dict['num_facebook_friends'] = get_num_fb_friends(user)
	try:
		feature_dict['device'] = get_devices(user)[0]
	except IndexError:
		feature_dict['device'] = "UNKNOWN"


	return feature_dict


print get_feature_dict_for_user(A)

def get_list_of_feature_dicts(users):
	feature_dicts = []
	for user in users:
		feature_dicts.append(get_feature_dict_for_user(user))
	return feature_dicts


users = [u for u in db.user.find({})]
random.shuffle(users)

print get_list_of_feature_dicts(users[:10])

