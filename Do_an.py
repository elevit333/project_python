import tkinter as tk
import pandas as pd

# Đọc file CSV với encoding phù hợp
file_path = 'laptop_price.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Trích xuất cột laptop_ID
data_set = {'Hãng': data['Company'],
'Product': data["Product"],
'cpu': data["Cpu"],
'ram': data["Ram"],
'memory': data["Memory"],
'GPU': data["Gpu"]}
df = pd.DataFrame(data_set)
#giao diện bộ lọc laptop
def bo_loc():
    filtered_df = df.copy()
    for column in ['Hãng','cpu','ram','memory','GPU']:
      selected_value = filter_vars[column].get()
      if selected_value != 'Tất cả':
        filtered_df = filtered_df[filtered_df[column] == selected_value]
#lọc theo khoảng giá
    min_price = float(min_price_entry.get()) if min_price_entry.get() else 0
    max_price = float(max_price_entry.get()) if max_price_entry.get() else float('inf')
    filtered_df = filtered_df[(filtered_df['Giá cả'] >= min_price) & (filtered_df['Giá cả'] <= max_price)]
