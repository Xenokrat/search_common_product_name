from multiple_brands_handler import MultipleBrands


def main():
    data = MultipleBrands(path_to_client_data="sample_data/client_titles.xlsx",
                          path_to_base_data="sample_data/base_titles.xlsx",)
    res = data.make_result_df()
    res.to_excel('test_output.xlsx')


if __name__ == '__main__':
    main()


