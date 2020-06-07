import pandas as pd
from pandas.io.json import json_normalize
import domainClient as dc
from lib.domain_authentication import get_access_token


class AuctionResults:

    def __init__(self, configuration: dict):
        """Setup method to:
            - Generate authentication token
            - Create Config client
            - Create sales results client

        Args:
            configuration (dict): Domain configuration containing:
                - client (str): Client ID
                - secret (str): Secret Key
                - scopes (list): Required API Scopes
        """

        # Authenticate
        self.scopes = configuration['scopes']
        self.auth_info = get_access_token(configuration['client'],
                                          configuration['secret'],
                                          self.scopes)

        # Create Domain Client
        self.configuration = dc.Configuration()
        self.configuration.access_token = self.auth_info['access_token']

        # Sales Results Object
        self.sales_results = dc.SalesResultsApi(dc.ApiClient(self.configuration))

    def get_city_results(self, city: str):
        """Download Auction Results for a City

        Uses: https://developer.domain.com.au/docs/apis/pkg_properties_locations/references/salesresults_listings

        Args:
            city (str): City of interest

        Returns:
            pandas.core.frame.DataFrame: Auction results for the given city
        """
        # Get Auction Results & conver to useable dicts
        results = self.sales_results.sales_results_listings(city)
        results = [result.to_dict() for result in results]

        # Convert to DF & fix column names
        results_df = json_normalize(results)
        results_df.columns = [x.replace('.', '_') for x in results_df.columns]

        # Drop geo_location column
        if 'geo_location' in results_df.columns:
            results_df.drop(columns = ['geo_location'], inplace=True)

        # Add City Name
        results_df['city'] = city.lower()

        # Add Auction Results Date
        results_df['date'] = self.get_auction_date(city)

        return results_df

    def get_auction_date(self, city):
        """Get the date of the auction results

        Uses: https://developer.domain.com.au/docs/apis/pkg_properties_locations/references/salesresults_head

        Args:
            city (str): City of interest

        Returns:
            str: Date the auction results relate to
        """

        results_info = self.sales_results.sales_results_head()
        return results_info.auctioned_date.strftime("%Y-%m-%d")
