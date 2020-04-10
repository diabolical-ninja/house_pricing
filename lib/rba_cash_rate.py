"""
Title:  RBA Cash Rate
Desc:   Scrape Australian cash rate from RBA website
Author: Yassin Eltahir    
Date:   2017-04-01
"""

# Required Libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import datetime



def getCashHistory():
    """
    From inspecting the site, I can see that the data is stored like:
        <tr>
         <th>
          7 Mar 1990   <!--Date-->
         </th>
         <td>
          0.00         <!--Cash Rate Change-->
         </td>
         <td>
          16.50 to 17.00 <!--From & To Cash Rate-->
         </td>
        </tr>
    
    Will Search through tr then th & td to extract desired data
    """
    
    # Location of Cash Rates
    url = 'https://www.rba.gov.au/statistics/cash-rate/'
    
    # Read site contents & convert to tree
    content = urlopen(url).read()
    soup = BeautifulSoup(content, "lxml");
       
    
    # Find all instances of the 'tr' tag & iterate through
    # For each, look for 'th' & 'td' tags which contain:
    #   - Date
    #   - Percentage Points Changed
    #   - New Cash Rate
    sections = soup.find_all('tr')
    cash_rate = []
    # for sec in tqdm(sections):
    for sec in sections:
        if sec.find('tr'):
            continue
        else:
            
            tmp = sec.prettify()
            try:
                out = [
                        BeautifulSoup(tmp).find_all('th')[0].string.replace('\n ',''),  # Date
                        BeautifulSoup(tmp).find_all('td')[0].string.replace('\n ',''),  # Change
                        BeautifulSoup(tmp).find_all('td')[1].string.replace('\n ','')   # New Cash Rate
                        ]
                
                cash_rate.append(out)
            except:
                continue
    
    
    # Clean response for output
    cash_rate = pd.DataFrame(cash_rate)
    cash_rate.columns = ['date','change','cash_rate']
    cash_rate['date'] = pd.to_datetime(cash_rate['date'])
    
    # Some cash rates have string tags such as '\n' present. Remove them
    cash_rate['cash_rate'] = [x.replace('\t','').replace('\n','').replace('\r',' ') for x in cash_rate['cash_rate']]
    
    return pd.DataFrame(cash_rate)
            
            
            


def cashRateAtDate(history, date):
    '''
    Takes a dataframe of historical cash rates & identifies the one
    in existence at a given date
    '''
    
    # convert date format
    date = datetime.datetime.strptime(date, '%Y%m%d')
    
    # Want to find the most recent record (max) that hasn't surpassed the 
    # auction date. This is the max((historical dates - date) < 0).
    diff = history['date'] - date
    return history.iloc[diff[diff < datetime.timedelta(minutes=0)].idxmax()]
    
    
