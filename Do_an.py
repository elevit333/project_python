import tkinter as Tk
import pandas as pd

# Đọc file CSV với encoding phù hợp
file_path = 'laptop_price.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1') #Đối số này chỉ định mã hóa của tệp, đảm bảo rằng dữ liệu được đọc chính xác, đặc biệt nếu nó chứa các ký tự đặc biệt

# Trích xuất cột laptop_ID

data_set = {'Hãng': data['Company'],
'Product': data["Product"],
'cpu': data["Cpu"],
'ram': data["Ram"],
'memory': data["Memory"],
'GPU': data["Gpu"],
'Loại máy':data['Typename'],
'Độ phân giải màn hình':data['ScreenResolution'],
'Khối lượng':data['Weight'],
'Hệ điều hành':data['OpSys']}
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

#hiển thị bộ lọc
result_text.delete('1.0',tk.END)
for index, row in filtered_df.iterrows():
  result_text.insert(tk.END, str(row.to_dict())+'\n')

root.Tk()
root.title('Ứng dụng tìm laptop')

filter_vars = {}
for column in ['Hãng', 'Loại máy', 'CPU', 'RAM', 'Memory', 'Card đồ họa']:
    label = tk.Label(root, text=column + ":")
    label.pack()
    filter_vars[column] = tk.StringVar(root)
    filter_vars[column].set("Tất cả")
    options = ['Tất cả'] + sorted(df[column].unique().tolist())
    dropdown = tk.OptionMenu(root, filter_vars[column], *options)
    dropdown.pack()
