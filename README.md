# Search Common Product Name
## Identify the same product names by comparasing the common string between two given names
#### Test samples in /sample_data directory

**client_titles.xlsx** template

| Product_Title    | EAN_CODE     |
|------------------|--------------|
| Yoghurt 1, 200 g | 400000000000 |
| Yoghurt 2, 400 g | 400000000001 |

<br/>

**base_titles.xlsx** template

| Product_Title       | 
|---------------------|
| Yohurt 10, 200 g    | 
| Yoghurts 20, 400 ml |

<br/>

**Output**

| client_sku       | common_string | base_sku         | EAN_CODE     |
|------------------|---------------|------------------|--------------|
| Yoghurt 1, 200 g | ohurt 1       | Yohurt 10, 200 g | 400000000000 |
