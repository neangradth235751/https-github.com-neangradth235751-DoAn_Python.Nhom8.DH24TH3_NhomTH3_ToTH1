import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Kết nối CSDL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="qlvatlieu"
    )

# Căn giữa cửa sổ
def center_window(win, w=500, h=400):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# Cửa sổ chính
root = tk.Tk()
root.title("Quản lý cửa hàng vật liệu xây dựng")
root.geometry("750x750")

# Tiêu đề
tk.Label(root, text="PHẦN MỀM QUẢN LÝ CỬA HÀNG VẬT LIỆU XÂY DỰNG", font=("Arial", 18, "bold")).pack(pady=10)

tk.Label(root, text="QUẢN LÝ VẬT LIỆU", font=("Arial", 16, "bold")).pack(pady=10)

# Frame thông tin nhập liệu
frame_input = tk.Frame(root)
frame_input.pack(pady=5, padx=10, fill="x")

tk.Label(frame_input, text="Mã VL").grid(row=0, column=0, padx=5, pady=5)
entry_mavl = tk.Entry(frame_input, width=15)
entry_mavl.grid(row=0, column=1)

tk.Label(frame_input, text="Tên VL").grid(row=0, column=2, padx=5, pady=5)
entry_tenvl = tk.Entry(frame_input, width=25)
entry_tenvl.grid(row=0, column=3)

# Bảng danh sách vật liệu
columns = ("mavl", "tenvl")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
tree.heading("mavl", text="Mã VL")
tree.heading("tenvl", text="Tên Vật liệu")
tree.pack(padx=10, pady=10, fill="x")

# Chức năng
def clear_input():
    entry_mavl.delete(0, tk.END)
    entry_tenvl.delete(0, tk.END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM qlvatlieu")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

def them_vl():
    mavl = entry_mavl.get()
    tenvl = entry_tenvl.get()
    if not mavl or not tenvl:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin")
        return
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO qlvatlieu VALUES (%s, %s)", (mavl, tenvl))
        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        conn.close()

def xoa_vl():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Chọn vật liệu để xóa")
        return
    mavl = tree.item(selected)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM qlvatlieu WHERE mavl=%s", (mavl,))
    conn.commit()
    conn.close()
    load_data()

def sua_vl():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Chọn vật liệu để sửa")
        return
    values = tree.item(selected)["values"]
    entry_mavl.delete(0, tk.END)
    entry_mavl.insert(0, values[0])
    entry_tenvl.delete(0, tk.END)
    entry_tenvl.insert(0, values[1])

def luu_vl():
    mavl = entry_mavl.get()
    tenvl = entry_tenvl.get()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE qlvatlieu SET tenvl=%s WHERE mavl=%s", (tenvl, mavl))
    conn.commit()
    conn.close()
    load_data()
    clear_input()

# Nút chức năng
frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)
tk.Button(frame_btn, text="Thêm", width=10, command=them_vl).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Lưu", width=10, command=luu_vl).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Sửa", width=10, command=sua_vl).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Xóa", width=10, command=xoa_vl).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=4, padx=5)
tk.Button(frame_btn, text="Thoát", width=10, command=root.quit).grid(row=0, column=5, padx=5)

load_data()
root.mainloop()
