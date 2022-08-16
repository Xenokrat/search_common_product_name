import os
import pandas as pd


class MultipleBrands:
    def __init__(self, path_to_client_data: str, path_to_base_data: str):
        assert os.path.exists(path_to_client_data), \
            f'{path_to_client_data} do not exists'
        assert os.path.exists(path_to_base_data), \
            f'{path_to_base_data} do not exists'

        self.path_to_client_data = path_to_client_data
        self.path_to_base_data = path_to_base_data

        self.__client_df = self.make_client_df()
        self.__base_df = self.make_base_df()

    def make_client_df(self):
        """
        Include 'client_product_title', 'ean_code', 'brand_name'
        :return: DataFrame with client's data
        """
        df = pd.read_excel(self.path_to_client_data)
        if 'client_product_title' not in df:
            raise Exception('No "client_product_title" column')
        elif 'ean_code' not in df:
            raise Exception('No "ean_code" column')
        elif 'brand_name' not in df:
            raise Exception('No "brand_name" column')

        return df['client_product_title', 'ean_code', 'brand_name']

    def make_base_df(self):
        """
        Include 'base_product_title', 'product_id', 'brand_name'
        :return: DataFrame with data from SQL base
        """
        df = pd.read_excel(self.path_to_base_data)
        if 'base_product_title' not in df:
            raise Exception('No "base_product_title" column')
        elif 'product_id' not in df:
            raise Exception('No "product_id" column')
        elif 'brand_name' not in df:
            raise Exception('No "brand_name" column')

        return df['base_product_title', 'product_id', 'brand_name']
