import sys
import time

import json
import requests

import numpy as N


ADDRESS = ""
ORDER = ""
API_KEY = ""
NUM_ITEMS_PER_PAGE = 25
MAX_PAGES = 10


def print_list(l):
    for item in l:
        print(item)

def print_transfers(in_list, out_list, order):
    print("INCOMING TRANSFERS (ORDER " + str(order) + ")")
    print_list(N.unique(in_list))
    print("OUTGOING TRANSFERS (ORDER " + str(order) + ")")
    print_list(N.unique(out_list))

        
# Returns a tuple - first element is incoming transfers, 2nd is outgoing
def get_transactions(addr):

    # Subscan API endpoint
    URL = 'https://polkadot.api.subscan.io/api/scan/transfers'

    # Headers needed for receiving content
    HEADERS = {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
    }
    
    in_list = []
    out_list = []
    
    for j in range(0, MAX_PAGES):

        json_data = {
            'row': NUM_ITEMS_PER_PAGE,
            'page': j,
            'address': addr
        }
        r = requests.post(URL, headers=HEADERS, json=json_data)
        rj = json.loads(r.text)

        if rj is None:
            break

        if rj['data']['transfers'] is None:
            break
    
        num_on_page = len(rj['data']['transfers'])

        if  num_on_page == 0:
            break

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
    return N.unique(in_list), N.unique(out_list)
        

# EXECUTION STARTS HERE

# All arguments are mandatory.

# Arguments:
# 1: Address - address to examine
# 2: Order - number of iterations (e.g. 1 = addresses that this address has transferred to, 2 = addresses that THOSE addresses have transferred to, etc.)
# 3: API Key - Your subscan API key. See https://support.subscan.io/#introduction


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


# Get initial list (input and output)
in_list, out_list = get_transactions(ADDRESS)

print_transfers(in_list, out_list, 1)

# If order > 0, start following only inputs on input path,
# only outputs on output path

for i in range(1, ORDER):

    new_in_list = []
    new_out_list = []
    
    for addr in in_list:
        new_in_list.extend(get_transactions(addr)[0])
        
    for addr in out_list:
        new_out_list.extend(get_transactions(addr)[1])
        
    print_transfers(new_in_list, new_out_list, (i + 1))
    
    in_list = N.unique(new_in_list)
    out_list = N.unique(new_out_list)
    

