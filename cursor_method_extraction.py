import pymongo
import random
from bson.objectid import ObjectId
from random import randint

connection = pymongo.Connection()

db = connection["prolific_new"]
users = db["user"]

cursor = users.find({"is_banned" : True }).limit(10)
for users in cursor:
	print users



#cursor2 = users.find({"is_banned" : False }).limit(10)
#for users in cursor2:
#	print users




"""
Tried to implement a random 10 generator but some issues rose especially with the ' i = 0, 
incorrect syntax' 
"""

db.user.ensureIndex( { random_point: '2d' } )

for ( i == 0 , i < 10 , ++i ) {
    db.user.insert( { key: i, random_point: [Math.random(), 0] } );
}

cursor = user.find( { random_point : { $near : [Math.random(), 0] } } ).limit( 10 )

for user in cursor:
	print user




#x = random.randint(0,274)

#cursor = users.find({"is_banned" : True }).limit(-1).skip(23).next()
#for users in cursor: 
#	print 'Banned accounts: % s' % cursor

#db.user.save( { key : 1, ..., random : Math.random() } )

#rand = Math.random()
#result = db.user.findOne( { key : 2, random : { $gte : rand } } )
#if ( result == null ) {
#  result = db.user.findOne( { key : 2, random : { $lte : rand } } )
#}




#cursor = user.find({"is_banned" : True })
#for user in cursor:
#	print user

	
#cursor = user.find({ "is_banned" : True }).limit(10)
#for user in cursor: 
#	print user



#def get_random_doc():
#    count = users.count()
#    cursor = users.find({"is_banned" : True})[random.randrange(count)]
#    return 


