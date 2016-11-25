"""
Title: pdf_processing
Desc:  All functions required to extract auction result table from Domain PDF
Author: Yassin Eltahir
Date: 2016-11-25
"""


# Dummy file for testing
test_file = '/Users/yassineltahir/Google Drive/Data Science/Real Estate Analysis/20160213_melbourne_auction_results.pdf'


import pdf_processing
import extract_processing


def main():
    
    # 1. Extract Table from PDF
    out = pdf_processing.pdf_process(test_file)

    # 2. Clean up Columns
    clean = extract_processing.extract_clean(out)


if __name__ == "__main__":
    main()