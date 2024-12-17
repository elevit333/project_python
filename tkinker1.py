import tkinter as tk
import pandas as pd

# Đọc file CSV với encoding phù hợp
file_path = 'laptop_price.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Trích xuất cột laptop_ID
laptop_ids = data['Company']
loai_laptop= data["Product"]
cpu_laptop= data["Cpu"]
ram_laptop = data["Ram"]
memory_laptop = data["Memory"]
card_dohoa_laptop = data["Gpu"]
