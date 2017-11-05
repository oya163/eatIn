import math
import random
import sys

from os import listdir
from os.path import isfile, join, curdir
from collections import defaultdict

import models

def main():
    randusers = random.sample(range(32747, 60001), 1000)

    for randuser in randusers:
           print "inserting to customer", randuser

           # assign random country to each chef
           countryid = random.randint(1, 260)
           zipcode = random.randint(1, 99999)

           customer = models.Customer("", "", "", "", zipcode, countryid, 1234567890, "", randuser)
           models.db.session.add(customer)
           models.db.session.commit()

           print "done"

main()
