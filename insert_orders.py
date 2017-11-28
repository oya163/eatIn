import math
import random
import sys

from os import listdir
from os.path import isfile, join, curdir
from collections import defaultdict

import models

from models import app
from models import db

def main():
    # populate mappings
    chefs = models.get_all_chefs()
    customers = models.get_all_customers()
    fooditems = models.get_all_fooditems()

    # generate 1 million random orders
    for i in range(1, 1000000):
        chef = random.choice(chefs)
        cust = random.choice(customers)
        food = random.choice(fooditems)

        # make random req_date

        r = create_order(cust.cutomerid, chef.chefid, food.foodid, rd, "")
        print "added  order", cust.custid, chef.chefid, food.foodid, rd

main()
