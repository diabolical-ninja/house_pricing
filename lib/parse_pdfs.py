"""
Title:  Parse PDF's
Desc:   Executes all the cleaning processed on the PDF's
Author: Yassin Eltahir    
Date:   2018-07-08
"""


from lib.pdf_processing import pdf_process
from lib.extract_processing import extract_clean
from lib.rba_cash_rate import *


def parse_pdfs(pdf: str):
    """Executes all the cleaning processed on the PDF's
    
    Args:
        pdf (str): Path of the pdf to clean
    
    Returns:
        pandas.core.frame.DataFrame: Dataframe of the extracted & cleaned data
    """

    # 1. Extract Table from PDF
    out = pdf_process(pdf)

    if out is not None:
    
        # 2. Clean up Columns
        clean = extract_clean(out)

        # 3. Get Current Cash Rate
        cash_rates = getCashHistory()
        clean['cash_rate'] = cashRateAtDate(cash_rates,clean.date[0])['cash_rate']

        return clean

    else:
        return None