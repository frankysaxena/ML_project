import numpy as np
from pymongo import MongoClient
import csv
import re
import string


connection = MongoClient()

db = connection["prolific_new"]

def get_banned_participants(user):
    banned_participants = db.user.find({'is_banned' : True})
    return banned_participants


def get_participants_on_ip(ip):
    X = db.ip_info.find({'ip' : ip}).distinct('user')
    return X

def get_num_participants_on_ip(ip):
    X = get_participants_on_ip(ip)
    return len(X)

def get_num_banned_participant_on_ip(ip):
    X = get_participants_on_ip(ip)
    return db.user.find({'is_banned' : True, '_id' : {'$in' : X}}).count()

def get_num_unbanned_participant_on_ip(ip):
    X = get_participants_on_ip(ip)
    return db.user.find({'is_banned' : False, '_id' : {'$in' : X}}).count()

csvfile = open('users_on_each_ip.csv', 'wb')
writer = csv.writer(csvfile)

x = db.ip_info.distinct('ip')

for ip in x:
    row = [ip, get_num_participants_on_ip(ip), get_num_banned_participant_on_ip(ip), get_num_unbanned_participant_on_ip(ip)]
    # print row
    writer.writerow(row)

csvfile.close()



csvfile = open('users_on_each_org.csv', 'wb')
writer = csv.writer(csvfile)

def get_participants_on_org(org):
    X = db.ip_info.find({'org' : org}).distinct('user')
    return X

def get_num_participants_on_org(org):
    X = get_participants_on_org(org)
    return len(X)

def get_num_banned_participant_on_org(org):
    X = get_participants_on_org(org)
    return db.user.find({'is_banned' : True, '_id' : {'$in' : X}}).count()

def get_num_unbanned_participant_on_org(org):
    X = get_participants_on_org(org)
    return db.user.find({'is_banned' : False, '_id' : {'$in' : X}}).count()

def make_safe_org(org):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return ''.join(c for c in org if c in valid_chars)


y = db.ip_info.distinct('org')



for org in y:
    safe_org = make_safe_org(org)
    row = [safe_org, get_num_participants_on_org(org), get_num_banned_participant_on_org(org), get_num_unbanned_participant_on_org(org)]
    # print row
    writer.writerow(row)

csvfile.close()


csvfile = open('users_on_each_hostname.csv', 'wb')
writer = csv.writer(csvfile)


def get_participants_on_host(hostname):
    X = db.ip_info.find({'hostname' : hostname}).distinct('user')
    return X

def get_num_participants_on_host(hostname):
    X = get_participants_on_host(hostname)
    return len(X)

def get_num_banned_participant_on_host(hostname):
    X = get_participants_on_host(hostname)
    return db.user.find({'is_banned' : True, '_id' : {'$in' : X}}).count()


def get_num_unbanned_participant_on_host(hostname):
    X = get_participants_on_host(hostname)
    return db.user.find({'is_banned' : False, '_id' : {'$in' : X}}).count()

z = db.ip_info.distinct('hostname')

for hostname in z:
    row = [hostname, get_num_participants_on_host(hostname), get_num_banned_participant_on_host(hostname), get_num_unbanned_participant_on_host(hostname)]
    # print row
    writer.writerow(row)

csvfile.close()
