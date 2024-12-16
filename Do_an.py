import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# tạo app
app = tk.Tk()
app.title("Laptop Filter GUI")
app.geometry("950x780")

# up data và xử lý các lỗi không tồn tại hoặc ko tìm thấy
file_path = 'laptop_price.csv'
try:
    data = pd.read_csv(file_path, encoding='ISO-8859-1')
except FileNotFoundError:
    messagebox.showerror("Error", "File 'laptop_price.csv' not found!")
    app.destroy()
    exit()
except Exception as e:
    messagebox.showerror("Error", f"Failed to load data: {e}")
    app.destroy()
    exit()

# phân chia bộ lọc
def update_combobox_options(filter_key, filtered_data):
    """Nếu người dùng đã chọn 1 option thì các widget khác sẽ tự thay đổi các option liên quan đến phần đã chọn"""
    for key, combobox in filter_comboboxes.items():
        if key != filter_key:
            unique_values = [''] + sorted(filtered_data[key].dropna().unique().astype(str))
            combobox['values'] = unique_values

# Define the logic for dynamic filtering
def on_filter_change(event=None):
    """ghi nhận các sự thay đổi lựa chọn từ người dùng và tự động cập nhật các ô còn lại."""
    filtered_data = data.copy()

    for key, var in filters.items():
        value = var.get().strip()
        if value:
            filtered_data = filtered_data[filtered_data[key].astype(str).str.contains(value, case=False)]

    update_combobox_options(event.widget, filtered_data)
    update_table(filtered_data)

# tạo khung và bố cục
filter_frame = tk.Frame(app, bd=2, relief=tk.GROOVE, padx=10, pady=10)
filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

table_frame = tk.Frame(app, bd=2, relief=tk.GROOVE)
table_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True,padx=10, pady = 10)

# thêm các bộ lọc và widget
filters = {}
filter_comboboxes = {}
row = 0

for key in ['Company', 'TypeName', 'Cpu', 'Gpu', 'Ram', 'Memory', 'OpSys']:
    label = tk.Label(filter_frame, text=f"{key}:", anchor='w')
    label.grid(row=row, column=0, sticky='w', padx=5, pady=5)

    var = tk.StringVar()
    filters[key] = var

    combobox = ttk.Combobox(filter_frame, textvariable=var, state="readonly")
    combobox['values'] = [''] + sorted(data[key].dropna().unique().astype(str))
    combobox.grid(row=row, column=1, padx=5, pady=5)
    combobox.bind('<<ComboboxSelected>>', on_filter_change)

    filter_comboboxes[key] = combobox
    row += 1

# tạo bảng để hiển thị kết quả
columns = list(data.columns)
scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

table = ttk.Treeview(table_frame, columns=columns, show="headings",
                     yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120, anchor=tk.W)  # Adjust column width

table.pack(fill=tk.BOTH, expand=True)

scroll_y.config(command=table.yview)
scroll_x.config(command=table.xview)

# Define function to update the table
def update_table(filtered_data):
    # Clear existing rows
    for row in table.get_children():
        table.delete(row)

    # Insert new rows
    for _, row in filtered_data.iterrows():
        table.insert("", tk.END, values=list(row))

# Load initial data into the table
update_table(data)

app.mainloop()
