from functools import lru_cache
from importlib import resources as impresources
from typing import List

import dateparser
import pandas as pd
import requests
from requests import HTTPError
from . import data as static_data


class PyPrycd:
    """
    This module provides a simple API for interacting with the PRYCD APIs for real estate analysis.
    """

    def __init__(self, pricing_api_key: str = None, comp_api_key: str = None) -> None:
        self.__pricing_api_key = pricing_api_key
        self.__comp_api_key = comp_api_key

    def set_pricing_api_key(self, pricing_api_key: str) -> None:
        self.__pricing_api_key = pricing_api_key

    def set_comp_api_key(self, comp_api_key: str) -> None:
        self.__comp_api_key = comp_api_key

    @lru_cache
    def get_pricing(self, apn: str, county_fips: str, latitude: float = None, longitude: float = None,
                    acreage: float = None, test: bool = False) -> pd.DataFrame:
        """
        Returns PRYCD estimated values for a requested property
        :param apn: The property Assessor Parcel Number (APN). (Required)
        :param county_fips: The County FIPS Code (Required)
        :param latitude: The latitude of the property. Used if the APN is not found.
        :param longitude: The longitude of the property. Used if the APN is not found.
        :param acreage: The acreage of the property. Used if the APN is not found.
        :param test: Whether or not to use the testing URL (Default: False)
        :return: A Pandas DataFrame of the PRYCD estimated pricing
        """

        if test is False:
            url = "https://gd4w0qoug6.execute-api.us-east-2.amazonaws.com/prod/api/priceProperty"
        else:
            url = "https://stoplight.io/mocks/prycd/pricing-api/109961998"

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-api-key': self.__pricing_api_key
        }

        data = {
            "apn": apn,
            "county_fips": county_fips,
        }

        if latitude is not None and longitude is not None:
            data['latitude'] = latitude
            data['longitude'] = longitude

        if acreage is not None:
            data['acreage'] = acreage

        response = requests.post(url=url, json=data, headers=headers, timeout=1000)
        if response.status_code == 200:
            pricing_data = response.json()
            return pd.json_normalize(pricing_data['pricing'])

        raise HTTPError(response.status_code)

    @lru_cache
    def get_comps(self, count_only: bool = False,
                  county: str = None,
                  min_acreage: float = 0.0, max_acreage: float = 0.0,
                  state: str = None,
                  city: str = None,
                  zip_code: str = None,
                  min_price: float = 0.0, max_price: float = 0.0,
                  min_list_date: str = None, max_list_date: str = None,
                  min_sold_date: str = None, max_sold_date: str = None,
                  comp_type: str = None,
                  remove_duplicates: bool = False,
                  excluded_sources=None,
                  comp_age: int = 1, test: bool = False
                  ) -> pd.DataFrame:

        if excluded_sources is None:
            excluded_sources = []
        if test is False:
            url = "https://prycd.com/_functions/comps"
        else:
            url = "https://prycd.com/_functions-dev/comps"

        params = {
            'user_id': self.__comp_api_key,
            'county': county,
            'min_acreage': min_acreage,
            'max_acreage': max_acreage,
            'state': state,
            'city': city,
            'zip_code': zip_code
        }

        if count_only:
            params['count'] = 1
        else:
            params['count'] = 0

        if min_price >= 0.0:
            params['min_price'] = min_price
        if max_price > 0.0:
            params['max_price'] = max_price

        if comp_type.lower() == 'for_sale':
            params['comp_type'] = 1
        elif comp_type.lower() == 'sold':
            params['comp_type'] = 2
        else:
            params['comp_type'] = 0

        if remove_duplicates:
            params['remove_duplicates'] = 1
        else:
            params['remove_duplicates'] = 0

        if len(excluded_sources) > 0:
            params['excluded_sources'] = ','.join(excluded_sources)

        if comp_age > 1:
            params['comp_age'] = comp_age

        # Clean up dates.
        if min_list_date:
            params['min_list_date'] = PyPrycd.__convert_date(min_list_date)
        if max_list_date:
            params['max_list_date'] = PyPrycd.__convert_date(max_list_date)
        if min_sold_date:
            params['min_sold_date'] = PyPrycd.__convert_date(min_sold_date)
        if max_sold_date:
            params['max_sold_date'] = PyPrycd.__convert_date(max_sold_date)

        response = requests.get(url, params=params, timeout=1000)

        if response.status_code == 200:
            return response.json()

        raise HTTPError(response.status_code)

    @staticmethod
    @lru_cache
    def get_fips_code(county_name: str) -> str:
        """
        Returns the FIPS code for a given county.  Note, you must specify the full county name and state.
        Example: Maricopa County, AZ.
        :param county_name: The county name and state.
        :return: The FIPS code for the provided county name.
        """
        input_file = impresources.files(static_data) / 'county_fips_master.csv'
        data = pd.read_csv(input_file, encoding="ISO-8859-1")
        fips_code = data[data['long_name'].str.lower() == county_name.lower()][['fips']]
        return fips_code['fips'].values[0]

    @staticmethod
    @lru_cache
    def get_counties_in_state(state: str) -> List[str]:
        input_file = impresources.files(static_data) / 'county_fips_master.csv'
        data = pd.read_csv(input_file, encoding="ISO-8859-1")

        # If the input is a state code
        if len(state) == 2:
            return data[data['state_abbr'].str.upper() == state]['long_name'].to_list()
        else:
            return data[data['state_name'].str.lower() == state.lower()]['long_name'].to_list()

    @staticmethod
    @lru_cache
    def get_state_abbr_list():
        input_file = impresources.files(static_data) / 'county_fips_master.csv'
        raw_data = pd.read_csv(input_file, encoding="ISO-8859-1")
        return raw_data['state_abbr'].drop_duplicates().to_list()

    @staticmethod
    @lru_cache
    def get_state_names():
        input_file = impresources.files(static_data) / 'county_fips_master.csv'
        raw_data = pd.read_csv(input_file, encoding="ISO-8859-1")
        return raw_data['state_name'].drop_duplicates().to_list()

    @staticmethod
    def __convert_date(date_str:str) -> str:
        """
        Converts a date to the mm/dd/yyyy format required by Prycd
        :param date_str:
        :return: A date string in the format mm/dd/yyyy
        """
        date = dateparser.parse(date_str)
        return date.strftime("%m/%d/%Y")
