from lcs import LSC
from make_prep import DataHandler
import pandas as pd


def main():
    data = DataHandler(path_to_client_data="sample_data/client_titles.xlsx",
                       path_to_base_data="sample_data/base_titles.xlsx",)

    client_sku, base_sku = data.cross_join()
    lcs = LSC(client_sku, base_sku)
    lcs.calculate_lcs()
    res = lcs.calculate_report()
    res = res.merge(data.ean_code, how='left', on='client_sku')
    res.to_csv('output.csv', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
