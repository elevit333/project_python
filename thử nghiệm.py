import tkinter as tk
from tkinter import ttk

# Dữ liệu mẫu cho danh sách laptop
laptops = [
    {"hãng": "Dell", "model": "XPS 13", "giá": 1500},
    {"hãng": "HP", "model": "Spectre x360", "giá": 1400},
    {"hãng": "Apple", "model": "MacBook Pro", "giá": 2000},
    {"hãng": "Asus", "model": "ZenBook", "giá": 1300},
    {"hãng": "Lenovo", "model": "ThinkPad X1", "giá": 1600},
]

# Hàm để lọc và hiển thị danh sách laptop
def filter_laptops():
    selected_brand = brand_var.get()
    selected_price = price_var.get()
    
    filtered_laptops = [laptop for laptop in laptops if (selected_brand == "Tất cả" or laptop["hãng"] == selected_brand)]
    
    if selected_price == "Dưới 1500":
        filtered_laptops = [laptop for laptop in filtered_laptops if laptop["giá"] < 1500]
    elif selected_price == "1500 - 2000":
        filtered_laptops = [laptop for laptop in filtered_laptops if 1500 <= laptop["giá"] <= 2000]
    elif selected_price == "Trên 2000":
        filtered_laptops = [laptop for laptop in filtered_laptops if laptop["giá"] > 2000]
    
    # Xóa danh sách cũ
    for i in tree.get_children():
        tree.delete(i)
    
    # Thêm danh sách mới
    for laptop in filtered_laptops:
        tree.insert("", tk.END, values=(laptop["hãng"], laptop["model"], laptop["giá"]))

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Bán Laptop")

# Tạo khung lọc
frame_filter = tk.Frame(root)
frame_filter.pack(pady=10)

# Lọc theo hãng
label_brand = tk.Label(frame_filter, text="Hãng:")
label_brand.grid(row=0, column=0, padx=5)

brand_var = tk.StringVar(value="Tất cả")
brand_combobox = ttk.Combobox(frame_filter, textvariable=brand_var)
brand_combobox['values'] = ("Tất cả", "Dell", "HP", "Apple", "Asus", "Lenovo")
brand_combobox.grid(row=0, column=1, padx=5)

# Lọc theo giá
label_price = tk.Label(frame_filter, text="Giá:")
label_price.grid(row=0, column=2, padx=5)

price_var = tk.StringVar(value="Tất cả")
price_combobox = ttk.Combobox(frame_filter, textvariable=price_var)
price_combobox['values'] = ("Tất cả", "Dưới 1500", "1500 - 2000", "Trên 2000")
price_combobox.grid(row=0, column=3, padx=5)

# Nút lọc
button_filter = tk.Button(frame_filter, text="Lọc", command=filter_laptops)
button_filter.grid(row=0, column=4, padx=5)

# Tạo danh sách hiển thị laptop
tree = ttk.Treeview(root, columns=("Hãng", "Model", "Giá"), show="headings")
tree.heading("Hãng", text="Hãng")
tree.heading("Model", text="Model")
tree.heading("Giá", text="Giá (USD)")

tree.pack(pady=10)

# Chạy vòng lặp chính của giao diện
root.mainloop()
