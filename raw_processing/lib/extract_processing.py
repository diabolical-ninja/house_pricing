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
        df['Price'] = df.Price.str.strip('$').str.replace(',','').astype(float)
    
        # Type: Extract number of bedrooms & property type
        tmp = df['Type'].str.split(' ',expand=True).ix[:,[0,2]]
        tmp.columns = ['num_beds','prop_type']
        df = pd.concat([df,tmp], axis=1)

        # Clean up agent names which contained linebreaks
        df = agent_breaks(df)

        logging.info(' Finish extract_clean')

        return df

    except Exception as e:
        logging.exception(' Failed extract_clean')
        quit()



def agent_breaks(df):
    """
    Finds instances where an agent name has contained a line break
    When found, the name is concatenated to the agent name on the above row
    Outputs a dataframe with the additional rows caused by line breaks removed
    """

    # Identify Instances of line breaks occuring in the agent name
    # Occurs when agent IS NOT NULL & Suburb/Price ARE NULL
    brk_rows = df[df.Suburb.isnull() & df.Price.isnull() & df.Agent.notnull()]

    # For each instance concatenate agent to previous agent
    # Work in reverse order to handle cases with multiple breaks
    for i in reversed(brk_rows.index):
        new_agent = "{} {}".format(df.Agent[(i-1)], df.Agent[i])
        df.set_value((i-1),'Agent',new_agent)

    # Remove rows identified & exit
    return df.drop(brk_rows.index)