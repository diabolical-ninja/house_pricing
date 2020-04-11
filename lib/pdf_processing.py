"""
Title: pdf_processing
Desc:  All functions required to extract auction result table from Domain PDF
Author: Yassin Eltahir
Date: 2016-11-25
"""

import pandas as pd
from PyPDF2 import PdfFileReader
from tabula import read_pdf


# All of the steps required to extract the data table from the PDF
# Takes the location of a pdf as in input & returns a dataframe with the extracted information
def pdf_process(pdf):

    try:
        # Determine City & Auction Date
        city, date = city_date(pdf)

        # Extract results
        results_df = extract_results(pdf)

        # Add City & Date info in
        results_df['city'] = city
        results_df['date'] = date

        return results_df
        
    except Exception as e:
        print(e)

        return None


def extract_results(pdf):
    
    results = read_pdf(pdf, pages = 'all', pandas_options={'header': None})
    df = pd.concat(results, ignore_index=True)
    df.columns = ['suburb','address','building_type','price','result','agent']

    return df


# Determine city & auction date
def city_date(filename):
    """
    Takes PDF name of known structure & returns the city & auction date
    """
    name_parts=filename.split('/')[-1].split('_')
    return name_parts[1].lower(), name_parts[0]

