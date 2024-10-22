import psycopg2
from psycopg2 import Error
import tkinter as tk
from tkinter import messagebox

# Hàm kết nối tới cơ sở dữ liệu
def connect_to_database(user, password, dbname, host, port):
    try:
        connection = psycopg2.connect(
            dbname=dbname, 
            user=user, 
            password=password,  
            host=host,  
            port=port  
        )
        print("Kết nối cơ sở dữ liệu thành công!")
        return connection
    except (Exception, Error) as error:
        messagebox.showerror("Lỗi", f"Lỗi khi kết nối tới PostgreSQL: {error}")
        return None

# Class GUI cho ứng dụng quản lý sách
class BookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng quản lý sách")

        self.connection = None  # Kết nối cơ sở dữ liệu sẽ được thiết lập sau khi đăng nhập

        # Tạo giao diện đăng nhập
        self.create_login_widgets()

    def create_login_widgets(self):
        # Giao diện đăng nhập vào cơ sở dữ liệu
        tk.Label(self.root, text="Tên đăng nhập:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Mật khẩu:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Tên cơ sở dữ liệu:").grid(row=2, column=0, padx=10, pady=10)
        self.dbname_entry = tk.Entry(self.root)
        self.dbname_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Host:").grid(row=3, column=0, padx=10, pady=10)
        self.host_entry = tk.Entry(self.root)
        self.host_entry.grid(row=3, column=1, padx=10, pady=10)
        self.host_entry.insert(0, 'localhost')  # Mặc định là localhost

        tk.Label(self.root, text="Port:").grid(row=4, column=0, padx=10, pady=10)
        self.port_entry = tk.Entry(self.root)
        self.port_entry.grid(row=4, column=1, padx=10, pady=10)
        self.port_entry.insert(0, '5432')  # Mặc định là 5432

        tk.Button(self.root, text="Đăng nhập", command=self.login_to_database).grid(row=5, columnspan=2, pady=10)

    def login_to_database(self):
        # Thông tin đăng nhập
        username = self.username_entry.get()
        password = self.password_entry.get()
        dbname = self.dbname_entry.get()
        host = self.host_entry.get()
        port = self.port_entry.get()

        # Kết nối đến database
        self.connection = connect_to_database(username, password, dbname, host, port)

        if self.connection:
            # Nếu đăng nhập thành công, chuyển sang giao diện quản lý sách
            self.create_book_widgets()

    def create_book_widgets(self):
        # Xóa các widget cũ (giao diện đăng nhập)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Giao diện tìm kiếm sách
        tk.Label(self.root, text="Tìm kiếm sách:").grid(row=0, column=0, padx=10, pady=10)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Tìm kiếm", command=self.search_book).grid(row=0, column=2, padx=10, pady=10)

        # Giao diện thêm sách mới
        tk.Label(self.root, text="Tiêu đề:").grid(row=1, column=0, padx=10, pady=10)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Tác giả:").grid(row=2, column=0, padx=10, pady=10)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="ISBN:").grid(row=3, column=0, padx=10, pady=10)
        self.isbn_entry = tk.Entry(self.root)
        self.isbn_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Năm xuất bản:").grid(row=4, column=0, padx=10, pady=10)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Số lượng:").grid(row=5, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=5, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Thêm sách", command=self.add_book).grid(row=6, column=1, padx=10, pady=10)

        # Text box hiển thị kết quả tìm kiếm
        self.result_box = tk.Text(self.root, height=10, width=50)
        self.result_box.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    def search_book(self):
        keyword = self.search_entry.get()
        if not keyword:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm.")
            return
        
        cursor = self.connection.cursor()
        query = "SELECT * FROM books WHERE title ILIKE %s OR author ILIKE %s"
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        books = cursor.fetchall()
        
        self.result_box.delete(1.0, tk.END)
        if books:
            for book in books:
                self.result_box.insert(tk.END, f"ID: {book[0]}, Tiêu đề: {book[1]}, Tác giả: {book[2]}, ISBN: {book[3]}\n")
        else:
            self.result_box.insert(tk.END, "Không tìm thấy sách phù hợp.\n")
        cursor.close()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        year = self.year_entry.get()
        quantity = self.quantity_entry.get()

        if not (title and author and isbn and year and quantity):
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin sách.")
            return

        try:
            year = int(year)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Lỗi", "Năm xuất bản và số lượng phải là số nguyên.")
            return

        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO books (title, author, isbn, published_year, quantity) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (title, author, isbn, year, quantity))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Sách đã được thêm thành công!")
            self.clear_entries()
        except (Exception, psycopg2.Error) as error:
            self.connection.rollback()  # Rollback trong trường hợp lỗi
            messagebox.showerror("Lỗi", f"Không thể thêm sách: {error}")
        finally:
            cursor.close()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()