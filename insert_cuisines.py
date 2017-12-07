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
    # randomly generate cuisines
    for i in range(1, 100):
        cname = "Cuisine Type " + str(i)
        print "inserting", cname

        cuisine = models.Cuisine(cname)
        models.db.session.add(cuisine)
        models.db.session.commit()
        print "done"

    # populate mappings
    chefs = models.get_all_chefs()
    cuisines = models.get_all_cuisines()
    fooditems = models.get_all_fooditems()
    
    # insert chef-cuisine mapping first (chef special)
    for chef in chefs:
        randcuisine = random.choice(cuisines)
        print chef.chefid, randcuisine

        chefspec = models.ChefSpecial(chef.chefid, randcuisine.cuisineid)
        models.db.session.add(chefspec)
    models.db.session.commit()
    print "commited chef-cuisine"    

    # insert fooditem-cuisine mapping (cuisine item)
    for fooditem in fooditems:
        randcuisine = random.choice(cuisines)
        print fooditem.foodid, randcuisine

        cuisineitem = models.CuisineItem(fooditem.foodid, randcuisine.cuisineid)
        models.db.session.add(cuisineitem)
    models.db.session.commit()
    print "commited fooditem-cuisine"

main()
