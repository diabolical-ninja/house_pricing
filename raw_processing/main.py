"""
Title: main
Desc:  All functions required to extract auction result table from Domain PDF
Author: Yassin Eltahir
Date: 2016-11-25
"""

from lib.pdf_processing import pdf_process
from lib.extract_processing import extract_clean
from lib.logConf import *

# Logging Setting:
#   - Print to Project Root
#   - File titled error_raw_processing.log
#   - Output logs to console as well
initialize_logger(console=False)


# Dummy file for testing
# test_file = '/Users/yassineltahir/Google Drive/Data Science/Real Estate Analysis/20160213_melbourne_auction_results.pdf'
# test_file = '/Users/yassineltahir/Google Drive/Data Science/Real Estate Analysis/roar.pdf'
test_file = 'C:/Users/Yass/Google Drive/Data Science/Real Estate Analysis/20170204_Melbourne_auction_results.pdf'


def main():
    
    logging.info(' Begin Processing {}'.format(test_file))


    try:
        # 1. Extract Table from PDF
        out = pdf_process(test_file)

        # 2. Clean up Columns
        clean = extract_clean(out)

        # 3. Export Data
        clean.to_csv(path_or_buf='C:/Users/Yass/Downloads/test.csv',sep='|')

        logging.info(' Finished processing {}'.format(test_file))

    except Exception as e:
        logging.exception(' Failed processing {}'.format(test_file))
        


if __name__ == "__main__":
    main()