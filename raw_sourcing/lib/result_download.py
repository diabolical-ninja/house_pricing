"""
Title: result_download.py
Desc:  Downloads auction results on demand
Author: Yassin Eltahir
Date: 2016-11-28
"""

import urllib
import time


# # Example Inputs
# url = "https://auction-results.domain.com.au/Proofed/PDF"
# city = 'Adelaide'
# out_dir = ''


def result_download(url, city, out_dir, append=True):
    
    # Build download string
    # Using the current address structure, but this is subject to change
    # Allows for other, less generic, strings to be used instead 
    if append is True:
        down_url = "{}/{}_Domain.pdf".format(url, city) 
    else:
        down_url = url

    
    # Build Output Location Name
    date = time.strftime("%Y%m%d")
    loc_name = "{}/{}_{}_auction_results.pdf".format(out_dir, date, city)

    # Source Auction Results & Save to appropriate directory
    urllib.urlretrieve(down_url, loc_name)   

    

