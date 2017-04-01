"""
Title:  RBA Cash Rate
Desc:   Scrape Australian cash rate from RBA website
Author: Yassin Eltahir    
Date:   2017-04-01
"""

# Required Libraries
from bs4 import BeautifulSoup
import urllib2
import pandas as pd
from tqdm import tqdm



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
    url = 'http://www.rba.gov.au/statistics/cash-rate/'
    
    # Read site contents & convert to tree
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")
       
    
    # Find all instances of the 'tr' tag & iterate through
    # For each, look for 'th' & 'td' tags which contain:
    #   - Date
    #   - Percentage Points Changed
    #   - New Cash Rate
    sections = soup.find_all('tr')
    cash_rate = []
    for sec in tqdm(sections):
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
            
            
            
out = getCashHistory()  
