import math
import random
import sys
import urllib2

from BeautifulSoup import BeautifulSoup
from os import listdir
from os.path import isfile, join, curdir
from collections import defaultdict

# url format is ".../azot/<LETTER>/<PAGE>" where PAGE is 0, 100, 200, ..., <total_names>
BASEURL = "https://www.chefdb.com/nm/atoz/"
AZ_DICT = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def main():
    for letter in AZ_DICT:
        c_url = BASEURL + letter + "/"
        print c_url

        # get html data of the url
        resp = urllib2.urlopen(c_url)
        html = resp.read()

        # parse html data with bs
        soup = BeautifulSoup(html)
        soup.prettify()

        # find number of names pages
        pages_text = soup.find("tr", { "class" : "text" }).getText()
        total_names = int(pages_text.split()[5])
        print total_names

        curr_page = int(0)
        
        while (curr_page < total_names):
            c_url = c_url + str(curr_page)
            print c_url

            # get html data of the url
            resp = urllib2.urlopen(c_url)
            html = resp.read()

            # parse html data with bs
            soup = BeautifulSoup(html)
            soup.prettify()

            # get names
            names = soup.findAll("div", { "style": "padding-bottom:6px;" })
            for name in names:
                lfname = name.getText()
                lflist = lfname.split(", ")
                fname = lflist[1]
                lname = lflist[0]

                print fname, lname

            # go to next page
            curr_page = int(curr_page) + 100

main()

