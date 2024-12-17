import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# Initialize the Tkinter app
app = tk.Tk()
app.title("Laptop Filter GUI")
app.geometry("950x780")

# Load the dataset with error handling
file_path = '/mnt/data/laptop_price.csv'
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

# Define filters
def update_combobox_options(filter_key, filtered_data):
    """Update the options of the comboboxes based on filtered data."""
    for key, combobox in filter_comboboxes.items():
        if key != filter_key:
            unique_values = [''] + sorted(filtered_data[key].dropna().unique().astype(str))
            combobox['values'] = unique_values

# Define the logic for dynamic filtering
def on_filter_change(event=None):
    """Handle changes in filters and update options dynamically."""
    filtered_data = data.copy()

    # Apply text-based filters
    for key, var in filters.items():
        value = var.get().strip()
        if value:
            filtered_data = filtered_data[filtered_data[key].astype(str).str.contains(value, case=False)]

    # Apply price range filter
    try:
        min_price = float(min_price_entry.get()) if min_price_entry.get() else 0
        max_price = float(max_price_entry.get()) if max_price_entry.get() else float('inf')
        filtered_data = filtered_data[(filtered_data['Price_euros'] >= min_price) &
                                      (filtered_data['Price_euros'] <= max_price)]
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for price range.")
        return

    # Apply sorting
    sort_order = sort_var.get()
    if sort_order == "Ascending":
        filtered_data = filtered_data.sort_values(by='Price_euros', ascending=True)
    elif sort_order == "Descending":
        filtered_data = filtered_data.sort_values(by='Price_euros', ascending=False)

    update_combobox_options(event.widget, filtered_data)
    update_table(filtered_data)

# Create frames for layout
filter_frame = tk.Frame(app, bd=2, relief=tk.GROOVE, padx=10, pady=10)
filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

table_frame = tk.Frame(app, bd=2, relief=tk.GROOVE)
table_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add filter widgets in filter_frame
filters = {}
filter_comboboxes = {}
row = 0

for key in ['Company', 'Product', 'TypeName', 'Cpu', 'Gpu', 'Ram', 'Memory', 'OpSys']:
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

# Add price range filter
price_label = tk.Label(filter_frame, text="Price Range:", anchor='w')
price_label.grid(row=row, column=0, sticky='w', padx=5, pady=5)

min_price_entry = tk.Entry(filter_frame, width=10)
min_price_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)

max_price_entry = tk.Entry(filter_frame, width=10)
max_price_entry.grid(row=row, column=1, sticky='e', padx=5, pady=5)
row += 1

# Add sort filter
sort_var = tk.StringVar()
sort_var.set("None")  # Default sort option
sort_label = tk.Label(filter_frame, text="Sort by Price:", anchor='w')
sort_label.grid(row=row, column=0, sticky='w', padx=5, pady=5)

sort_combobox = ttk.Combobox(filter_frame, textvariable=sort_var, state="readonly")
sort_combobox['values'] = ["None", "Ascending", "Descending"]
sort_combobox.grid(row=row, column=1, padx=5, pady=5)
sort_combobox.bind('<<ComboboxSelected>>', on_filter_change)
row += 1

#thêm các lựa chọn về biểu đồ


elif option == 'Laptop Count by Company':
        counts = data['Company'].value_counts()
        counts.plot(kind='barh', title='Laptop Count by Company', xlabel='Count', ylabel='Company', color='red', grid=True)
        plt.show()

#hiển thị bảng kết quả 
columns = list(data.columns)
scroll_y tk.Scrollbar(table_frame, orient=tk.VERTICAL)
scroll_x tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

scroll_y.pack(side = tk.RIGHT, fill=tk.Y)
scroll_x.pack(side = tk.BOTTOM, fill= tk.X)

table = ttk.Treeview(table_frame, columns=columns, show="headings",
                     yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

for col in columns:
    table.heading(col, text = col)
    table.heading(col, width=120 , anchor= tk.M) # Điều chỉnh chiều rộng cột

table.pack(fill=tk.BOTH , expand=True)


scroll_y.config(command=table.yview)
scroll_x.config(command=table.xview)

# Xác định chức năng để cập nhật bảng
def update_table(filtered_data):
    # Xóa các hàng hiện có
    for row in table.get_children():
        table.delete(row)


    # Chèn hàng mới
    for _,row in filtered_data.iterrow():
        table.insert("", tk.END, values=list(row))

# Tải dữ liệu ban đầu vào bảng
update_table(data)

app.mainloop()
