import sqlite3
import time
from tkinter import *
from tkinter import ttk, messagebox
import os
import tempfile
from PIL import Image, ImageTk


class BillingClass:
    def __init__(self, element):
        self.invoice = None
        self.net_pay = None
        self.bill_amount = None

        self.new_obj = None
        self.new_win = None
        self.root = element
        self.root.geometry("1375x735")
        self.root.title("iData")
        self.root.config(bg="white")
        self.root.minsize(1375, 735)
        self.root.maxsize(1375, 735)
        logo_image = None
        logo_width = 0
        logo_height = 0

        # =============== Title ===============
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

        # =============== Product Field ===============
        # =============== Variables ===============
        self.var_search = StringVar()
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        # =============== Content ===============
        product_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_frame.place(x=20, y=165, width=430, height=550)

        product_title = Label(product_frame, text="All Products", font=("times new roman", 20, "bold"), bg="#4d636d",
                              fg="white")
        product_title.place(x=0, y=0, relwidth=1)

        product_frame_2 = Frame(product_frame, bd=2, relief=RIDGE, bg="white")
        product_frame_2.place(x=3, y=40, width=400, height=90)

        lbl_search = Label(product_frame_2, text="Search By", font=("times new roman", 15, "bold"), bg="white")
        lbl_search.place(x=10, y=10)

        lbl_name = Label(product_frame_2, text="Name", font=("times new roman", 15, "bold"), bg="white")
        lbl_name.place(x=10, y=50)

        txt_name = Entry(product_frame_2, textvariable=self.var_search, font=("times new roman", 15, "bold"),
                         bg="lightyellow", fg="black", relief=GROOVE)
        txt_name.place(x=70, y=50, width=180)

        btn_search = Button(product_frame_2, text="Search", cursor="hand2", font=("times new roman", 15, "bold"),
                            bg="#2196f3", fg="white", bd=2, command=self.search)
        btn_search.place(x=260, y=48, width=100, height=30)

        btn_show_all = Button(product_frame_2, text="Show All", cursor="hand2", font=("times new roman", 15, "bold"),
                              bg="#2196f3", fg="white", bd=2, command=self.show)
        btn_show_all.place(x=260, y=10, width=100, height=30)

        # =============== Product Table ===============
        product_frame_3 = Frame(product_frame, bd=3, relief=RIDGE)
        product_frame_3.place(x=3, y=135, width=400, height=385)

        scroll_y = Scrollbar(product_frame_3, orient=VERTICAL)
        scroll_x = Scrollbar(product_frame_3, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(product_frame_3, columns=("pid", "name", "price",
                                                                    "quantity", "status"), yscrollcommand=scroll_y.set,
                                          xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.product_table.xview)
        scroll_y.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="Product ID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("quantity", text="Quantity")
        self.product_table.heading("status", text="Status")

        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=50)
        self.product_table.column("name", width=50)
        self.product_table.column("price", width=50)
        self.product_table.column("quantity", width=50)
        self.product_table.column("status", width=50)

        self.product_table.pack(fill=BOTH, expand=1)

        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        lbl_note = Label(product_frame, text="Note: Enter 0 quantity to remove product from the cart",
                         font=("times new roman", 13), anchor="w", bg="white")
        lbl_note.place(x=5, y=520)

        # =============== Customer Field ===============
        # =============== Variables ===============
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()
        self.var_cal_input = StringVar()
        self.cart_list = []
        self.chk_print = 0

        # =============== Content ===============
        customer_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        customer_frame.place(x=455, y=165, width=530, height=550)

        cal_cart_frame = Frame(customer_frame, bd=2, relief=RIDGE, bg="white")
        cal_cart_frame.place(x=5, y=90, width=515, height=320)

        customer_title = Label(customer_frame, text="Customer Details", font=("times new roman", 20, "bold"),
                               bg="#4d636d", fg="white")
        customer_title.place(x=0, y=0, relwidth=1)

        lbl_name = Label(customer_frame, text="Name", font=("times new roman", 15, "bold"), bg="white")
        lbl_name.place(x=5, y=50)

        txt_name = Entry(customer_frame, textvariable=self.var_cname, font=("times new roman", 15),
                         bg="lightyellow", fg="black", relief=GROOVE)
        txt_name.place(x=65, y=50, width=200)

        lbl_contact = Label(customer_frame, text="Contact", font=("times new roman", 15, "bold"), bg="white")
        lbl_contact.place(x=275, y=50)

        txt_contact = Entry(customer_frame, textvariable=self.var_contact, font=("times new roman", 15),
                            bg="lightyellow", fg="black", bd=1, relief=GROOVE)
        txt_contact.place(x=355, y=50, width=130)

        # =============== Cart ===============
        cart_frame = Frame(cal_cart_frame, bd=3, relief=RIDGE)
        cart_frame.place(x=260, y=5, width=245, height=305)

        self.cart_title = Label(cart_frame, text="Cart \t Total products: 0", font=("times new roman", 12, "bold"),
                                bg="#4d636d", fg="white")
        self.cart_title.pack(side=TOP, fill=X)

        scroll_y = Scrollbar(cart_frame, orient=VERTICAL)
        scroll_x = Scrollbar(cart_frame, orient=HORIZONTAL)

        self.cart_table = ttk.Treeview(cart_frame, columns=("pid", "name", "price", "quantity"),
                                       yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.cart_table.xview)
        scroll_y.config(command=self.cart_table.yview)

        self.cart_table.heading("pid", text="PID")
        self.cart_table.heading("name", text="Name")
        self.cart_table.heading("price", text="Price")
        self.cart_table.heading("quantity", text="Qty")

        self.cart_table["show"] = "headings"

        self.cart_table.column("pid", width=50)
        self.cart_table.column("name", width=50)
        self.cart_table.column("price", width=50)
        self.cart_table.column("quantity", width=50)

        self.cart_table.pack(fill=BOTH, expand=1)
        self.cart_table.bind("<ButtonRelease-1>", self.get_cart_data)

        add_cart_widget_frame = Frame(customer_frame, bd=2, relief=RIDGE, bg="white")
        add_cart_widget_frame.place(x=5, y=415, width=515, height=125)

        lbl_pname = Label(add_cart_widget_frame, text="Product Name", font=("times new roman", 15, "bold"), bg="white")
        lbl_pname.place(x=20, y=5)

        txt_pname = Entry(add_cart_widget_frame, textvariable=self.var_pname, font=("times new roman", 15),
                          bg="lightyellow", fg="black", bd=1, relief=GROOVE, state="disabled", cursor="arrow")
        txt_pname.place(x=20, y=35, width=160)

        lbl_price = Label(add_cart_widget_frame, text="Price", font=("times new roman", 15, "bold"), bg="white")
        lbl_price.place(x=200, y=5)

        txt_price = Entry(add_cart_widget_frame, textvariable=self.var_price, font=("times new roman", 15),
                          bg="lightyellow", fg="black", bd=1, relief=GROOVE, state="disabled", cursor="arrow")
        txt_price.place(x=200, y=35, width=120)

        lbl_qty = Label(add_cart_widget_frame, text="Quantity", font=("times new roman", 15, "bold"), bg="white")
        lbl_qty.place(x=340, y=5)

        txt_qty = Entry(add_cart_widget_frame, textvariable=self.var_qty, font=("times new roman", 15),
                        bg="lightyellow", fg="black", bd=1, relief=GROOVE)
        txt_qty.place(x=340, y=35, width=120)

        self.lbl_in_stock = Label(add_cart_widget_frame, text="In Stock: 0", font=("times new roman", 15, "bold"),
                                  bg="white", fg="green")
        self.lbl_in_stock.place(x=340, y=70)

        btn_add_to_cart = Button(add_cart_widget_frame, text="Add | Update", font=("times new roman", 15, "bold"),
                                 bg="#2196f3", fg="white", cursor="hand2", command=self.add_update_cart)
        btn_add_to_cart.place(x=20, y=70, width=160, height=30)

        btn_clear_cart = Button(add_cart_widget_frame, text="Clear", font=("times new roman", 15, "bold"),
                                bg="gray", fg="white", cursor="hand2", command=self.clear_cart)
        btn_clear_cart.place(x=200, y=70, width=120, height=30)

        # ===================== Calculator =====================
        # =============== Content ===============
        cal_frame = Frame(cal_cart_frame, bd=6, relief=RIDGE)
        cal_frame.place(x=5, y=5, width=250, height=305)

        self.txt_cal_input = Entry(cal_frame, font=("times new roman", 15), textvariable=self.var_cal_input,
                                   bg="lightyellow", fg="black", bd=10, relief=GROOVE, state="readonly")
        self.txt_cal_input.grid(row=0, columnspan=4, padx=0, pady=2)

        btn_7 = Button(cal_frame, text="7", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=lambda: self.get_input("7"))
        btn_7.grid(row=1, column=0)

        btn_8 = Button(cal_frame, text="8", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=lambda: self.get_input("8"))
        btn_8.grid(row=1, column=1)

        btn_9 = Button(cal_frame, text="9", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=lambda: self.get_input("9"))
        btn_9.grid(row=1, column=2)

        btn_add = Button(cal_frame, text="+", font=("times new roman", 15), bg="orange", fg="black", bd=5, width=4,
                         cursor="hand2", pady=9, command=lambda: self.get_input("+"))
        btn_add.grid(row=1, column=3)

        btn_4 = Button(cal_frame, text="4", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=lambda: self.get_input("4"))
        btn_4.grid(row=2, column=0)

        btn_5 = Button(cal_frame, text="5", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=lambda: self.get_input("5"))
        btn_5.grid(row=2, column=1)

        btn_6 = Button(cal_frame, text="6", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=lambda: self.get_input("6"))
        btn_6.grid(row=2, column=2)

        btn_sub = Button(cal_frame, text="-", font=("times new roman", 15), bg="orange", fg="black", bd=5, width=4,
                         cursor="hand2", pady=9, command=lambda: self.get_input("-"))
        btn_sub.grid(row=2, column=3)

        btn_1 = Button(cal_frame, text="1", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=lambda: self.get_input("1"))
        btn_1.grid(row=3, column=0)

        btn_2 = Button(cal_frame, text="2", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=lambda: self.get_input("2"))
        btn_2.grid(row=3, column=1)

        btn_3 = Button(cal_frame, text="3", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=lambda: self.get_input("3"))
        btn_3.grid(row=3, column=2)

        btn_mult = Button(cal_frame, text="*", font=("times new roman", 15), bg="orange", fg="black", bd=5, width=4,
                          cursor="hand2", pady=9, command=lambda: self.get_input("*"))
        btn_mult.grid(row=3, column=3)

        btn_0 = Button(cal_frame, text="0", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=lambda: self.get_input("0"))
        btn_0.grid(row=4, column=0)

        btn_c = Button(cal_frame, text="C", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                       cursor="hand2", pady=9, command=self.clear_cal_input)
        btn_c.grid(row=4, column=1)

        btn_div = Button(cal_frame, text="/", font=("times new roman", 15), bg="lightgray", fg="black", bd=5, width=4,
                         cursor="hand2", pady=9, command=lambda: self.get_input("/"))
        btn_div.grid(row=4, column=2)

        btn_eq = Button(cal_frame, text="=", font=("times new roman", 15), bg="orange", fg="black", bd=5, width=4,
                        cursor="hand2", pady=9, command=self.perform_operation)
        btn_eq.grid(row=4, column=3)

        # ================== Billing Field ==================
        # ================== Content ==================
        bill_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_frame.place(x=990, y=165, width=365, height=380)

        billing_title = Label(bill_frame, text="Customer Bill", font=("times new roman", 20, "bold"),
                              bg="#4d636d", fg="white")
        billing_title.pack(side=TOP, fill=X)

        scroll_y_bill = Scrollbar(bill_frame, orient=VERTICAL)
        scroll_y_bill.pack(side=RIGHT, fill=Y)
        self.txt_bill_area = Text(bill_frame, yscrollcommand=scroll_y_bill.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scroll_y_bill.config(command=self.txt_bill_area.yview)

        # ================== Menu ==================
        bill_menu_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_menu_frame.place(x=990, y=550, width=365, height=165)

        self.lbl_amount = Label(bill_menu_frame, text="Total Amount\n0", font=("times new roman", 15, "bold"),
                                bg="#4d636d", fg="white")
        self.lbl_amount.place(x=5, y=5, width=130, height=80)

        self.discount = Label(bill_menu_frame, text="Discount\n5%", font=("times new roman", 15, "bold"),
                              bg="#4d636d", fg="white")
        self.discount.place(x=140, y=5, width=80, height=80)

        self.lbl_net_pay = Label(bill_menu_frame, text="Pay\n0", font=("times new roman", 15, "bold"),
                                 bg="#4d636d", fg="white")
        self.lbl_net_pay.place(x=225, y=5, width=130, height=80)

        self.btn_print = Button(bill_menu_frame, text="Print", font=("times new roman", 15, "bold"),
                                bg="#4d636d", fg="white", bd=3, command=self.print_bill)
        self.btn_print.place(x=5, y=90, width=130, height=70)

        self.clear_all = Button(bill_menu_frame, text="Clear\nall", font=("times new roman", 15, "bold"),
                                bg="#4d636d", fg="white", bd=3, command=self.clear_all)
        self.clear_all.place(x=140, y=90, width=80, height=70)

        self.generate = Button(bill_menu_frame, text="Generate", font=("times new roman", 15, "bold"),
                               bg="#4d636d", fg="white", bd=3, command=self.generate_bill)
        self.generate.place(x=225, y=90, width=130, height=70)

        self.show()
        self.update_date_time()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ================== Functions ==================
    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.lbl_in_stock.config(text=f"In Stock")
        self.var_stock.set("")
        self.var_qty.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set("")
        self.var_contact.set("")
        self.txt_bill_area.delete("1.0", END)
        self.cart_title.config(text=f"Cart \t Total products: 0")
        self.var_search.set("")
        self.chk_print = 0
        self.clear_cart()
        self.show_cart()

    def get_input(self, num):
        num = self.txt_cal_input.get() + str(num)
        self.var_cal_input.set(num)

    def perform_operation(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def clear_cal_input(self):
        self.var_cal_input.set("")

    def on_closing(self):
        if messagebox.askyesno("Confirm Close", "Are you sure you want to close?", parent=self.root):
            self.root.destroy()

    def show(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            cur.execute("Select pid, name, price, quantity, status from product where status = 'Available'")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def search(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search text required", parent=self.root)
            else:
                cur.execute("Select pid, name, price, quantity, status from product where name LIKE"
                            "'%" + self.var_search.get() + "%' and status = 'Available'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def get_data(self, event):
        f = self.product_table.focus()
        content = self.product_table.item(f)
        row = content["values"]
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.lbl_in_stock.config(text=f"In Stock: {str(row[3])}")
            self.var_stock.set(row[3])
            self.var_qty.set("1")

            if row and len(row) >= 1:
                self.var_pname.set(row[1])
            else:
                self.var_pname.set("")

            if row and len(row) >= 2:
                self.var_price.set(row[2])
            else:
                self.var_price.set("")

            if row and len(row) >= 3:
                self.var_stock.set(row[3])
            else:
                self.var_stock.set("")

    def get_cart_data(self, event):
        f = self.cart_table.focus()
        content = self.cart_table.item(f)
        row = content["values"]
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.lbl_in_stock.config(text=f"In Stock: {str(row[4])}")
            self.var_stock.set(row[4])
            self.var_qty.set(row[3])

            if row and len(row) >= 1:
                self.var_pname.set(row[1])
            else:
                self.var_pname.set("")

            if row and len(row) >= 2:
                self.var_price.set(row[2])
            else:
                self.var_price.set("")

            if row and len(row) >= 3:
                self.var_qty.set(row[3])
            else:
                self.var_qty.set("")

            if row and len(row) >= 4:
                self.var_stock.set(row[4])
            else:
                self.var_stock.set("")

    def add_update_cart(self):
        price_cal = 0
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select a product from the list", parent=self.root)
        elif self.var_qty.get() == "":
            messagebox.showerror("Error", "Quantity is required", parent=self.root)
        elif self.var_qty.get() > self.var_stock.get():
            messagebox.showerror("Error", "Quantity not available", parent=self.root)
        else:
            # price_cal = int(int(self.var_qty.get()) * float(self.var_price.get())) + price_cal
            # price_cal = float(price_cal)
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]

            present = False
            index = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = True
                    break
                index += 1
            if present:
                op = messagebox.askyesno("Confirm", "Product already present in the cart, do you want "
                                                    "to update?", parent=self.root)
                if op is True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index)
                    else:
                        self.cart_list[index][3] = self.var_qty.get()
                        self.cart_list[index][2] = price_cal
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amount = 0
        self.net_pay = 0
        for row in self.cart_list:
            self.bill_amount += float(row[2]) * int(row[3])

        self.discount = self.bill_amount * 0.05
        self.net_pay = self.bill_amount - self.discount
        self.lbl_amount.config(text=f"Total Amount\n{str(self.bill_amount)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cart_title.config(text=f"Cart \t Total products: {str(len(self.cart_list))}")

    def show_cart(self):
        try:
            self.cart_table.delete(*self.cart_table.get_children())
            for row in self.cart_list:
                self.cart_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get() == "" or self.var_contact.get() == "":
            messagebox.showerror("Error", "Customer details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "No product selected", parent=self.root)
        else:
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()

            fp = open(f"billing/{str(self.invoice)}.txt", "w")
            fp.write(self.txt_bill_area.get("1.0", END))
            fp.close()
            messagebox.showinfo("Success", f"Bill no. {str(self.invoice)} generated successfully",
                                parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
    \t\tXYZ-Inventory\n    Phone No. 98725***** , Delhi-125001\n {str("=" * 40)}
    Customer Name: {self.var_cname.get()}
    Ph no. :{self.var_contact.get()}
    Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}\n {str("=" * 40)}
    Product Name\t\t\tQTY\tPrice\n {str("=" * 40)}
            '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp = f'''\n {str("=" * 40)}
    Bill Amount\t\t\t\t{self.bill_amount}
    Discount\t\t\t\t{self.discount}
    Net Pay\t\t\t\t{self.net_pay}\n {str("=" * 40)}\n
            '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        status = ""
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            for row in self.cart_list:
                # pid,name,price,qty,stock
                pid = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = "Out of stock"
                if int(row[3]) != int(row[4]):
                    status = "Available"
                price = float(row[2]) * int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END, "\n    " + name + "\t\t\t" + row[3] + "\t" + price)
                cur.execute("Update product set quantity = ?, status = ? where pid = ?", (
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def update_date_time(self):
        timing = time.strftime("%I:%M:%S")
        date = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to iData\t\t Date: {str(date)}\t\t Time: {str(timing)}")
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo("Success", f"Bill no. {str(self.invoice)} printed successfully",
                                parent=self.root)
            new_file = tempfile.mktemp(".txt")
            open(new_file, "w").write(self.txt_bill_area.get("1.0", END))
            os.startfile(new_file, "print")
        else:
            messagebox.showerror("Error", "Please generate bill first", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = BillingClass(root)
    root.mainloop()
