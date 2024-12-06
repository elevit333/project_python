from tkinter import *
#Trích dataset tại đây
from json import*
latops = []
with open ("laptop_price.csv", mode='r', encoding='utf-8'):


#Tạo một cửa sổ mới
window = Tk()

#Thêm tiêu đề cho cửa sổ
window.title('TƯ VẤN LAPTOP')

#Đặt kích thước của cửa sổ
window.geometry('1440x900')

#Tao khung lọc
frame_filter = Frame(window)
frame_filter.pack(pady=10)

#hiển thị lựa chọn laptop theo hãng(hình ảnh logo hãng)
label_brand = Label(frame_filter,
                       text="Hãng:")
label_brand.grid(row=0,
                 column=0,
                 padx=5)

window.mainloop()
