"""
Title: main
Desc:  All functions required to extract auction result table from Domain PDF
Author: Yassin Eltahir
Date: 2016-11-25
"""

from lib.pdf_processing import pdf_process
from lib.extract_processing import extract_clean
from lib.rba_cash_rate import *
from lib.logConf import *
from sqlalchemy import create_engine
import yaml
import os



# Source Config
conf = yaml.load(open('../conf.yaml','r'))

# Logging Setting:
#   - Print to Project Root
#   - File titled error_raw_processing.log
#   - Output logs to console as well
initialize_logger(console=False)


# # Connect to DB
dbName = conf['db']['dbname']
user = conf['db']['username']
pwrd = conf['db']['password']
host = conf['db']['server']
port = conf['db']['port']
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, pwrd, host, port, dbName))

# Dummy file for testing
#pdfFile = 'C:/Users/Yass/Google Drive/Data Science/Real Estate Analysis/20150530_melbourne_auction_results.pdf'
all_files = 'C:/Users/Yass/Google Drive/Data Science/Real Estate Analysis/'


def main(pdfFile):
    
    logging.info(' Begin Processing {}'.format(pdfFile))

    try:
        # 1. Extract Table from PDF
        out = pdf_process(pdfFile)
        
        # 2. Clean up Columns
        clean = extract_clean(out)
        
        # 3. Get Current Cash Rate
        cash_rates = getCashHistory()
        clean['cash_rate'] = cashRateAtDate(cash_rates,clean.date[0])['cash_rate']
        
        # 3. Attach Location Attributes Data
        # loc_attris = 

        # 4. Export Data
#        clean.to_csv(path_or_buf='C:/Users/Yass/Downloads/test.csv',sep='|', index = False)
        clean.to_sql('auction_results', con = engine, if_exists = 'append', schema ='real_estate', index = False)

        logging.info(' Finished processing {}'.format(pdfFile))

    except Exception as e:
        logging.exception(' Failed processing {}'.format(pdfFile))
        


if __name__ == "__main__":
    for file in os.listdir(all_files):
        if 'pdf' in file:
            main(all_files + file)