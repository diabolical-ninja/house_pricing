"""
Title: pdf_processing
Desc:  All functions required to extract auction result table from Domain PDF
Author: Yassin Eltahir
Date: 2016-11-25
"""

import pandas as pd
from PyPDF2 import PdfFileReader
from tabula import read_pdf_table
from lib.logConf import *


initialize_logger(console=False)

# Coordinates for first page table
y1 = 224.4
x1 = 11
y2 = 770
x2 = 580
p1_coords = [y1, x1, y2, x2] 


# Coordinates for pages 2-n
y21 = 0
x21 = 11
y22 = 780
x22 = 590
p2n_coords = [y21, x21, y22, x22]



# All of the steps required to extract the data table from the PDF
# Takes the location of a pdf as in input & returns a dataframe with the extracted information
def pdf_process(pdf):
    
    logging.info(' Start pdf_process on {}'.format(pdf))
    
    try:
        # Determine City & Auction Date
        city, date = city_date(pdf)

        # Process pages 2-N
        p2n = process_p2n(pdf, p2n_coords)
                
        # Extract Columns to assign to Page 1
        if p2n is None:
            p2_columns = None
        else:
            p2_columns = p2n.columns
        
        # Process page 1
        p1 = process_p1(pdf, p1_coords, p2_columns)
        
        # Combine P1 & P2N and add city & date info
        out = p1.append(p2n).reset_index()
        out['city'] = city
        out['date'] = date

        # Update column names
        out = out.drop('index',1)
        out.columns=['suburb','address','building_type','price','result','agent','city','date']
        
        logging.info(' Finish pdf_process on {}'.format(pdf))

        return out

    except Exception as e:
        logging.exception(' Failed pdf_process on {}'.format(pdf))
        pass



# Determine city & auction date
def city_date(filename):
    """
    Takes PDF name of known structure & returns the city & auction date
    """
    name_parts=filename.split('/')[-1].split('_')
    return name_parts[1], name_parts[0]


# Process Pages 2 - N
def process_p2n(pdf, coordinates):
    """
    Takes PDF from Domain & extracts auction results from pages 2 onwards
    """

    # Determine number of pages
    with open(pdf, 'rb') as f:
        reader=PdfFileReader(f, 'rb')
        num_pages=reader.getNumPages()
    if num_pages != 1:
        # Extract from pages 2-(N-1)
        hold=read_pdf_table(pdf, pages=range(2, num_pages+1), area=coordinates)
        return hold[hold.ix[:, 0] != 'Suburb']



# Process Page 1, checking that no more than the 1st row is missed
def process_p1(pdf, coordinates, columns=None):
    """
    Takes PDF from domain & extracts auctions results from the first page
    """

    p1=read_pdf_table(pdf, pages=1, area=coordinates)
    
    if p1 is None:
        ncol=0
    else:
        ncol=p1.shape[1]


    # Check that y1 is not too high
    # If it is then move down 1 point
    while ncol != 6:

        coordinates[0]=coordinates[0] + 1
        p1=read_pdf_table(pdf, pages=1, area=coordinates)
        try:
            ncol=p1.shape[1]
        except:
            ncol=0


    # Check that y1 is not too low
    # If it is then move up in small steps
    while ncol == 6:
        coordinates[0]=coordinates[0] - 0.1
        p1=read_pdf_table(pdf, pages=1, area=coordinates)
        try:
            ncol=p1.shape[1]
        except:
            ncol=0

        # Indicates we've gone past the top of the table
        if ncol != 6:
            coordinates[0]=coordinates[0] + 0.1
            p1=read_pdf_table(pdf, pages=1, area=coordinates)


    # TO-DO: read first row of table. Currently skipping
    # The 2nd row is incorrectly read as the header. Make it a row
    tmp=pd.DataFrame([p1.columns.tolist()], columns=p1.columns.tolist())
    p1=p1.append(tmp)

    # If Column headers aren't provided assume their values
    if columns is None:
        p1.columns=['suburb','address','building_type','price','result','agent']
    else:
        p1.columns=columns

    return p1

