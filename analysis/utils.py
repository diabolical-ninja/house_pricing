"""
Title:      Analysis Utility Functions
Desc:       A collection of functions to aid analysis
Author:
Date:
"""


from math import radians, cos, sin, asin, sqrt
import json
from requests import request


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    
    From: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r



def street2coordinates(address):
    """
    Function to leverage the DSTK Street Address to Coordinates 
    http://www.datasciencetoolkit.org/developerdocs#street2coordinates
    
    address (str or list): 
        if str then single GET call
        if list then batch POST calls
    
    returns (dict): Returned JSON object
    """
    
    base_url = "http://www.datasciencetoolkit.org/street2coordinates"
    
    if isinstance(address, str):
        try:
            full_url = "{}/{}".format(base_url, address)
            response = request("GET",url = full_url)
        except Exception as ex:
            print(ex)
    
    elif isinstance(address, list):
        try:
            payload = json.dumps(address)
            response = request("POST",url = base_url, data = payload)          
        except Exception as ex:
            print(ex)
            
    return response.json()