import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import numpy
import time
from employee import EmployeeClass
from supplier import SupplierClass
from category import CategoryClass
from product import ProductClass
from sales import SalesClass
from billing import BillingClass


class DashboardClass:
    def __init__(self, element):
        logo_width = 0
        logo_height = 0
        logo_image = None
        self.new_obj = None
        self.new_win = None
        self.root = element
        self.root.geometry("1375x675")
        self.root.title("iData")
        self.root.config(bg="white")
        self.root.minsize(1375, 675)

        # =============== Title ===============
        # Open and resize the logo image
        try:
            logo_image = Image.open("images/logo.png")
            logo_image = logo_image.resize((100, 100), Image.LANCZOS)
            logo_width, logo_height = logo_image.size
        except FileNotFoundError as e:
            print("Logo image file not found:", e)
        except Exception as e:
            print("Error loading or processing logo image:", e)

        # Create a canvas with the width of the logo
        canvas = Canvas(self.root, bg="#000f49", bd=0, highlightthickness=0, width=logo_width, height=logo_height + 20)
        canvas.pack(fill=BOTH, expand=False)

        # Create PhotoImage object from the logo image
        self.logo = ImageTk.PhotoImage(logo_image)

        # Display the logo image on the canvas
        canvas.create_image(15, 10, anchor=NW, image=self.logo)

        canvas.create_text(235, 60, text="iData", font=("times new roman", 40, "bold"), fill="#FFFFFF")

        # =============== Logout button ===============
        btn_logout = Button(self.root, text="Logout", cursor="hand2", font=("times new roman", 15, "bold"),
                            bg="yellow", fg="#000000", bd=0, command=self.logout)
        btn_logout.place(relx=1, x=-50, y=35, width=135, height=45, anchor=NE)

        # =============== Clock ===============
        self.lbl_clock = Label(self.root, text="Welcome to iData\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=110, relwidth=1, height=40)

        # =============== Left Menu ===============
        left_menu = Frame(self.root, bd=0, relief=RIDGE, bg="#4d636d")
        left_menu.place(x=0, y=150, width=250, relheight=1)

        self.menu_logo = Image.open("images/left_menu_logo.png")
        self.menu_logo = self.menu_logo.resize((200, 200), Image.LANCZOS)
        self.menu_logo = ImageTk.PhotoImage(self.menu_logo)

        lbl_menu_logo = Label(left_menu, image=self.menu_logo, bg="#4d636d")
        lbl_menu_logo.pack(side=TOP, fill=X)

        lbl_menu = Label(left_menu, text="Menu", font=("times new roman", 20, "bold"), bg="#009688", fg="white")
        lbl_menu.pack(side=TOP, fill=X)

        # =============== Left Menu Buttons ===============
        btn_employee = Button(left_menu, text="Employee", cursor="hand2", font=("times new roman", 15, "bold"),
                              bg="#4d636d", fg="white", bd=3, command=self.employee)
        btn_employee.pack(side=TOP, fill=X)

        btn_supplier = Button(left_menu, text="Supplier", cursor="hand2", font=("times new roman", 15, "bold"),
                              bg="#4d636d", fg="white", bd=3, command=self.supplier)
        btn_supplier.pack(side=TOP, fill=X)

        btn_category = Button(left_menu, text="Category", cursor="hand2", font=("times new roman", 15, "bold"),
                              bg="#4d636d", fg="white", bd=3, command=self.category)
        btn_category.pack(side=TOP, fill=X)

        btn_products = Button(left_menu, text="Products", cursor="hand2", font=("times new roman", 15, "bold"),
                              bg="#4d636d", fg="white", bd=3, command=self.product)
        btn_products.pack(side=TOP, fill=X)

        btn_sales = Button(left_menu, text="Sales", cursor="hand2", font=("times new roman", 15, "bold"),
                           bg="#4d636d", fg="white", bd=3, command=self.sales)
        btn_sales.pack(side=TOP, fill=X)

        btn_exit = Button(left_menu, text="Exit", cursor="hand2", font=("times new roman", 15, "bold"),
                          bg="#4d636d", fg="white", bd=3, command=self.exit)
        btn_exit.pack(side=TOP, fill=X)

        # =============== Content ===============
        self.lbl_employee = Label(self.root, text="Total Employees\n 0 ", bd=5, relief=RIDGE,
                                  cursor="hand2", font=("times new roman", 20), bg="#4d636d", fg="white")
        self.lbl_employee.place(x=315, y=200, width=300, height=150)

        self.lbl_supplier = Label(self.root, text="Total Suppliers\n 0 ", bd=5, relief=RIDGE,
                                  cursor="hand2", font=("times new roman", 20), bg="#4d636d", fg="white")
        self.lbl_supplier.place(x=665, y=200, width=300, height=150)

        self.lbl_category = Label(self.root, text="Total Categories\n 0 ", bd=5, relief=RIDGE,
                                  cursor="hand2", font=("times new roman", 20), bg="#4d636d", fg="white")
        self.lbl_category.place(x=1015, y=200, width=300, height=150)

        self.lbl_product = Label(self.root, text="Total Products\n 0 ", bd=5, relief=RIDGE,
                                 cursor="hand2", font=("times new roman", 20), bg="#4d636d", fg="white")
        self.lbl_product.place(x=490, y=405, width=300, height=150)

        self.lbl_sales = Label(self.root, text="Total Sales\n 0 ", bd=5, relief=RIDGE,
                               cursor="hand2", font=("times new roman", 20), bg="#4d636d", fg="white")
        self.lbl_sales.place(x=840, y=405, width=300, height=150)

        # =============== Footer ===============
        lbl_footer = Label(self.root, text="iData\t\temail@example.com", relief=RAISED,
                           font=("times new roman", 15), bg="#4d636d", fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)

        self.update_content()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    def employee(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = EmployeeClass(self.new_win)
        except Exception as e:
            print("Error creating Employee window:", e)

    def supplier(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = SupplierClass(self.new_win)
        except Exception as e:
            print("Error creating Supplier window:", e)

    def category(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = CategoryClass(self.new_win)
        except Exception as e:
            print("Error creating Category window:", e)

    def product(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = ProductClass(self.new_win)
        except Exception as e:
            print("Error creating Category window:", e)

    def sales(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = SalesClass(self.new_win)
        except Exception as e:
            print("Error creating Category window:", e)

    def billing(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = BillingClass(self.new_win)
        except Exception as e:
            print("Error creating Category window:", e)

    def update_content(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            cur.execute("Select * from product")
            product = cur.fetchall()
            self.lbl_product.config(text=f"Total Products\n {str(len(product))}")

            cur.execute("Select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employees\n {str(len(employee))}")

            cur.execute("Select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n {str(len(supplier))}")

            cur.execute("Select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Categories\n {str(len(category))}")
            billings = len(os.listdir("billing/"))
            self.lbl_sales.config(text=f"Total Sales\n {str(billings)}")

            timing = time.strftime("%I:%M:%S")
            date = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to iData\t\t Date: {str(date)}\t\t Time: {str(timing)}")
            self.lbl_clock.after(200, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def exit(self):
        if messagebox.askyesno("Confirm Close", "Are you sure you want to close?", parent=self.root):
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = DashboardClass(root)
    root.mainloop()
