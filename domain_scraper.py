"""
Title:  Domain Catcher
Desc:   Executes everything
"""

import yaml
import csv
import os
import logging
from datetime import datetime
from sqlalchemy import create_engine
from lib.auction_results import AuctionResults
from lib.rba_cash_rate import getCashHistory, cashRateAtDate
from lib.auction_results_download import result_download


# Configure logging
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level = logging.DEBUG,
                    format = LOG_FORMAT,
                    handlers=[
                        logging.FileHandler("domain_scraper_status.log"),
                        logging.StreamHandler()]
                    )


# Read in Configuration
conf = yaml.safe_load(open('conf.yaml', 'r'))


# Connect to DB
dbName = conf['db']['dbname']
user = conf['db']['username']
pwrd = conf['db']['password']
host = conf['db']['server']
port = conf['db']['port']
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, pwrd, host, port, dbName))


# Instantiate Auction Result Object
ac = AuctionResults(conf['domain'])


# 1. Download all results

# Fn Inputs
city_list = ['Sydney', 'Adelaide', 'Canberra', 'Brisbane', 'Melbourne']
domain_url = "https://auction-results.domain.com.au/Proofed/PDF"
unprocessed_dir = "{}/unprocessed".format(conf['directory'])

# Get Current Cash Rate History
cash_rates = getCashHistory()

# Run for all cities
for city in city_list:

    try:
        # Download PDF of Results
        result_download(url=domain_url, city=city, out_dir=unprocessed_dir)
        logging.info(f"Downloaded PDF for {city}")

        # Download Auction Results Data
        results_df = ac.get_city_results(city)

        # Append Cash Rate
        results_df['cash_rate'] = cashRateAtDate(cash_rates, results_df.date[0])['cash_rate']

        # Upload to DB
        results_df.to_sql('auction_results',
                          con = engine,
                          if_exists = 'append',
                          schema ='real_estate',
                          index = False)
        logging.info(f"Saved results in DB for {city}")

    except Exception as ex:
        print(ex)
        logging.error(ex)
