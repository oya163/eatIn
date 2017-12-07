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
    start_date = date.today().replace(day=1, month=1).toordinal()
    end_date = date.today().toordinal()

    print start_date, end_date 

    # populate mappings
    chefs = models.get_all_chefs()
    customers = models.get_all_customers()
    fooditems = models.get_all_fooditems()
    total_time = 0.0

    start = time.time()
    # generate 1 million random orders
    for i in range(1, 10000):
        random_day = date.fromordinal(random.randint(start_date, end_date))

        chef = random.choice(chefs)
        cust = random.choice(customers)
        food = random.choice(fooditems)

        comment = "random order " + str(i)

        # make random req_date
        rd = random_day.strftime('%Y-%m-%d')
        order_date = datetime.now()

        # add order
        #start = time.time()

        order = models.OrderFood(cust.customerid, chef.chefid, food.foodid, order_date, rd, comment)
        models.db.session.add(order)

        #end = time.time()
        #t_time = end - start
        #total_time = total_time + t_time

        # models.create_order(cust.customerid, chef.chefid, food.foodid, rd, comment)
        print "added:", order.orderid #, "| time:", t_time, "| total:", total_time, "| i:", i
    models.db.session.commit()
    end = time.time()
    t_time = end - start

    print t_time

main()