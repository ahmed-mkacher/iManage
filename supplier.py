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


class SupplierClass:
    def __init__(self, element):
        self.root = element
        self.root.geometry("1170x490")
        self.root.title("Suppliers")
        self.root.config(bg="white")
        self.root.minsize(1170, 490)
        self.root.focus_force()

        # =============== All variables ===============
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        self.var_supp_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        # =============== Title ===============
        title = Label(self.root, text="Supplier Details", font=("times new roman", 20, "bold"),
                      bg="#0f4d7d", fg="white", justify=CENTER, anchor=CENTER)
        title.place(x=85, y=25, width=1000, height=40)

        # =============== Search Field ===============
        lbl_search = Label(self.root, text="Invoice No.", font=("times new roman", 13, "bold"),
                           justify=CENTER, bg="white")
        lbl_search.place(x=700, y=90)

        txt_search = Entry(self.root, textvariable=self.var_search_txt, font=("times new roman", 13, "bold"),
                           bg="lightyellow")
        txt_search.place(x=795, y=90, width=160)

        btn_search = Button(self.root, bg="#4caf50", text="Search", cursor="hand2", command=self.search,
                            font=("times new roman", 13, "bold"))
        btn_search.place(x=965, y=85, width=120, height=30)

        # =============== Content ===============
        # =============== Row 1 ===============
        lbl_supp_invoice = Label(self.root, text="Invoice No.", font=("times new roman", 15, "bold"), bg="white")
        lbl_supp_invoice.place(x=80, y=90)

        txt_supp_invoice = Entry(self.root, textvariable=self.var_supp_invoice, font=("times new roman", 15, "bold"),
                                 bg="lightyellow")
        txt_supp_invoice.place(x=190, y=90, width=200)

        # =============== Row 2 ===============
        lbl_name = Label(self.root, text="Name", font=("times new roman", 15, "bold"), bg="white")
        lbl_name.place(x=80, y=145)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman", 15, "bold"), bg="lightyellow")
        txt_name.place(x=190, y=145, width=200)

        # =============== Row 3 ===============
        lbl_contact = Label(self.root, text="Contact", font=("times new roman", 15, "bold"), bg="white")
        lbl_contact.place(x=80, y=200)

        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("times new roman", 15, "bold"),
                            bg="lightyellow")
        txt_contact.place(x=190, y=200, width=200)

        # =============== Row 4 ===============
        lbl_description = Label(self.root, text="Description", font=("times new roman", 15, "bold"), bg="white")
        lbl_description.place(x=80, y=255)

        self.txt_description = Text(self.root, font=("times new roman", 15, "bold"), bg="lightyellow")
        self.txt_description.place(x=190, y=255, width=460, height=120)

        # =============== Buttons ===============
        btn_save = Button(self.root, text="Save", command=self.add, font=("times new roman", 15, "bold"), bg="#2196f3",
                          fg="white", cursor="hand2")
        btn_save.place(x=190, y=400, width=110, height=35)
        btn_update = Button(self.root, text="Update", command=self.update, font=("times new roman", 15, "bold"),
                            bg="#4caf50", fg="white", cursor="hand2")
        btn_update.place(x=320, y=400, width=110, height=35)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("times new roman", 15, "bold"),
                            bg="#f44336", fg="white", cursor="hand2")
        btn_delete.place(x=450, y=400, width=110, height=35)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15, "bold"),
                           bg="#607d8b", fg="white", cursor="hand2")
        btn_clear.place(x=580, y=400, width=110, height=35)

        # =============== Supplier Details ===============
        supp_frame = Frame(self.root, bd=3, relief=RIDGE)
        supp_frame.place(x=705, y=130, width=380, height=305)

        scroll_y = Scrollbar(supp_frame, orient=VERTICAL)
        scroll_x = Scrollbar(supp_frame, orient=HORIZONTAL)

        self.supp_table = ttk.Treeview(supp_frame, columns=("invoice", "name", "contact", "description"),
                                       yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.supp_table.xview)
        scroll_y.config(command=self.supp_table.yview)

        self.supp_table.heading("invoice", text="Invoice No.")
        self.supp_table.heading("name", text="Name")
        self.supp_table.heading("contact", text="Contact")
        self.supp_table.heading("description", text="Description")

        self.supp_table["show"] = "headings"

        self.supp_table.column("invoice", width=100)
        self.supp_table.column("name", width=100)
        self.supp_table.column("contact", width=100)
        self.supp_table.column("description", width=100)

        self.supp_table.pack(fill=BOTH, expand=1)
        self.supp_table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_supp_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. and Name are required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_supp_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Invoice No. already assigned, try different",
                                         parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice, name, contact, description) values(?,?,?,?)",
                                (
                                    self.var_supp_invoice.get(),
                                    self.var_name.get(),
                                    self.var_contact.get(),
                                    self.txt_description.get("1.0", "end"),))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows = cur.fetchall()
            self.supp_table.delete(*self.supp_table.get_children())
            for row in rows:
                self.supp_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def get_data(self, event):
        f = self.supp_table.focus()
        content = self.supp_table.item(f)
        row = content["values"]
        if row and len(row) >= 1:  # Check if row is not empty and has at least one element
            self.var_supp_invoice.set(row[0])
        else:
            self.var_supp_invoice.set("")  # Set a default value if row is empty or lacks elements

        if row and len(row) >= 2:
            self.var_name.set(row[1])
        else:
            self.var_name.set("")

        if row and len(row) >= 3:
            self.txt_description.delete("1.0", "end")
            self.txt_description.insert(END, row[2])
        else:
            self.txt_description.delete("1.0", "end")

        if row and len(row) >= 4:
            self.var_contact.set(row[3])
        else:
            self.var_contact.set("")

    def update(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_supp_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. and Name are required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_supp_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invoice No. already assigned, try different",
                                         parent=self.root)
                else:
                    cur.execute("Update supplier set name=?, contact=?, description=? where invoice=?",
                                (
                                    self.var_name.get(),
                                    self.var_contact.get(),
                                    self.txt_description.get("1.0", "end-1c"),
                                    self.var_supp_invoice.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_supp_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. is required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_supp_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invoice No. already assigned, try different",
                                         parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("Delete from supplier where invoice=?",
                                    (self.var_supp_invoice.get(),))
                        con.commit()
                        reindex_primary_keys("supplier")
                        messagebox.showinfo("Success", "Supplier deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear(self):
        self.var_supp_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_description.delete("1.0", "end")

        self.var_search_txt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_search_txt.get() == "":
                messagebox.showerror("Error", "Invoice No. required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_search_txt.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.supp_table.delete(*self.supp_table.get_children())
                    self.supp_table.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def on_closing(self):
        if messagebox.askyesno("Confirm Close", "Are you sure you want to close?", parent=self.root):
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = SupplierClass(root)
    root.mainloop()
