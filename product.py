import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


def reindex_primary_keys(table_name):
    con = sqlite3.connect(database=r'idata.db')
    cur = con.cursor()

    cur.execute(f"SELECT rowid FROM {table_name} ORDER BY rowid")
    existing_ids = [row[0] for row in cur.fetchall()]

    for index, rowid in enumerate(existing_ids, start=1):
        cur.execute(f"UPDATE {table_name} SET rowid=? WHERE rowid=?", (index, rowid))
        con.commit()

    con.close()


class ProductClass:
    def __init__(self, element):
        self.root = element
        self.root.geometry("1100x500")
        self.root.title("Products")
        self.root.config(bg="white")
        self.root.minsize(1100, 500)
        self.root.focus_force()

        # =============== Variables ===============
        self.var_search_txt = StringVar()
        self.var_search_by = StringVar()

        self.supp_list = []
        self.cat_list = []
        self.var_status = StringVar()
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_supp = StringVar()

        self.fetch_cat_supp()

        # =============== Frame ===============
        product_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        product_frame.place(x=10, y=10, width=450, height=480)

        # =============== Title ===============
        Label(product_frame, text="Product Details", font=("times new roman", 20, "bold"), bg="#0f4d7d",
              fg="white").pack(side=TOP, fill=X)

        # =============== Search Frame ===============
        search_frame = LabelFrame(self.root, text="Search Product", font=("times new roman", 15, "bold"), bd=2,
                                  relief=RIDGE, bg="white")
        search_frame.place(x=480, y=10, width=600, height=80)

        # =============== Search Field ===============
        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_search_by, font=("times new roman", 13, "bold"),
                                  state="readonly", justify=CENTER, values=("Select", "Category", "Supplier", "Name"))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(search_frame, textvariable=self.var_search_txt, font=("times new roman", 13, "bold"),
                           bg="lightyellow")
        txt_search.place(x=200, y=11, width=220)

        btn_search = Button(search_frame, bg="#4caf50", text="Search", cursor="hand2", command=self.search,
                            font=("times new roman", 13, "bold"))
        btn_search.place(x=430, y=7, width=150, height=30)

        # =============== Buttons ===============
        btn_add = Button(product_frame, text="Add", font=("times new roman", 15, "bold"), bg="#2196f3",
                         fg="white", cursor="hand2", command=self.add)
        btn_add.place(x=7, y=400, width=100, height=40)

        btn_update = Button(product_frame, text="Update", font=("times new roman", 15, "bold"), bg="#4caf50",
                            fg="white", cursor="hand2", command=self.update)
        btn_update.place(x=117, y=400, width=100, height=40)

        btn_delete = Button(product_frame, text="Delete", font=("times new roman", 15, "bold"), bg="#f44336",
                            fg="white", cursor="hand2", command=self.delete)
        btn_delete.place(x=227, y=400, width=100, height=40)

        btn_clear = Button(product_frame, text="Clear", font=("times new roman", 15, "bold"), bg="#607d8b",
                           fg="white", cursor="hand2", command=self.clear)
        btn_clear.place(x=337, y=400, width=100, height=40)

        # =============== Product Details ===============
        # =============== Column 1 ===============
        lbl_category = Label(product_frame, text="Category", font=("times new roman", 15, "bold"), bg="white")
        lbl_category.place(x=30, y=60)

        lbl_supplier = Label(product_frame, text="Supplier", font=("times new roman", 15, "bold"), bg="white")
        lbl_supplier.place(x=30, y=110)

        lbl_name = Label(product_frame, text="Name", font=("times new roman", 15, "bold"), bg="white")
        lbl_name.place(x=30, y=160)

        lbl_price = Label(product_frame, text="Price", font=("times new roman", 15, "bold"), bg="white")
        lbl_price.place(x=30, y=210)

        lbl_quantity = Label(product_frame, text="Quantity", font=("times new roman", 15, "bold"), bg="white")
        lbl_quantity.place(x=30, y=260)

        lbl_status = Label(product_frame, text="Status", font=("times new roman", 15, "bold"), bg="white")
        lbl_status.place(x=30, y=310)

        # =============== Column 2 ===============
        cmb_cat = ttk.Combobox(product_frame, textvariable=self.var_cat, font=("times new roman", 15),
                               values=self.cat_list, state="readonly", justify=CENTER)
        cmb_cat.place(x=180, y=60, width=200)
        cmb_cat.current(0)

        cmb_supp = ttk.Combobox(product_frame, textvariable=self.var_supp, font=("times new roman", 15),
                                values=self.supp_list, state="readonly", justify=CENTER)
        cmb_supp.place(x=180, y=110, width=200)
        cmb_supp.current(0)

        cmb_status = ttk.Combobox(product_frame, textvariable=self.var_status, font=("times new roman", 15),
                                  values=("Select", "Available", "Out of stock"), state="readonly", justify=CENTER)
        cmb_status.place(x=180, y=310, width=200)
        cmb_status.current(0)

        txt_name = Entry(product_frame, textvariable=self.var_name, font=("times new roman", 15),
                         bg="lightyellow")
        txt_name.place(x=180, y=160, width=250)

        txt_price = Entry(product_frame, textvariable=self.var_price, font=("times new roman", 15), bg="lightyellow")
        txt_price.place(x=180, y=210, width=250)

        txt_quantity = Entry(product_frame, textvariable=self.var_qty, font=("times new roman", 15),
                             bg="lightyellow")
        txt_quantity.place(x=180, y=260, width=250)

        # =============== Table ===============
        table_frame = Frame(self.root, bd=3, relief=RIDGE)
        table_frame.place(x=480, y=100, width=600, height=390)

        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(table_frame, columns=("pid", "category", "supplier", "name", "price",
                                          "quantity", "status"), yscrollcommand=scroll_y.set,
                                          xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.product_table.xview)
        scroll_y.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="Product ID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("supplier", text="supplier")
        self.product_table.heading("category", text="Category")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("quantity", text="Quantity")
        self.product_table.heading("status", text="Status")

        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=50)
        self.product_table.column("name", width=50)
        self.product_table.column("supplier", width=50)
        self.product_table.column("category", width=50)
        self.product_table.column("price", width=50)
        self.product_table.column("quantity", width=50)
        self.product_table.column("status", width=50)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # =============== Functions ===============
    def fetch_cat_supp(self):
        self.cat_list.append("Empty")
        self.supp_list.append("Empty")
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            cur.execute("select name from category")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for row in cat:
                    self.cat_list.append(row[0])
            cur.execute("select name from supplier")
            supp = cur.fetchall()
            if len(supp) > 0:
                del self.supp_list[:]
                for row in supp:
                    self.supp_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def add(self):
        con = sqlite3.connect(database=r'idata.db')
        cur = con.cursor()
        try:
            # Check for duplicate product
            cur.execute("Select * from product where name=?", (self.var_name.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "Product already exists", parent=self.root)
            else:
                # Determine the next appropriate rowid
                cur.execute("SELECT MAX(rowid) FROM product")
                max_rowid = cur.fetchone()[0]
                if max_rowid is None:
                    max_rowid = 0
                new_rowid = max_rowid + 1

                # Insert with explicit rowid
                cur.execute("Insert into product (rowid, category, supplier, name, price, quantity, status) "
                            "values(?, ?, ?, ?, ?, ?, ?)",
                            (new_rowid,
                             self.var_cat.get(),
                             self.var_supp.get(),
                             self.var_name.get(),
                             self.var_price.get(),
                             self.var_qty.get(),
                             self.var_status.get()))
                con.commit()
                messagebox.showinfo("Success", "Product added successfully", parent=self.root)
                self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            cur.execute("Select * from product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def get_data(self, event):
        f = self.product_table.focus()
        content = self.product_table.item(f)
        row = content["values"]
        if row:
            self.var_pid.set(row[0])
            self.var_cat.set(row[1])
            self.var_supp.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            # Assuming the table has more columns for quantity, status, etc., they can be set similarly.

            if row and len(row) >= 1:
                self.var_name.set(row[1])
            else:
                self.var_name.set("")

            if row and len(row) >= 2:
                self.var_cat.set(row[2])
            else:
                self.var_cat.set("")

            if row and len(row) >= 3:
                self.var_supp.set(row[3])
            else:
                self.var_supp.set("")

            if row and len(row) >= 4:
                self.var_price.set(row[4])
            else:
                self.var_price.set("")

            if row and len(row) >= 5:
                self.var_qty.set(row[5])
            else:
                self.var_qty.set("")

            if row and len(row) >= 6:
                self.var_status.set(row[6])
            else:
                self.var_status.set("")

    def update(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    cur.execute("Update product set category=?, supplier=?, name=?, price=?, quantity=?, status=?"
                                "where pid=?", (
                                    self.var_cat.get(),
                                    self.var_supp.get(),
                                    self.var_name.get(),
                                    self.var_price.get(),
                                    self.var_qty.get(),
                                    self.var_status.get(),
                                    self.var_pid.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Product is required", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("Delete from product where pid=?", (self.var_pid.get(),))
                        con.commit()
                        reindex_primary_keys("product")
                        messagebox.showinfo("Success", "Employee deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear(self):
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_supp.set("Select")
        self.var_status.set("Select")
        self.var_cat.set("Select")

        self.var_search_by.set("Select")
        self.var_search_txt.set("")

        self.show()

    def search(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_search_by.get() == "Select":
                messagebox.showerror("Error", "Select search by option", parent=self.root)
            elif self.var_search_txt.get() == "":
                messagebox.showerror("Error", "Search text required", parent=self.root)
            else:
                cur.execute("Select * from product where " + self.var_search_by.get() + " LIKE '%" +
                            self.var_search_txt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def on_closing(self):
        if messagebox.askyesno("Confirm Close", "Are you sure you want to close?", parent=self.root):
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root)
    root.mainloop()
