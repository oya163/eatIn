import math
import random
import sys

from os import listdir
from os.path import isfile, join, curdir
from collections import defaultdict

import models

FILENAME = "./datasets/meals_data.dat"

def main():
   with open(FILENAME) as f:
       for line in f:
           llist = line.split('|~|')

           fn_id = llist[0].strip()
           if (len(fn_id) > 10):
               fn_id = ""

           foodname = llist[1].strip()
           fn_url = llist[2].strip()[2:]

           # pick random price
           price = float(random.randint(500.0, 5000.0)/100.0)
           cooktime = random.randrange(15, 180, 5)

           print "inserting", fn_id, "::", foodname, "::", price, cooktime

           food_item = models.FoodItem(foodname, "", cooktime, 0.0, price, fn_id)
           models.db.session.add(food_item)
           models.db.session.commit()

main()
