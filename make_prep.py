import os
import pandas as pd
import re


def add_space_between_num_and_char(string):
    numbers = '0123456789'
    new_string = string
    for ind in range(len(string) - 1, 0, -1):
        current_char = string[-ind]
        previous_char = string[-ind - 1]
        if current_char not in numbers and previous_char in numbers:
            new_string = string[:-ind] + ' ' + string[-ind:]
            break

    return new_string


class DataHandler:
    def __init__(self, path_to_client_data: str, path_to_base_data: str):
        assert os.path.exists(path_to_client_data), f'{path_to_client_data} do not exists'
        assert os.path.exists(path_to_base_data), f'{path_to_base_data} do not exists'

        self.path_to_client_data = path_to_client_data
        self.path_to_base_data = path_to_base_data

        self.client_sku = self.make_client_sku()
        self.ean_code = self.make_ean_code()
        self.base_sku = self.make_base_sku()
        self.prod_id = self.make_prod_id()

    @staticmethod
    def make_pretty_str(string: str) -> str:
        try:
            string = string.lower()
            string = re.sub('[^\w\s_]', " ", string)
            string = re.sub("_", " ", string)
            string = add_space_between_num_and_char(string)
            string = " ".join(string.split())
        except AttributeError:
            print(string)
            raise AttributeError
        return string

    def make_client_sku(self):
        df = pd.read_excel(self.path_to_client_data)
        if 'Product_Title' not in df:
            raise Exception('No "Product_Title" column')
        else:
            return df['Product_Title']

    def make_ean_code(self):
        df = pd.read_excel(self.path_to_client_data)
        if 'EAN_CODE' not in df:
            raise Exception('No "EAN_CODE" column')
        else:
            df.rename(columns={'Product_Title': 'client_product_title'},
                      inplace=True)
            return df.loc[:, ['client_product_title', 'EAN_CODE']]

    def make_prod_id(self):
        df = pd.read_excel(self.path_to_base_data)
        if 'product_id' not in df:
            raise Exception('No "product_id" column')
        else:
            df.rename(columns={'Product_Title': 'base_product_title'},
                      inplace=True)
            return df.loc[:, ['base_product_title', 'product_id']]

    def make_base_sku(self):
        df = pd.read_excel(self.path_to_base_data)
        if 'Product_Title' not in df:
            raise Exception('No "Product_Title" column')
        else:
            return df['Product_Title']

    def cross_join_table(self):
        client_data_var = self.client_sku
        base_data_var = self.base_sku

        client_data_var = client_data_var.to_frame().rename(columns={'Product_Title': 'client_product_title'})
        base_data_var = base_data_var.to_frame().rename(columns={'Product_Title': 'base_product_title'})

        # create common key
        client_data_var['key'] = 0
        base_data_var['key'] = 0
        df = client_data_var.merge(base_data_var, on='key', how='outer')
        del df['key']

        return df
