#***************************************************************
# Title: Bulk Auction Results Processing
# Desc:  Take all historical results & extract relevant data
#        Includes: City, Date, Price, Basic property info, address
# Author: Yassin Eltahir
# Date: 2016-11-10
#***************************************************************


import os
import pandas as pd
from PyPDF2 import PdfFileReader
from tabula import read_pdf




#pdf_dir = '/Users/yassineltahir/Google Drive/Data Science/Real Estate Analysis'
pdf_dir = 'C:/Users/Yassin/Google Drive/Data Science/Real Estate Analysis'
all_files = ['{0}/{1}'.format(pdf_dir, x) for x in os.listdir(pdf_dir)]
#test_file = 'C:/Users/Yassin/Google Drive/Data Science/Real Estate Analysis/20160213_melbourne_auction_results.pdf'

out_dir = 'C:/Users/Yassin/Google Drive/Data Science/Real Estate Analysis/processing_output'


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
x22 = 580

p2n_coords = [y21, x21, y22, x22]



# Variable (list) to capture failed files
failed = []


def main(pdf):

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
    
        print "Processed {}".format(pdf)
        
        return out
        
    except:
        print "Failed {}".format(pdf)
        failed.append(pdf)
        pass
    
    

# Determine city & auction date
def city_date(filename):
    
    """
    Takes PDF name of known structure & returns the city & auction date
    """
    
    name_parts = filename.split('/')[-1].split('_')
    return name_parts[1], name_parts[0]


# Process Pages 2 - N
def process_p2n(pdf, coordinates):
    
    # Determine number of pages
    with open(pdf,'rb') as f:
        reader = PdfFileReader(f,'rb')
        num_pages = reader.getNumPages() 
    
    if num_pages != 1:    
        # Extract from pages 2-(N-1)
        hold = read_pdf(pdf, pages = range(2,num_pages+1), area = coordinates)
        return  hold[hold.ix[:,0]!='Suburb']

    
    
# Process Page 1, checking that no more than the 1st row is missed
def process_p1(pdf, coordinates, columns=None):

    p1 = read_pdf(pdf, pages = 1, area = coordinates)
    
    if p1 is None:
        ncol = 0
    else:
        ncol = p1.shape[1]


    # Check that y1 is not too high
    # If it is then move down 1 point
    while ncol != 6:

        coordinates[0] = coordinates[0] + 1
        p1 = read_pdf(pdf, pages = 1, area = coordinates)
        try:
            ncol = p1.shape[1]
        except:
            ncol = 0


    # Check that y1 is not too low
    # If it is then move up in small steps
    while ncol == 6:
        
        coordinates[0] = coordinates[0] - 0.1
        p1 = read_pdf(pdf, pages = 1, area = coordinates)
        try:
            ncol = p1.shape[1]
        except:
            ncol = 0

        # Indicates we've gone past the top of the table
        if ncol != 6:
            coordinates[0] = coordinates[0] + 0.1
            p1 = read_pdf(pdf, pages = 1, area = coordinates)
        
        
    # TO-DO: read first row of table. Currently skipping
    # The 2nd row is incorrectly read as the header. Make it a row
    tmp = pd.DataFrame([p1.columns.tolist()], columns = p1.columns.tolist())
    p1 = p1.append(tmp)
    
    # If Column headers aren't provided assume their values
    if columns is None:
        p1.columns = ['Suburb','Address','Type','Price','Result','Agent']
    else:
        p1.columns = columns
    
    return p1
 

    


if __name__ == "__main__":
   out_all = map(main, all_files)

   
   

   
    
# Create single DF out of all files    
out_all = [x for x in out_all if isinstance(x,pd.DataFrame)]
df = pd.concat(out_all)

# Write output
df.to_csv("{}/historical_auction_results.csv".format(out_dir), sep='|',
          index=False, 
          header = True)


# Write Fails to Disk
out_fails = open("{}/failed.txt".format(out_dir), 'w')
for item in failed:
    out_fails.write(item+'\n')
out_fails.close()    

