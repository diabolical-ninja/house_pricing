"""
Title: extract_cleaning
Desc:  Formats extracted table data, creating new columns & removing unwanted symbols
            - Removes '$' & ',' from Price data
            - Separate Type into number of bedrooms & proprety type
            - Identifies Agents that contained a line break & stitches the 2 rows back together
Author: Yassin Eltahir
Date: 2016-11-25
"""

import pandas as pd
from lib.logConf import *


initialize_logger(console=False)


# Will perform all the cleaning tasks
def extract_clean(df):
    
    logging.info(' Start extract_clean')

    try:

        # Price: Remove special characters & convert to float
        df['price'] = pd.to_numeric(df.price.str.strip('$').str.replace(',',''), errors='coerce')
    
        # Type: Extract number of bedrooms & property type
        tmp = getBuildType(df)
        df = pd.concat([df,tmp], axis=1)

        # Clean up agent names which contained linebreaks
        df = agent_breaks(df)

        logging.info(' Finish extract_clean')

        return df

    except Exception as e:
        logging.exception(' Failed extract_clean')
        pass
        



def agent_breaks(df):
    """
    Finds instances where an agent name has contained a line break
    When found, the name is concatenated to the agent name on the above row
    Outputs a dataframe with the additional rows caused by line breaks removed
    """

    # Identify Instances of line breaks occuring in the agent name
    # Occurs when agent IS NOT NULL & Suburb/Price ARE NULL
    brk_rows = df[df.suburb.isnull() & df.price.isnull() & df.agent.notnull()]

    # For each instance concatenate agent to previous agent
    # Work in reverse order to handle cases with multiple breaks
    for i in reversed(brk_rows.index):
        new_agent = "{} {}".format(df.agent[(i-1)], df.agent[i])
        df.set_value((i-1),'agent',new_agent)

    # Remove rows identified & exit
    return df.drop(brk_rows.index)





def getBuildType(df):
    '''
    Processes the buidling type string into:
        Bedroom count (NA, 0.....N)
        Building Type (studio, house, etc)
    '''
    tmp = df['building_type'].str.split(' ',expand=True).ix[:,[0,2]]
    tmp.columns = ['num_beds','prop_type']
    
    # Some buildings are listed as:
    #   - 'studio' or 'h' only. Fix those up.
    tmp.loc[tmp['num_beds']=='h',['num_beds','prop_type']] = [None,'h']
    tmp.loc[tmp['num_beds']=='u',['num_beds','prop_type']] = [None,'u']
    tmp.loc[tmp['num_beds']=='t',['num_beds','prop_type']] = [None,'t']
    tmp.loc[tmp['num_beds']=='studio',['num_beds','prop_type']] = [0,'studio']
    
    return tmp
    