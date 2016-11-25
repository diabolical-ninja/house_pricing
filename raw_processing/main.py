"""
Title: main
Desc:  All functions required to extract auction result table from Domain PDF
Author: Yassin Eltahir
Date: 2016-11-25
"""


# Dummy file for testing
test_file = '/Users/yassineltahir/Google Drive/Data Science/Real Estate Analysis/20160213_melbourne_auction_results.pdf'


from lib.pdf_processing import pdf_process
from lib.extract_processing import extract_clean

failed=[]

def main():

    # 1. Extract Table from PDF
    out = pdf_process(test_file)

    # 2. Clean up Columns
    clean = extract_clean(out)


if __name__ == "__main__":
    main()