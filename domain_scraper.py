"""
Title:  Domain Catcher
Desc:   Executes everything
Author: Yassin Eltahir
Date:   2018-07-08
"""

import yaml
import csv
import os
from datetime import datetime
from sqlalchemy import create_engine
from lib.auction_results_download import result_download
from lib.parse_pdfs import parse_pdfs

conf = yaml.load(open('conf.yaml','r'))


# Connect to DB
dbName = conf['db']['dbname']
user = conf['db']['username']
pwrd = conf['db']['password']
host = conf['db']['server']
port = conf['db']['port']
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, pwrd, host, port, dbName))



# 1. Download all results

# Fn Inputs
city_list = ['Sydney','Adelaide','Canberra','Brisbane','Melbourne']
domain_url = "https://auction-results.domain.com.au/Proofed/PDF"
unprocessed_dir = "{}/unprocessed".format(conf['directory'])


# Run for all cities
for city in city_list:

    result_download(url=domain_url, city=city, out_dir=unprocessed_dir)
    print("{}: Downloaded {} Auction Results".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), city))



# 2. Extract Results
unprocessed_dir = "{}/unprocessed".format(conf['directory'])
for pdf_file in os.listdir(unprocessed_dir):
    
    # Ignore hidden files
    if not pdf_file.startswith('.'): 
        
        # Extract data
        unprocessed_pdf = "{}/{}".format(unprocessed_dir,pdf_file)
        parsed_df = parse_pdfs(unprocessed_pdf)

        # Dump to disk
        parsed_df.to_csv("{}/testing.csv".format(conf['directory']),
               sep = "|",
               index = False,
               quoting = csv.QUOTE_ALL,
               encoding='utf-8',
               mode = 'a'
               )

        # Upload to DB
        parsed_df.to_sql('auction_results', con = engine, if_exists = 'append', schema ='real_estate', index = False)


        # Move the PDF to processed
        os.rename(unprocessed_pdf, "{}/processed/{}".format(conf['directory'], pdf_file))

        print("{}: Parsed {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pdf_file))


