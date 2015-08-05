"""script to convert strings into arrays and then into a matrix for machine learning"""

from numpy import *
import numpy as np
from pprint import *

firstrow = 'users , country_of_residence_matching_location? , banned/unbanned'
firstrow = firstrow.split(',')
print firstrow

secondrow = 'Franky , no ,  yes'
secondrow = secondrow.split(',')
print secondrow	

#A = matrix('users , key_features , banned/unbanned ; Franky , no ,  yes')

#print A

#if secondrow = 'Franky , no , yes' 
#	secondrow = ' 1 ' , '1' ,  '1'

import pylab

first = ['1','2','3']
second = ['1', '2' , '3']

pylab.figure(1)
x = range(3)
pylab.xticks(x, first)
pylab.plot(x,second,"g")

pylab.show()
