import math
import random
import sys
import urllib2

from BeautifulSoup import BeautifulSoup
from os import listdir
from os.path import isfile, join, curdir
from collections import defaultdict

# url format is ".../a-z/<letter>/p/<page#>" where PAGE is 1, 2, etc
BASEURL = "http://www.foodnetwork.com/recipes/a-z/%s/p/%s"

LETTERS = ['123', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'XYZ']

def main():
    for letter in LETTERS:
        pagenum = 1
        total_pages = 1

        c_url = BASEURL % (letter.lower(), str(pagenum))
        # print c_url

        # get html data of the url
        resp = urllib2.urlopen(c_url)
        html = resp.read()

        # parse html data with bs
        soup = BeautifulSoup(html)
        soup.prettify()

        # find number of names pages
        if (pagenum == 1):
            pages = soup.findAll("li", { "class" : "o-Pagination__a-ListItem" })
            total_pages = int(pages[-2].find("a").contents[0])

        while (pagenum <= total_pages):
            o_url = BASEURL % (letter.lower(), str(pagenum))
            # print o_url

            # get html data of the url
            resp = urllib2.urlopen(o_url)
            html = resp.read()

            # parse html data with bs
            soup = BeautifulSoup(html)
            soup.prettify()

            # get recipe lists
            recipe_lists = soup.findAll("ul", { "class": "m-PromoList o-Capsule__m-PromoList" })

            for recipe_list in recipe_lists:
                # print recipe_list
                recipes = recipe_list.findAll("a")

                for recipe in recipes:
                    recipe_name = recipe.contents[0]
                    recipe_url  = recipe["href"]
                    recipe_id   = recipe_url.split("-")[-1]

                    print recipe_id, "|~|", recipe_name.encode('utf-8'), "|~|", recipe_url

            # go to next page
            pagenum = pagenum + 1

main()

