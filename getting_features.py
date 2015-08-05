"""long winded procedure, without the cursor, but works nonetheless to 
show 10 random unbanned accounts."""

import pymongo
import random
from bson.objectid import ObjectId
from random import randint
import numpy as np



connection = pymongo.Connection()

db = connection["prolific_new"]
user = db["user"]
digital_finger_print = db["digital_finger_print"]
ip_info = db["ip_info"]

x = db.user.find({"is_facebook_email_verified_stored" : True }).count()

a = randint(0,x)

A = db.user.find({"is_facebook_email_verified_stored" : True }).limit(-1).skip(a).next()
B = db.user.find({"is_banned" : False }).limit(-1).skip(a).next()
C = db.digital_finger_print.find().limit(-1).skip(a).next()
D = db.ip_info.find().limit(-1).skip(a).next()


def index_devices():
	device_index = db.digital_finger_print.create_index([( 'device' , 1 )])
	return device_index

def get_distinct_devices():
	device_distinct = db.digital_finger_print.distinct('device')
	return device_distinct

def get_num_fb_friends(user):
	num_friends = user.get('num_facebook_friends_stored', -1)
	return num_friends

print get_num_fb_friends(A)

def get_device(digital_finger_print):
	user_device = digital_finger_print.get('device', -1)
	return user_device
#	return device_list.ensureIndex('Other')

print get_device(C)

def get_browser(digital_finger_print):
	user_browser = digital_finger_print.get('browser', -1)
	return user_browser

print get_browser(C)

def get_browser_version(digital_finger_print):
	user_browser_version = digital_finger_print.get('browser_version', -1)
	return user_browser_version

print get_browser_version(C)
	
def get_ip_data(ip_info):
	user_ip_data = ip_info.get('ip', -1)
	return user_ip_data

print get_ip_data(D)

print db.digital_finger_print.distinct("device")



# for index,device in enumerate(device_distinct)
# print device_distinct

