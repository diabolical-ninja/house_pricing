"""
Title: google_data
Desc:  Takes the extracted data and finds the following:
            - Travel Time to N nearest supermarkets by Car, PT & Walking
            - Travel Time to N nearest schools (primary & secondary) by Car, PT & Walking
            - Travel time to the CBD by Car and Public Transport
            - .....
        Assumes 9am arrival time. This is to counter distance vs convenience
Author: Yassin Eltahir
Date: 2017-02-07
"""

import pandas as pd
from lib.logConf import *

initialize_logger(console=False)


def google_data(df):

    # Initialise Connection Object
    google_key = 'AIzaSyCz99k0qrmN3qc7kL2gI_hViJWOtnm5wnE'  # This HAS to be removed!!
    gmaps = googlemaps.Client(key=google_key)

    # Apply function on Address & Suburb
    
    





    
def nearest_feature(address, feature, num_sm, sm_pref, con):
    """
    Calcualtes travel time & distance (Car, PT, Walking) for the N nearest features 
    Input:
        df = Dataframe containing an address column used for searching
        feature = What to search for; supermarket, high-school etc
        num_sm = Closest N to return
        sm_pref = Closeness measure: distance or travel duration
        con = Initialised Google maps connection object
    Output:
        df = Dataframe containing location name, coordinates, distance, duration & transit mode
    """

    # Get Address Coordinates
    address_coords = con.geocode(address)[0]['geometry']['location']
    
    # Find all places within radius of POI
    places_out = gmaps.places(query = feature
                                , radius = 2000   # Search within 2km. Might change later
                                , location = address_coords)
    
    
    # Extract Feature Name & Coordinates
    nearby = [[x['name'],x['geometry']['location']] for x in places_out['results']]
    nearby_coords = [x[1] for x in nearby]
    
    # For each place, calculate the travel time
    transport_methods = ['driving','transit','walking']
    
    travel_times = []
    for mode in transport_methods:
        
        # Get distance to all locations      
        dmat = gmaps.distance_matrix(origins = address_coords
                        , destinations = nearby_coords
                        , mode = mode
                        , units = 'metric')
        
        # Extract distance & travel time
        tmp = [[x['distance']['value'],x['duration']['value']] for x in dmat['rows'][0]['elements']]

        # Join Back with Nearby Destinations & add in tranit mode
        tmp = zip(nearby, tmp)
        out = [x[0]+x[1]+[mode] for x in tmp]
        
        # Capture
        travel_times.extend(out)
        
        
    # Identify the N closest (travel time) locations
    travel_times = pd.DataFrame(travel_times)
    travel_times.columns = ('loc_name','coords','distance','duration','mode')
    tmp_small = travel_times.groupby('mode')[sm_pref].nsmallest(num_sm)
    
    return travel_times.ix[tmp_small.index.levels[1]]


