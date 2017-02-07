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
    
    





    
def nearest_feature(address, feature, num_sm, con):
    """
    Returns travel time (Car, PT, Walking) for the N nearest features 
    Input:
        df = Dataframe containing an address column used for searching
        feature = What to search for; supermarket, high-school etc
        num_sm = Closest (travel time) N to return
        con = Initialised Google maps connection object
    Output:
        df = original df with columns for travel times
    """

    # Get Address Coordinates
    address_coords = con.geocode(address)[0]['geometry']['location']
    
    # Find all places within radius of POI
    places_out = gmaps.places(query = feature
                                , radius = 2000   # Search within 2km. Might change later
                                , location = address_coords)
    
    
    # Extract Feature Name & Coordinates
    nearby = [[x['name'],x['geometry']['location']] for x in places_out['results']]
    
    
    # For each place, calculate the travel time
    transport_methods = ['driving','transit','walking']
    
    travel_times = []
    for mode in transport_methods:
        
        for dest in nearby:
            
            # Get Directions
            directions = gmaps.directions(origin = address_coords
                            , destination = dest[1]
                            , mode = mode
                            , units = 'metric'
                            #, arrival_time = 9 # This currently isn't working
                            )
            
            # Extract Travel Time & Distance
            out = [dest[0]                                          # Feature Name
                   , mode                                           # Transport Method
                   , directions[0]['legs'][0]['distance']['text']   # Distance (Km)
                   , directions[0]['legs'][0]['duration']['text']   # Travel Time
                   ]
            
            
            '''
            TO-DO:
            -For each transport mode, capture the N fastest (time) locations
            -Return some data structure containing just those locations for that mode
            
            Collect all modes & close out fn
            '''
            
            travel_times.append(out)


            
    return travel_times



