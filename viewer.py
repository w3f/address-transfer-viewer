import sys
import time

import json
import requests

import numpy as N


ADDRESS = ""
DEGREE = ""
API_KEY = ""
NUM_ITEMS_PER_PAGE = 25
MAX_PAGES = 10


def print_list(l):
    for item in l:
        print(item)

def print_transfers(in_list, out_list, order):
    print("INCOMING TRANSFERS (DEGREE " + str(order) + ")")
    print_list(N.unique(in_list))
    print("OUTGOING TRANSFERS (DEGREE " + str(order) + ")")
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

        if num_on_page == 0:
            break

        # print("Num on page = " + str(num_on_page))
    
        for j in range(0, num_on_page):

            # print("Starting " + str(j) + "...")
            # For each item on the page, get the Address

            from_addr = rj['data']['transfers'][j]['from']
            to_addr = rj['data']['transfers'][j]['to']
            
            if (to_addr == addr):
                in_list.append(from_addr)
            else:
                out_list.append(to_addr)


        # Clean up
        # Remove any duplicates
        in_list = N.unique(in_list).tolist()
        out_list = N.unique(out_list).tolist()
        # If same address is in list, remove it
        if addr in in_list:
            in_list.remove(addr)
        if addr in out_list:
            out_list.remove(addr)
            
    return in_list, out_list
        

# EXECUTION STARTS HERE

# All arguments are mandatory.

# Arguments:
# 1: API Key - Your subscan API key. See https://support.subscan.io/#introduction
# 2: Order - number of iterations (e.g. 1 = addresses that this address has transferred to, 2 = addresses that THOSE addresses have transferred to, etc.)
# 3: Address - address to examine


# Read in args from command line

ARGS_LEN = len(sys.argv)
if ARGS_LEN < 3:
    print("Usage: python viewer.py ADDRESS DEGREE API_KEY")
    print("API Key - Your subscan API key. See https://support.subscan.io/")
    print("DEGREE - Number of iterations to check against")
    print("ADDRESS - Polkadot address to examine")

    sys.exit(1)
else:
    API_KEY = sys.argv[1]
    DEGREE = int(sys.argv[2])
    ADDRESS = sys.argv[3]

# Get initial list (input and output)
in_list, out_list = get_transactions(ADDRESS)

print_transfers(in_list, out_list, 1)
print()

# If order > 0, start following only inputs on input path,
# only outputs on output path

for i in range(1, DEGREE):

    new_in_list = []
    new_out_list = []

    for addr in in_list:
        tr = get_transactions(addr)[0]
        new_in_list.extend(tr)

    for addr in out_list:
        tr = get_transactions(addr)[1]
        new_out_list.extend(tr)
        
    print_transfers(new_in_list, new_out_list, (i + 1))
    print()
    
    in_list = N.unique(new_in_list)
    out_list = N.unique(new_out_list)
    

