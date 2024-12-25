import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# Initialize the Tkinter app
app = tk.Tk()
app.title("Thông Tin Laptop")
app.geometry("950x780")

# tải và xử lý dataset
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

# Định nghĩa bộ lọc logic
def update_combobox_options(filter_key, filtered_data):
    for key, combobox in filter_comboboxes.items():
        if key != filter_key:
            unique_values = [''] + sorted(filtered_data[key].dropna().unique().astype(str))
            combobox['values'] = unique_values

#tạo hàm cập nhật table
def update_table(filtered_data):
    """Update the table display with filtered data."""
    # Clear existing data in the table
    for row in table.get_children():
        table.delete(row)
    # Insert new data into the table
    for _, row in filtered_data.iterrows():
        table.insert("", "end", values=list(row))

# Define the logic for dynamic filtering
def on_filter_change(event=None):
    filtered_data = data.copy()

    # Apply text-based filters
    for key, var in filters.items():
        value = var.get().strip()
        if value:
            filtered_data = filtered_data[filtered_data[key].astype(str).str.contains(value, case=False)]

    # Bộ lọc theo giá
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

# Tạo khung
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

# Thêm các lựa chọn về biểu đồ
def show_chart(option):
    if option == 'Average Price by Company':
        avg_price = data.groupby('Company')['Price_euros'].mean()
        avg_price.plot(kind='bar', title='Average Price by Company', ylabel='Price (Euros)', xlabel='Company', color='blue', grid=True)
        plt.xticks(rotation=45)
        plt.show()

    elif option == 'Laptop Count by Company':
        counts = data['Company'].value_counts()
        counts.plot(kind='barh', title='Laptop Count by Company', xlabel='Count', ylabel='Company', color='red', grid=True)
        plt.show()

    elif option == 'Laptop Count by Selected Company':
        company = filters['Company'].get()
        if company:
            selected_data = data[data['Company'] == company]
            counts = selected_data['Product'].value_counts()
            counts.plot(kind='bar', title=f'Laptop Count for {company}', xlabel='Product', ylabel='Count', color='green', grid=True)
            plt.xticks(rotation=45)
            plt.show()
        else:
            messagebox.showwarning("Warning", "Please select a Company first!")
            
    elif option == 'GPU Usage by Company':
        gpu = filters['Gpu'].get()
        if gpu:
            selected_data = data[data['Gpu'] == gpu]
            counts = selected_data['Company'].value_counts()
            counts.plot(kind='bar', title=f'GPU Usage by Company: {gpu}', xlabel='Company', ylabel='Count', color='brown', grid=True)
            plt.xticks(rotation=45)
            plt.show()
        else:
            messagebox.showwarning("Warning", "Please select a GPU first!")

    elif option == 'Operating System Usage':
        opsys_counts = data['OpSys'].value_counts()
        opsys_counts.plot(kind='barh', title='Operating System Usage', xlabel='Count', ylabel='Operating System', grid=True)
        plt.show()

    elif option == 'Memory Usage in Selected Product':
        product = filters['Product'].get()
        if product:
            selected_data = data[data['Product'] == product]
            counts = selected_data['Memory'].value_counts()
            counts.plot(kind='barh', title=f'Memory Usage in {product}', xlabel='Count', ylabel='Memory', color='yellow', grid=True)
            plt.show()
        else:
            messagebox.showwarning("Warning", "Please select a Product first!")
            
    elif option == 'Product Count by TypeName':
        typename_counts = data['TypeName'].value_counts()
        typename_counts.plot(kind='bar', title='Product Count by TypeName', xlabel='TypeName', ylabel='Count', color='black', grid=True)
        plt.xticks(rotation=45)
        plt.show()
        
chart_options = [
    'Average Price by Company',
    'Laptop Count by Company',
    'Laptop Count by Selected Company',
    'GPU Usage by Company',
    'Operating System Usage',
    'Memory Usage in Selected Product',
    'Product Count by TypeName'
]

chart_var = tk.StringVar()
chart_var.set(chart_options[0])
chart_label = tk.Label(filter_frame, text="Select Chart:", anchor='w')
chart_label.grid(row=row, column=0, sticky='w', padx=5, pady=5)
chart_combobox = ttk.Combobox(filter_frame, textvariable=chart_var, values=chart_options, state="readonly")
chart_combobox.grid(row=row, column=1, padx=5, pady=5)
chart_button = tk.Button(filter_frame, text="Show Chart", command=lambda: show_chart(chart_var.get()))
chart_button.grid(row=row, column=2, padx=5, pady=5)

# Hiển thị bảng kết quả 
columns = list(data.columns)
scroll_y=tk.Scrollbar(table_frame, orient=tk.VERTICAL)
scroll_x=tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

scroll_y.pack(side = tk.RIGHT, fill=tk.Y)
scroll_x.pack(side = tk.BOTTOM, fill= tk.X)

table = ttk.Treeview(table_frame, columns=columns, show="headings",
                     yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

for col in columns:
    table.heading(col, text = col)
    table.column(col, width=120 , anchor= tk.W) # Điều chỉnh chiều rộng cột

table.pack(fill=tk.BOTH , expand=True)

scroll_y.config(command=table.yview)
scroll_x.config(command=table.xview)

# Thêm nút chỉnh sửa thông tin
def edit_laptop_info():
    laptop_id = laptop_id_entry.get().strip()
    col = column_combobox.get().strip()
    new_value = new_value_entry.get().strip()

    if not laptop_id or not col or not new_value:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    try:
        # chuyển đổi dữ liệu theo csv
        if data[col].dtype == 'float64':
            new_value = float(new_value)
        elif data[col].dtype == 'int64':
            new_value = int(new_value)

        # Update data
        data.loc[data['laptop_ID'] == int(laptop_id), col] = new_value

        # Lưu vào CSV
        data.to_csv(file_path, index=False, encoding='ISO-8859-1')

        messagebox.showinfo("Success", "Laptop information updated successfully!")
        update_table(data)  # Refresh table display
    except ValueError:
        messagebox.showerror("Error", f"Invalid data type for column '{col}'. Please enter a valid value.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# tạo giao diện chỉnh sửa thông tin
edit_frame = tk.Frame(app, bd=2, relief=tk.GROOVE, padx=10, pady=10)
edit_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

tk.Label(edit_frame, text="Laptop ID:").grid(row=0, column=0, padx=5, pady=5)
laptop_id_entry = tk.Entry(edit_frame, width=10)
laptop_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(edit_frame, text="Column:").grid(row=0, column=2, padx=5, pady=5)
column_combobox = ttk.Combobox(edit_frame, values=list(data.columns), state="readonly", width=15)
column_combobox.grid(row=0, column=3, padx=5, pady=5)

tk.Label(edit_frame, text="New Value:").grid(row=0, column=4, padx=5, pady=5)
new_value_entry = tk.Entry(edit_frame, width=15)
new_value_entry.grid(row=0, column=5, padx=5, pady=5)

edit_button = tk.Button(edit_frame, text="Update Info", command=edit_laptop_info)
edit_button.grid(row=0, column=6, padx=5, pady=5)

app.mainloop()
