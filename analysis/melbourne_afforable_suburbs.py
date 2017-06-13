"""
Title:  melbourne_afforable_suburbs.py
Desc:   Identify Suburbs in Melbourne with prices between $350-450k
            - Property Type = House
            - CBD Distance pref = <20km
Author: Yassin Eltahir
Date:   2017-06-05
"""


# Required Libraries
import pandas as pd
import numpy as np
import googlemaps
from sqlalchemy import create_engine
import yaml
from tqdm import tqdm


# Source Config
conf = yaml.load(open('../conf.yaml','r'))
google_key = conf['google']['key']


# # Connect to DB
dbName = conf['db']['dbname']
user = conf['db']['username']
pwrd = conf['db']['password']
host = conf['db']['server']
port = conf['db']['port']
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, pwrd, host, port, dbName))



# Source Data
qry_str = """

    SELECT suburb, price, date
    FROM real_estate.auction_results
    WHERE city = 'melbourne'
      and prop_type in ('h','t')
      and num_beds >= 2
      and result in ('S','SP','SA')

"""
df = pd.read_sql(qry_str, con = engine)



# Calculate Mean, Median & Number of Sales by Suburb
sale_agg = df.groupby(['suburb'])['price'].agg({'median_price':np.median, 'mean_price':np.mean, 'num_sales':len})
sale_agg.reset_index(level=0, inplace=True)

## Get distance from CBD for each suburb

gmaps = googlemaps.Client(key=google_key, timeout = None)


# Build list of all suburbs with Vic appended to them
suburbs = sale_agg.index.tolist()
suburbs = [x + ', Vic' for x in suburbs]

# Get distance from Fed square for each suburb
dmat = gmaps.distance_matrix(origins = 'Federation Square, Swanston St, Melbourne VIC'
                        , destinations = suburbs
                        , mode = 'driving'
                        , units = 'metric'
                        )


dist_list = []
dura_list = []
new_sub = []

for sub in tqdm(suburbs):
    
#    print sub
    dmat = gmaps.distance_matrix(origins = 'Federation Square, Swanston St, Melbourne VIC'
                        , destinations = sub
                        , mode = 'driving'
                        , units = 'metric'
                        )
    
    if dmat['status']:
        dist_list.append(dmat['rows'][0]['elements'][0]['distance']['text'])
        dura_list.append(dmat['rows'][0]['elements'][0]['duration']['text'])
        new_sub.append(dmat['destination_addresses'][0])
    else:
        dist_list.append(None)
        dura_list.append(None)
        new_sub.append(None)
    
    

sale_agg['distance'] = dist_list
sale_agg['duration'] = dura_list
sale_agg['suburb'] = new_sub


# Get Suburbs between $350-450k
subset = sale_agg[(sale_agg.median_price >= 350000) & (sale_agg.median_price <= 500000)]


# Export Results to CSV
sale_agg.to_csv(path_or_buf='C:/Users/Yass/Downloads/melbourne_historical_suburb_prices.csv',sep='|', index = False)

