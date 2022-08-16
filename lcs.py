import pandas as pd
from make_prep import DataHandler


class LSC(DataHandler):
    def __init__(self, path_to_client_data, path_to_base_data):
        super().__init__(
            path_to_client_data,
            path_to_base_data,
        )
        self.client_sku = self.make_client_sku()
        self.ean_code = self.make_ean_code()
        self.base_sku = self.make_base_sku()

        self.common_string = None

    def __repr__(self):
        return f'''Class: {self.__class__}, 
        Client SKU with size {self.client_sku.shape}, 
        SKU from base with size {self.base_sku.shape}'''

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def max_len_str(lst):
        max_len = -1
        res = ''
        for val in lst:
            if len(val) > max_len:
                max_len = len(val)
                res = val
        return res

    def calculate_report(self):
        df = pd.DataFrame({
            'client_sku': self.client_sku,
            'base_sku': self.base_sku,
            'common_string': self.common_string
        })
        res_grp = df.groupby('client_sku', as_index=False).agg({'common_string': self.max_len_str})
        res = res_grp.merge(df, how='inner', on=['client_sku', 'common_string'])
        return res

    def calculate_lcs(self):
        for ind, row in enumerate(zip(self.client_sku, self.base_sku)):
            str1, str2 = row
            parsed_common_string = self.longest_common_string(str1=str1, str2=str2)
            self.common_string = pd.concat(
                [self.common_string, pd.Series(parsed_common_string, dtype=str)],
                ignore_index=True
            )

    def longest_common_string(self, str1: str, str2: str) -> list[str]:
        str1 = self.make_pretty_str(str1)
        str2 = self.make_pretty_str(str2)

        n = len(str1)
        m = len(str2)
        longest_str = 0
        set_of_str = set()

        matrix = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        for i in range(n):
            for j in range(m):
                if str1[i] == str2[j]:
                    counter: int = matrix[j][i] + 1
                    matrix[j + 1][i + 1] = counter

                    if counter > longest_str:
                        longest_str = counter
                        set_of_str = set()
                        set_of_str.add(str1[i - counter + 1: i + 1])

                    # if counter == longest_str:
                    #     set_of_str.add(str1[i - counter + 1: i + 1])

        return list(set_of_str)
