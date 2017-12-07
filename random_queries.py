import math
import random
import sys
import time

from datetime import date, datetime
from os import listdir
from os.path import isfile, join, curdir
from collections import defaultdict

import models

from models import app
from models import db

def main():
    chef_range = list(range(65367, 98050))
    food_range = list(range(1, 68517))

    total_time = 0.0

    for i in range(1, 10000):
        chefid = random.choice(chef_range)
        foodid = random.choice(food_range)

        start = time.time()

        chef = models.get_chef_by_id(chefid)
        fooditem = models.get_fooditem_by_id(foodid)
        orders = models.get_orders_by_chef_id(chefid)

        end = time.time()
        t_time = end - start
        total_time = total_time + t_time

        #print "query: ", t_time, total_time, i

    print "avg time: ", total_time/10000.0

    #models.db.session.commit()
    #end = time.time()
    #t_time = end - start

    #print t_time

main()
