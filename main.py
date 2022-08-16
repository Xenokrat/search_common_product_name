from common_words_tokens import CommonWords


def main():
    data = CommonWords(path_to_client_data="sample_data/client_titles.xlsx",
                       path_to_base_data="sample_data/base_titles.xlsx",)
    res = data.filter_df_by_length_of_sets()
    res.to_excel('test_output.xlsx')


if __name__ == '__main__':
    main()


