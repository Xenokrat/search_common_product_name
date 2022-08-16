import pandas as pd
from make_prep import DataHandler


class CommonWords(DataHandler):
    def __init__(self, path_to_client_data, path_to_base_data):
        super().__init__(
            path_to_client_data,
            path_to_base_data,
        )
        self.client_sku = self.make_client_sku()
        self.ean_code = self.make_ean_code()
        self.base_sku = self.make_base_sku()

    def tokenize(self, text) -> frozenset:
        """
        Tokenize words in text
        :return  set of words
        """
        text = self.make_pretty_str(text)
        text = text.split(' ')
        return frozenset(text)

    def calc_common_words(self, text1, text2) -> frozenset:
        """
        Calculates common words between two strings
        :returns set of common words
        """
        tokenized_text1 = self.tokenize(text1)
        tokenized_text2 = self.tokenize(text2)
        return tokenized_text1 & tokenized_text2

    def calc_cw_dataframe(self) -> pd.DataFrame:
        """
        Applying calc_common_words to all possible variations
        :returns dataframe columns: client_product_title, base_product_title, common_words
        """
        # df columns: client_product_title, base_product_title
        df = self.cross_join_table()
        df['common_words'] = df.apply(
            lambda x: self.calc_common_words(x['client_product_title'],
                                             x['base_product_title']),
            axis=1
        )
        return df

    @staticmethod
    def max_set_length(list_of_sets) -> int:
        """
        :param list_of_sets: list of sets, used in "apply"
        :return: set with max length
        """
        max_len = -1
        res = 0
        for set_ in list_of_sets:
            if len(set_) > max_len:
                max_len = len(set_)
                res = set_
        return res

    def filter_df_by_length_of_sets(self) -> pd.DataFrame:
        """
        Filtering dataframe with sets of max length for each product
        Join EAN_CODE
        Join product_id
        :return: filtered df with ean code
        """

        df = self.calc_cw_dataframe()
        grouped_df = df.groupby('client_product_title', as_index=False) \
            .agg({'common_words': self.max_set_length})

        res_df = grouped_df.merge(df, how='inner',
                                  on=['client_product_title', 'common_words'])

        res_df_with_ean = res_df.merge(self.ean_code,
                                       how='left',
                                       on='client_product_title')

        res_df_with_sku = res_df_with_ean.merge(self.prod_id,
                                                how='left',
                                                on='base_product_title')
        return res_df_with_sku
