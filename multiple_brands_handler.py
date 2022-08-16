import os
import pandas as pd
from common_words_tokens import CommonWords


class MultipleBrands(CommonWords):
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

        df['brand_name'] = df['brand_name'].str.title()
        df = df.loc[:, ['client_product_title', 'ean_code', 'brand_name']] \
            .sort_values(by=['brand_name', 'client_product_title']) \
            .dropna(axis=0, how='any')

        clear_df = df[
            (df['client_product_title'].apply(lambda x: isinstance(x, str)))
        ]
        assert not clear_df['client_product_title'].isnull().values.any()
        assert not clear_df['brand_name'].isnull().values.any()
        return clear_df

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

        df = df.loc[:, ['base_product_title', 'product_id', 'brand_name']] \
            .sort_values(by=['brand_name', 'base_product_title']) \
            .dropna(axis=0, how='any')

        clear_df = df[
            (df['base_product_title'].apply(lambda x: isinstance(x, str)))
        ]
        assert not clear_df['base_product_title'].isnull().values.any()
        assert not clear_df['brand_name'].isnull().values.any()
        return clear_df

    def cross_join_table(self):
        df_cross = \
            self.__client_df[['client_product_title', 'brand_name']].merge(
                self.__base_df[['base_product_title', 'brand_name']],
                on='brand_name',
                how='inner'
            )
        assert df_cross.shape[0] > 1
        return df_cross

    def calc_cw_dataframe(self) -> pd.DataFrame:
        """
        Applying calc_common_words to all possible variations
        :returns dataframe columns: client_product_title, base_product_title,
        common_words
        """
        df = self.cross_join_table()
        df['common_words'] = df.apply(
            lambda x: self.calc_common_words(x['client_product_title'],
                                             x['base_product_title']),
            axis=1
        )
        return df

    def filter_df_by_length_of_sets(self) -> pd.DataFrame:
        """
        Filtering dataframe with sets of max length for each product
        :return: filtered df with ean code
        """

        df = self.calc_cw_dataframe()
        grouped_df = df.groupby(
            ['client_product_title', 'brand_name'], as_index=False
        ).agg({
            'common_words': self.max_set_length
        })

        res_df = grouped_df.merge(
            df,
            how='inner',
            on=['client_product_title', 'common_words']
        )

        return res_df

    def make_result_df(self) -> pd.DataFrame:
        """
        Join EAN_CODE
        Join product_id
        :return: full DataFrame
        """
        df = self.filter_df_by_length_of_sets()
        res_df_with_ean = df.merge(
            self.__client_df[['ean_code', 'client_product_title']],
            how='left',
            on='client_product_title'
        )

        res_df_with_sku = res_df_with_ean.merge(
            self.__base_df[['product_id', 'base_product_title']],
            how='left',
            on='base_product_title'
        )
        return res_df_with_sku
