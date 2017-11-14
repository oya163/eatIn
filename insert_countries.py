import math
import random
import sys

from os import listdir
from os.path import isfile, join, curdir
from collections import defaultdict

import models

FILENAME = "./datasets/countries.dat"

def main():
   with open(FILENAME) as f:
       for line in f:
           name = line.split(',')[0]
           abbr = line.split(',')[1]

           print "inserting", name, abbr

           country = models.Country(name, abbr)
           models.db.session.add(country)
           models.db.session.commit()

           print "done"

main()
