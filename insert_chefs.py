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
               fname = llist[0].strip()
               lname = llist[1].strip()
               chefdbid = int(llist[2])
           else:   
               fname = llist[0].strip()
               lname = ""
               chefdbid = int(llist[1])

           print "inserting", line
           email = lname + "_" + str(chefdbid) + "@gmail.com"

           user = models.User(email, "", fname, lname, "user")
           models.db.session.add(user)
           models.db.session.commit()

           # assign random country to each chef
           countryid = random.randint(1, 260)
           zipcode = random.randint(1, 99999)

           chef = models.Chef("", "", "", "", zipcode, countryid, 1234567890, 0.0, user.userid, chefdbid)
           models.db.session.add(chef)
           models.db.session.commit()

           print "done"

main()
