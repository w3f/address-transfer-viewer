import sys
import time

import json
import requests

import numpy as N

def print_list(l):
    for item in l:
        print(item)


# EXECUTION STARTS HERE

# All arguments are mandatory.

# Arguments:
# 1: Address - address to examine
# 2: Order - number of iterations (e.g. 1 = addresses that this address has transferred to, 2 = addresses that THOSE addresses have transferred to, etc.)
# 3: API Key - Your subscan API key. See https://support.subscan.io/#introduction

ADDRESS = ""
ORDER = ""
API_KEY = ""
NUM_ITEMS_PER_PAGE = 25
MAX_PAGES = 100
INDICATOR_LENGTH = 0

# Read in args from command line

ARGS_LEN = len(sys.argv)
if ARGS_LEN < 3:
    print("Usage: python viewer.py ADDRESS ORDER API_KEY")
    print("ADDRESS - Polkadot address to examine")
    print("ORDER - Number of iterations to check against")
    print("API Key - Your subscan API key. See https://support.subscan.io/")
    sys.exit(1)
else:
    ADDRESS = sys.argv[1]
    ORDER = int(sys.argv[2])
    API_KEY = sys.argv[3]

# Subscan API endpoint
URL = 'https://polkadot.api.subscan.io/api/scan/transfers'

# Headers needed for receiving content
HEADERS = {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
}


for j in range(0, 1):
    # for j in range(0, MAX_PAGES):
    # Get data from one page of Subscan results, searching for System.remark_with_event
    # extrinsics. The request is then converted to JSON (rj variable).

    # Right now an invalid request from Subscan will make this die, would be nice to
    # add something which fixes that.

    json_data = {
        'row': NUM_ITEMS_PER_PAGE,
        'page': j,
        'address': ADDRESS
    }
    r = requests.post(URL, headers=HEADERS, json=json_data)
    rj = json.loads(r.text)

    in_list = []
    out_list = []

    num_on_page = len(rj['data']['transfers'])

    # print("Num on page = " + str(num_on_page))
    
    for j in range(0, num_on_page):

        # print("Starting " + str(j) + "...")
        # For each item on the page, get the Address

        from_addr = rj['data']['transfers'][j]['from']
        to_addr = rj['data']['transfers'][j]['to']
        
        if (to_addr == ADDRESS):
            in_list.append(from_addr)
        else:
            out_list.append(to_addr)
        line = rj['data']['transfers'][j]['to']

        # raw_vote = (rj2[0]['value'])
        # addr = rj['data']['extrinsics'][j]['account_display']['address']
        # extr = rj['data']['extrinsics'][j]['extrinsic_index']

    print("INCOMING TRANSFERS")
    print_list(N.unique(in_list))
    print("OUTGOING TRANSFERS")
    print_list(N.unique(out_list))


        # This sleeps for 400 ms, to ensure that we don't overwhelm our free tier of
        # API services from Subscan
    time.sleep(0.4)

