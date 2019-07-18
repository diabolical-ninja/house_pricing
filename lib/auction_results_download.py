"""
Title:  Auction Results Download
Desc:   Downloads auction results on demand
Author: Yassin Eltahir
Date:   2016-11-28
"""

import requests
import time
import yaml
import os


# # Example Inputs
# url = "https://auction-results.domain.com.au/Proofed/PDF"
# city = 'Adelaide'
# out_dir = ''


def result_download(url: str, city: str, out_dir: str):
    """Downloads the Auction Results PDF's
    
    Args:
        url (str): Domain PDF base URL
        city (str): Autralian city name. Options are Melbourne, Sydney, Adelaide, Perth, Canberra
        out_dir (str): Where to save the PDF
    """

    # Build Required Vars
    date = time.strftime("%Y%m%d")
    output_name = "{}/{}_{}_auction_results.pdf".format(out_dir, date, city)
    full_url = "{}/{}_Domain.pdf".format(url, city)
    
    # Source Auction Results & Save to appropriate directory
    file = requests.get(full_url, stream=True, verify=False)

    # Save PDF to disk
    os.makedirs(os.path.dirname(output_name), exist_ok=True)
    with open(output_name, 'wb') as f:
        f.write(file.content)