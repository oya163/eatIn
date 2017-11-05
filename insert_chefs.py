import math
import random
import sys

from os import listdir
from os.path import isfile, join, curdir
from collections import defaultdict

import models

FILENAME = "./datasets/chefdb.dat"

def main():
   with open(FILENAME) as f:
       for line in f:
           llist = line.split('|')

           if (llist >= 2):
               fname = llist[0]
               lname = llist[1]
               chefdbid = llist[2]
           else:   
               fname = llist[0]
               lname = ""
               chefdbid  llist[1]

           print "inserting", line

           user = models.User( stuff );

           chef = models.Chef( ... );

           models.db.session.add(country)
           models.db.session.commit()

           print "done"

main()
