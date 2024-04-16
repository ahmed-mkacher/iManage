import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


def reindex_primary_keys(table_name):
    con = sqlite3.connect(database=r'idata.db')
    cur = con.cursor()

    # Add a temporary column to store new indexes
    cur.execute(f"ALTER TABLE {table_name} ADD COLUMN temp_new_index INTEGER")

    # Fetch current row-ids and set the new indexes in the temporary column
    cur.execute(f"SELECT rowid FROM {table_name} ORDER BY rowid")
    existing_ids = [row[0] for row in cur.fetchall()]
    for index, rowid in enumerate(existing_ids, start=1):
        cur.execute(f"UPDATE {table_name} SET temp_new_index=? WHERE rowid=?", (index, rowid))

    # Update the rowid with the new indexes from the temporary column
    cur.execute(f"UPDATE {table_name} SET rowid=temp_new_index")

    # Drop the temporary column
    cur.execute(f"ALTER TABLE {table_name} DROP COLUMN temp_new_index")

    con.commit()
    con.close()


class CategoryClass:
    def __init__(self, element):
        self.root = element
        self.root.geometry("1170x490")
        self.root.title("Categories")
        self.root.config(bg="white")
        self.root.minsize(1170, 490)
        self.root.focus_force()

        # =============== Variables ===============
        self.var_cat_id = StringVar()
        self.var_cat_name = StringVar()
        self.var_cat_status = StringVar()

        # =============== Category Details ===============
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=705, y=130, width=380, height=305)

        scroll_y = Scrollbar(cat_frame, orient=VERTICAL)
        scroll_x = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.cat_table = ttk.Treeview(cat_frame, columns=("cid", "name"),
                                      yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.cat_table.xview)
        scroll_y.config(command=self.cat_table.yview)

        self.cat_table.heading("cid", text="Category ID")
        self.cat_table.heading("name", text="Name")

        self.cat_table["show"] = "headings"

        self.cat_table.column("cid", width=100)
        self.cat_table.column("name", width=100)

        self.cat_table.pack(fill=BOTH, expand=1)
        self.cat_table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        # =============== Title ===============
        lbl_title = Label(self.root, text="Manage Categories", font=("times new roman", 20, "bold"), bg="#4d636d",
                          fg="white")
        lbl_title.pack(side=TOP, fill=X)

        # =============== Row 1 ===============
        lbl_cat_name = Label(self.root, text="Enter Category Name", font=("times new roman", 35, "bold"), bg="white")
        lbl_cat_name.place(x=40, y=60)
        txt_cat_name = Entry(self.root, textvariable=self.var_cat_name, font=("times new roman", 15, "bold"),
                             bg="lightyellow")
        txt_cat_name.place(x=45, y=135, width=290)

        btn_add = Button(self.root, text="Add", font=("times new roman", 15, "bold"), bg="#4d636d", fg="white",
                         cursor="hand2", command=self.add)
        btn_add.place(x=375, y=132, width=100, height=30)

        btn_delete = Button(self.root, text="Delete", font=("times new roman", 15, "bold"), bg="#4d636d", fg="white",
                            cursor="hand2", command=self.delete)
        btn_delete.place(x=495, y=132, width=100, height=30)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add(self):
        con = sqlite3.connect(database=r'idata.db')
        cur = con.cursor()
        try:
            # Check for duplicate category
            cur.execute("Select * from category where name=?", (self.var_cat_name.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "Category already exists", parent=self.root)
            else:
                # Determine the next appropriate rowid
                cur.execute("SELECT MAX(rowid) FROM category")
                max_rowid = cur.fetchone()[0]
                if max_rowid is None:
                    max_rowid = 0
                new_rowid = max_rowid + 1

                # Insert with explicit rowid
                cur.execute("Insert into category (rowid, name) values(?, ?)",
                            (new_rowid, self.var_cat_name.get()))
                con.commit()
                messagebox.showinfo("Success", "Category added successfully", parent=self.root)
                self.show()
                self.var_cat_id.set("")
                self.var_cat_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_cat_name.get() == "":
                messagebox.showerror("Error", "Category is required", parent=self.root)
            else:
                cur.execute("Select * from category where cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Please select category from the list first",
                                         parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("Delete from category where cid=?",
                                    (self.var_cat_id.get(),))
                        con.commit()
                        reindex_primary_keys("category")
                        messagebox.showinfo("Success", "Supplier deleted successfully", parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_cat_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            cur.execute("Select * from category")
            rows = cur.fetchall()
            self.cat_table.delete(*self.cat_table.get_children())
            for row in rows:
                self.cat_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def get_data(self, event):
        f = self.cat_table.focus()
        content = self.cat_table.item(f)
        row = content["values"]

        if row and len(row) >= 1:  # Check if row is not empty and has at least one element
            self.var_cat_id.set(row[0])
        else:
            self.var_cat_id.set("")  # Set a default value if row is empty or lacks elements

        if row and len(row) >= 2:
            self.var_cat_name.set(row[1])
        else:
            self.var_cat_name.set("")

    def on_closing(self):
        if messagebox.askyesno("Confirm Close", "Are you sure you want to close?", parent=self.root):
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = CategoryClass(root)
    root.mainloop()
