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
import re



# Will perform all the cleaning tasks
def extract_clean(df):
    
    try:

        # Remove dirty rows such as misplaced headers, etc
        dirty_rows_indicies = identify_dirty_rows(df)
        df = df.drop(dirty_rows_indicies)

        # Clean Misaligned Columns
        df = clean_misaligned_columns(df)

        # Clean up agent names which contained linebreaks
        df = agent_breaks(df)

        # Remove incomplete rows
        incomplete_row_indicies = incomplete_rows(df)
        df = df.drop(incomplete_row_indicies)

        # Price: Remove special characters & convert to float
        df['price'] = pd.to_numeric(df.price.str.strip('$').str.replace(',',''), errors='coerce')
    
        # Type: Extract number of bedrooms & property type
        tmp = getBuildType(df)
        df = pd.concat([df,tmp], axis=1)

        df.reset_index(inplace=True, drop=True)

        return df

    except Exception as e:
        print(e)
        pass
        

def identify_dirty_rows(df):
    # Some rows are dirty values from the extraction that need to be purged
    unwanted_rows = df[(df.suburb.str.contains('Median:', na=False)) | 
                        (df.suburb.str.contains('Suburb Address', na=False)) | 
                        (df.suburb.str.contains("Saturday's Auctions", na=False))].index


    unwanted_header_rows = df[(df.suburb == 'Suburb') & (df.address == 'Address')].index
    unwanted_rows = unwanted_rows.append(unwanted_header_rows)

    return unwanted_rows


def clean_misaligned_columns(df):
    # Fix up misaligned columns
    misaligned_col_index = df[(df.building_type.str.contains("$", regex=False, na=False)) | 
                                (df.building_type.str.contains("N/A", regex=False, na=False)) ].index

    misaligned_clean = df.loc[misaligned_col_index].apply(lambda x: clean_bad_row(x), axis = 1)
    misaligned_clean_df = pd.DataFrame(misaligned_clean.tolist())

    # Drop Unwanted rows
    df = pd.concat([df.drop(misaligned_col_index), misaligned_clean_df], ignore_index=True)

    return df


def incomplete_rows(df):
    """
    Remove Rows that are missing crucial information
    """

    unwanted_rows = df[df.suburb.isnull() & df.address.isnull()].index
    return unwanted_rows


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
    # Don't try to fix first row issues. They'll just be removed.
    for i in reversed(brk_rows.index):
        if i != 0:
            new_agent = "{} {}".format(df.agent[(i-1)], df.agent[i])
            df.at[(i-1), 'agent'] = new_agent

    # Remove rows identified, reset index & exit
    return df.drop(brk_rows.index).reset_index().drop('index',1)





def getBuildType(df):
    '''
    Processes the buidling type string into:
        Bedroom count (NA, 0.....N)
        Building Type (studio, house, etc)
    '''
    tmp = df['building_type'].str.split(' ',expand=True).iloc[:,[0,2]]
    tmp.columns = ['num_beds','prop_type']
    
    # Some buildings are listed as:
    #   - 'studio' or 'h' only. Fix those up.
    tmp.loc[tmp['num_beds']=='h',['num_beds','prop_type']] = [None,'h']
    tmp.loc[tmp['num_beds']=='u',['num_beds','prop_type']] = [None,'u']
    tmp.loc[tmp['num_beds']=='t',['num_beds','prop_type']] = [None,'t']
    tmp.loc[tmp['num_beds']=='studio',['num_beds','prop_type']] = [0,'studio']
    
    return tmp
    
def separate_suburb_address(combined_suburb_address):
    """Separate Suburb & Address when in a single string
    
    Args:
        combined_suburb_address (str): Combined suburb & string
    """

    split_val = re.search('\d+', combined_suburb_address).group()
    address_splits = re.split(split_val, combined_suburb_address)
    
    if len(address_splits) == 2:
        address_splits[-1] = f"{split_val}{address_splits[-1]}"
        address_splits = [x.strip() for x in address_splits]
        
        return address_splits[0], address_splits[1]
    else:
        return None, None


def extract_price(string):
    """Extract Price from string

    Format supported: $X,XXX,XXX
                      $XXXX
                      $XX,XXX
    
    Args:
        bad_string (str): String containing dollar amount to extract
    """

    price_pattern = re.compile(r'\$(\d[0-9,.]+)|N/A')
    price = re.search(price_pattern, string).group()
    string_no_price = string.replace(price, '')

    return string_no_price.strip(), price.strip()


def extract_result_type(string):
    """Extract property sale result type from string
    
    Args:
        string (string): String containing result type
    """

    results_types = ["SS","VB","SN","SA","PN","RW","SP","PI","S","W"]
    results_cache = []

    for result in results_types:
        result_search = f"{result} "
        if result_search in string:
            results_cache.append(result)
            string = string.replace(result_search, '')

    results_cache = ' '.join(results_cache)

    return string.strip(), results_cache.strip()


def split_bad_building_string(string):
    """Split string containing price, result type & agent
    
    Args:
        string (str): string to clean

    Returns:
        - price
        - result type
        - agent
    """

    # Extract Price
    clean_string, price = extract_price(string)

    # Extract Result Type
    clean_string, result_type = extract_result_type(clean_string)

    return price, result_type, clean_string


def clean_bad_row(row_info):
    """Clean misalign & badly formatted row
    
    Args:
        row_info (dict): Full row info
    """

    # Split suburb & address
    suburb, address = separate_suburb_address(row_info['suburb'])

    # Reassign building type
    building_type = row_info['address']

    # Extract price, result & agent
    price, result, agent = split_bad_building_string(row_info['building_type'])

    return {
        'suburb': suburb,
        'address': address,
        'building_type': building_type,
        'price': price,
        'result': result,
        'agent': agent,
        'city': row_info['city'],
        'date': row_info['date']
    }

