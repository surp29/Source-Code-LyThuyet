import tkinter as tk
from tkinter import messagebox
import math

# Hàm tính nghiệm phương trình bậc 2: ax^2 + bx + c = 0
def giai_pt_bac2():
    try:
        a = float(entry_a2.get())
        b = float(entry_b2.get())
        c = float(entry_c2.get())
        
        if a == 0:
            messagebox.showerror("Lỗi", "Hệ số a phải khác 0!")
            return
        
        delta = b**2 - 4*a*c
        if delta > 0:
            x1 = (-b + math.sqrt(delta)) / (2*a)
            x2 = (-b - math.sqrt(delta)) / (2*a)
            result = f"Phương trình có 2 nghiệm phân biệt:\n x1 = {x1:.2f}, x2 = {x2:.2f}"
        elif delta == 0:
            x = -b / (2*a)
            result = f"Phương trình có nghiệm kép:\n x = {x:.2f}"
        else:
            result = "Phương trình vô nghiệm."
        
        label_result2.config(text=result, fg="blue")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

# Hàm tính nghiệm phương trình bậc 3: ax^3 + bx^2 + cx + d = 0
def giai_pt_bac3():
    try:
        a = float(entry_a3.get())
        b = float(entry_b3.get())
        c = float(entry_c3.get())
        d = float(entry_d3.get())
        
        if a == 0:
            messagebox.showerror("Lỗi", "Hệ số a phải khác 0!")
            return
        
        # Chuyển đổi phương trình bậc 3 về dạng tổng quát
        f = ((3 * c / a) - (b ** 2 / a ** 2)) / 3
        g = ((2 * b ** 3 / a ** 3) - (9 * b * c / a ** 2) + (27 * d / a)) / 27
        h = (g ** 2 / 4) + (f ** 3 / 27)
        
        if h > 0:
            # Có một nghiệm thực và hai nghiệm phức
            R = -(g / 2) + math.sqrt(h)
            S = math.copysign(1, R) * abs(R) ** (1 / 3)
            T = -(g / 2) - math.sqrt(h)
            U = math.copysign(1, T) * abs(T) ** (1 / 3)
            x1 = S + U - (b / (3 * a))
            result = f"Phương trình có 1 nghiệm thực:\n x1 = {x1:.2f}"
        elif h == 0:
            # Có ba nghiệm thực, trong đó ít nhất hai nghiệm bằng nhau
            if f == 0 and g == 0:
                x1 = -(b / (3 * a))
                result = f"Phương trình có 1 nghiệm bội:\n x1 = x2 = x3 = {x1:.2f}"
            else:
                x1 = 2 * ((-g / 2) ** (1 / 3)) - (b / (3 * a))
                x2 = -(((-g / 2) ** (1 / 3))) - (b / (3 * a))
                result = f"Phương trình có 2 nghiệm:\n x1 = {x1:.2f}, x2 = x3 = {x2:.2f}"
        else:
            # Có ba nghiệm thực phân biệt
            i = math.sqrt((g ** 2 / 4) - h)
            j = i ** (1 / 3)
            k = math.acos(-(g / (2 * i)))
            L = j * -1
            M = math.cos(k / 3)
            N = math.sqrt(3) * math.sin(k / 3)
            P = -(b / (3 * a))
            x1 = 2 * j * math.cos(k / 3) - (b / (3 * a))
            x2 = L * (M + N) + P
            x3 = L * (M - N) + P
            result = f"Phương trình có 3 nghiệm thực:\n x1 = {x1:.2f}, x2 = {x2:.2f}, x3 = {x3:.2f}"
        
        label_result3.config(text=result, fg="green")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

# Khởi tạo giao diện
root = tk.Tk()
root.title("Giải phương trình bậc 2 và bậc 3")
root.configure(bg="#F0F0F0")

# --- Phần phương trình bậc 2 ---
frame_bac2 = tk.Frame(root, bg="#ADD8E6", bd=5, relief=tk.RAISED)
frame_bac2.pack(pady=20, padx=20)

label_title2 = tk.Label(frame_bac2, text="Phương trình bậc 2: ax² + bx + c = 0", font=('Arial', 14, 'bold'), bg="#ADD8E6", fg="#003366")
label_title2.grid(row=0, column=0, columnspan=4, pady=5)

label_a2 = tk.Label(frame_bac2, text="a:", bg="#ADD8E6", font=('Arial', 12))
label_a2.grid(row=1, column=0)
entry_a2 = tk.Entry(frame_bac2, font=('Arial', 12))
entry_a2.grid(row=1, column=1)

label_b2 = tk.Label(frame_bac2, text="b:", bg="#ADD8E6", font=('Arial', 12))
label_b2.grid(row=1, column=2)
entry_b2 = tk.Entry(frame_bac2, font=('Arial', 12))
entry_b2.grid(row=1, column=3)

label_c2 = tk.Label(frame_bac2, text="c:", bg="#ADD8E6", font=('Arial', 12))
label_c2.grid(row=2, column=0)
entry_c2 = tk.Entry(frame_bac2, font=('Arial', 12))
entry_c2.grid(row=2, column=1)

btn_giai2 = tk.Button(frame_bac2, text="Giải", font=('Arial', 12, 'bold'), bg="#FF9933", fg="white", command=giai_pt_bac2)
btn_giai2.grid(row=2, column=2, columnspan=2, pady=10)

label_result2 = tk.Label(frame_bac2, text="", font=('Arial', 12), bg="#ADD8E6")
label_result2.grid(row=3, column=0, columnspan=4)

# --- Phần phương trình bậc 3 ---
frame_bac3 = tk.Frame(root, bg="#FFDEAD", bd=5, relief=tk.RAISED)
frame_bac3.pack(pady=20, padx=20)

label_title3 = tk.Label(frame_bac3, text="Phương trình bậc 3: ax³ + bx² + cx + d = 0", font=('Arial', 14, 'bold'), bg="#FFDEAD", fg="#8B4513")
label_title3.grid(row=0, column=0, columnspan=4, pady=5)

label_a3 = tk.Label(frame_bac3, text="a:", bg="#FFDEAD", font=('Arial', 12))
label_a3.grid(row=1, column=0)
entry_a3 = tk.Entry(frame_bac3, font=('Arial', 12))
entry_a3.grid(row=1, column=1)

label_b3 = tk.Label(frame_bac3, text="b:", bg="#FFDEAD", font=('Arial', 12))
label_b3.grid(row=1, column=2)
entry_b3 = tk.Entry(frame_bac3, font=('Arial', 12))
entry_b3.grid(row=1, column=3)

label_c3 = tk.Label(frame_bac3, text="c:", bg="#FFDEAD", font=('Arial', 12))
label_c3.grid(row=2, column=0)
entry_c3 = tk.Entry(frame_bac3, font=('Arial', 12))
entry_c3.grid(row=2, column=1)

label_d3 = tk.Label(frame_bac3, text="d:", bg="#FFDEAD", font=('Arial', 12))
label_d3.grid(row=2, column=2)
entry_d3 = tk.Entry(frame_bac3, font=('Arial', 12))
entry_d3.grid(row=2, column=3)

btn_giai3 = tk.Button(frame_bac3, text="Giải", font=('Arial', 12, 'bold'), bg="#8B4513", fg="white", command=giai_pt_bac3)
btn_giai3.grid(row=3, column=0, columnspan=4, pady=10)

label_result3 = tk.Label(frame_bac3, text="", font=('Arial', 12), bg="#FFDEAD")
label_result3.grid(row=4, column=0, columnspan=4)

# Chạy ứng dụng
root.mainloop()
