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

# AZ_DICT = ['S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def main():
    for letter in AZ_DICT:
        c_url = BASEURL + letter + "/"
        # print c_url

        # get html data of the url
        resp = urllib2.urlopen(c_url)
        html = resp.read()

        # parse html data with bs
        soup = BeautifulSoup(html)
        soup.prettify()

        # find number of names pages
        pages_text = soup.find("tr", { "class" : "text" }).getText()
        total_names = int(pages_text.split()[5])
        # print total_names

        curr_page = 0
        
        while (curr_page < total_names):
            o_url = c_url + str(curr_page)
            # print o_url

            # get html data of the url
            resp = urllib2.urlopen(o_url)
            html = resp.read()

            # parse html data with bs
            soup = BeautifulSoup(html)
            soup.prettify()

            # get names
            names = soup.findAll("div", { "style": "padding-bottom:6px;" })
            for name in names:
                href = name.contents
                chefdb_id = str(href[0]).split("/")[2]
                # print chefdb_id

                lfname = name.getText()
                lflist = lfname.split(", ")

                if (len(lflist) < 2):
                    fname = lflist[0]
                    lname = "<None>"
                else:
                    fname = lflist[1]
                    lname = lflist[0]

                print fname.encode('utf-8'), "|", lname.encode('utf-8'), "|",  chefdb_id

            # go to next page
            curr_page = curr_page + 100

main()

