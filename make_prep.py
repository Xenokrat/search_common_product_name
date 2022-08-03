from lcs import LSC
import os
import pandas as pd


class DataHandler:
    def __init__(self, path_to_client_data: str, path_to_base_data: str):
        assert os.path.exists(path_to_client_data), f'{path_to_client_data} do not exists'
        assert os.path.exists(path_to_base_data), f'{path_to_base_data} do not exists'

        self.path_to_client_data = path_to_client_data
        self.path_to_base_data = path_to_base_data

        self.client_sku = self.make_client_sku()
        self.ean_code = self.make_ean_code()
        self.base_sku = self.make_base_sku()

    # @property
    # def client_sku(self):
    #     return self.__client_sku
    #
    # @property
    # def ean_code(self):
    #     print('getter method called')
    #     return self.__ean_code
    #
    # @property
    # def base_code(self):
    #     return self.__base_sku

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
            df.rename(columns={'Product_Title': 'client_sku'}, inplace=True)
            return df.loc[:, ['client_sku', 'EAN_CODE']]

    def make_base_sku(self):
        df = pd.read_excel(self.path_to_base_data)
        if 'Product_Title' not in df:
            raise Exception('No "Product_Title" column')
        else:
            return df['Product_Title']

    def cross_join(self):
        client_data_var = self.client_sku
        base_data_var = self.base_sku

        client_data_var = client_data_var.to_frame().rename(columns={'Product_Title': 'client_product_title'})
        base_data_var = base_data_var.to_frame().rename(columns={'Product_Title': 'base_product_title'})

        # create common key
        client_data_var['key'] = 0
        base_data_var['key'] = 0
        df = client_data_var.merge(base_data_var, on='key', how='outer')
        del df['key']

        res = (
            df['client_product_title'],
            df['base_product_title'],
        )
        return res


class DataSaver:
    pass
