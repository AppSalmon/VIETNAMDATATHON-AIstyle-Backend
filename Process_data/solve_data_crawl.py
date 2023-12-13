import pandas as pd
import re

file_path = 'data_adidas_2.json'
df = pd.read_json(file_path)

# Thay thế các dấu /n trong description
descrip =  []
for index,item in enumerate(df.description):
    try:
        descrip.append(re.sub("\n"," ",item))
    except:
        descrip.append(item)

df.description = descrip

# Xóa đi kí tự khác chứ số trong price -> int 
price =  []
for index,item in enumerate(df.price):
    try:
        price.append(int(re.sub(r'\D', '', item)))
    except:
        price.append(item)
df.price = price

# Xóa đi kí tự khác chứ số trong original price -> int 
origin_price =  []
for index,item in enumerate(df.original_price):
    try:
        origin_price.append(int(re.sub(r'\D', '', item)))
    except:
        origin_price.append(item)

df.original_price = origin_price

# Thêm vào df cột sale ( tạm gán = 0  )
df.sale = 0
# Các cột cần chuyển về chữ thường
# Các cột cần chuyển về chữ thường
list_columns_convert_lower = ['availability', 'brand', 'color', 'currency','description','name','category','cloth_gender']
for col in list_columns_convert_lower:
    df[col] = df[col].str.lower()
# xuất file csv
df.to_csv("data_crawl_new.csv")