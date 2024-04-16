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


class EmployeeClass:
    def __init__(self, element):
        self.root = element
        self.root.geometry("1125x600")
        self.root.title("Employees")
        self.root.config(bg="white")
        self.root.minsize(1125, 600)
        self.root.focus_force()

        # =============== All variables ===============
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        self.var_emp_id = StringVar()
        self.var_name = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_utype = StringVar()
        self.var_pass = StringVar()
        self.var_salary = StringVar()
        self.var_address = StringVar()

        # =============== Title ===============
        title = Label(self.root, text="Employee Details", font=("times new roman", 20, "bold"),
                      bg="#0f4d7d", fg="white", justify=CENTER, anchor=CENTER)
        title.place(x=85, y=125, relwidth=0.85)

        # =============== Search Frame ===============
        search_frame = LabelFrame(self.root, text="Search Employee", font=("times new roman", 15, "bold"), bd=2,
                                  relief=RIDGE, bg="white")
        search_frame.place(x=250, y=20, width=595, height=80)

        # =============== Search Field ===============
        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_search_by, font=("times new roman", 13, "bold"),
                                  state="readonly", justify=CENTER, values=("Select", "Name", "Email", "Contact"))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(search_frame, textvariable=self.var_search_txt, font=("times new roman", 13, "bold"),
                           bg="lightyellow")
        txt_search.place(x=200, y=11, width=220)

        btn_search = Button(search_frame, bg="#4caf50", text="Search", cursor="hand2", command=self.search,
                            font=("times new roman", 13, "bold"))
        btn_search.place(x=430, y=7, width=150, height=30)

        # =============== Content ===============
        # =============== Row 1 ===============
        lbl_emp_id = Label(self.root, text="Emp ID", font=("times new roman", 15, "bold"), bg="white")
        lbl_emp_id.place(x=90, y=200)

        txt_emp_id = Entry(self.root, textvariable=self.var_emp_id, font=("times new roman", 15, "bold"),
                           bg="lightyellow")
        txt_emp_id.place(x=165, y=200, width=200)

        lbl_gender = Label(self.root, text="Gender", font=("times new roman", 15, "bold"), bg="white")
        lbl_gender.place(x=410, y=200)

        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, font=("times new roman", 13, "bold"),
                                  state="readonly", justify=CENTER, values=("Select", "Male", "Female"))
        cmb_gender.place(x=485, y=200, width=200)
        cmb_gender.current(0)

        lbl_contact = Label(self.root, text="Contact", font=("times new roman", 15, "bold"), bg="white")
        lbl_contact.place(x=735, y=200)

        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("times new roman", 15, "bold"),
                            bg="lightyellow")
        txt_contact.place(x=835, y=200, width=200)

        # =============== Row 2 ===============
        lbl_name = Label(self.root, text="Name", font=("times new roman", 15, "bold"), bg="white")
        lbl_name.place(x=90, y=255)
        lbl_dob = Label(self.root, text="D.O.B.", font=("times new roman", 15, "bold"), bg="white")
        lbl_dob.place(x=410, y=255)
        lbl_doj = Label(self.root, text="D.O.J.", font=("times new roman", 15, "bold"), bg="white")
        lbl_doj.place(x=735, y=255)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman", 15, "bold"), bg="lightyellow")
        txt_name.place(x=165, y=255, width=200)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("times new roman", 15, "bold"), bg="lightyellow")
        txt_dob.place(x=485, y=255, width=200)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("times new roman", 15, "bold"), bg="lightyellow")
        txt_doj.place(x=835, y=255, width=200)

        # =============== Row 3 ===============
        lbl_email = Label(self.root, text="Email", font=("times new roman", 15, "bold"), bg="white")
        lbl_email.place(x=90, y=310)
        lbl_pass = Label(self.root, text="Pass", font=("times new roman", 15, "bold"), bg="white")
        lbl_pass.place(x=410, y=310)
        lbl_utype = Label(self.root, text="User type", font=("times new roman", 15, "bold"), bg="white")
        lbl_utype.place(x=735, y=310)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("times new roman", 15, "bold"),
                          bg="lightyellow")
        txt_email.place(x=165, y=310, width=200)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("times new roman", 15, "bold"), bg="lightyellow")
        txt_pass.place(x=485, y=310, width=200)

        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, font=("times new roman", 13, "bold"),
                                 state="readonly", justify=CENTER, values=("Select", "Admin", "Employee"))
        cmb_utype.place(x=835, y=310, width=200)
        cmb_utype.current(0)

        # =============== Row 4 ===============
        lbl_address = Label(self.root, text="Address", font=("times new roman", 15, "bold"), bg="white")
        lbl_address.place(x=90, y=365)
        lbl_salary = Label(self.root, text="Salary", font=("times new roman", 15, "bold"), bg="white")
        lbl_salary.place(x=480, y=365)

        self.txt_address = Text(self.root, font=("times new roman", 15, "bold"), bg="lightyellow")
        self.txt_address.place(x=165, y=365, width=280, height=70)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("times new roman", 15, "bold"),
                           bg="lightyellow")
        txt_salary.place(x=555, y=365, width=200)

        # =============== Buttons ===============
        btn_save = Button(self.root, text="Save", command=self.add, font=("times new roman", 15, "bold"), bg="#2196f3",
                          fg="white", cursor="hand2")
        btn_save.place(x=480, y=400, width=110, height=35)
        btn_update = Button(self.root, text="Update", command=self.update, font=("times new roman", 15, "bold"),
                            bg="#4caf50", fg="white", cursor="hand2")
        btn_update.place(x=630, y=400, width=110, height=35)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("times new roman", 15, "bold"),
                            bg="#f44336", fg="white", cursor="hand2")
        btn_delete.place(x=780, y=400, width=110, height=35)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15, "bold"),
                           bg="#607d8b", fg="white", cursor="hand2")
        btn_clear.place(x=930, y=400, width=110, height=35)

        # =============== Employee Details ===============
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=450, relwidth=1, height=150)

        scroll_y = Scrollbar(emp_frame, orient=VERTICAL)
        scroll_x = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.emp_table = ttk.Treeview(emp_frame, columns=("eid", "name", "gender", "contact", "dob", "doj", "email",
                                                          "pass", "utype", "address", "salary"),
                                      yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.emp_table.xview)
        scroll_y.config(command=self.emp_table.yview)

        self.emp_table.heading("eid", text="EMP ID")
        self.emp_table.heading("name", text="Name")
        self.emp_table.heading("email", text="Email")
        self.emp_table.heading("gender", text="Gender")
        self.emp_table.heading("contact", text="Contact")
        self.emp_table.heading("dob", text="D.O.B.")
        self.emp_table.heading("doj", text="D.O.J.")
        self.emp_table.heading("utype", text="User type")
        self.emp_table.heading("pass", text="Password")
        self.emp_table.heading("salary", text="Salary")
        self.emp_table.heading("address", text="Address")

        self.emp_table["show"] = "headings"

        self.emp_table.column("eid", width=100)
        self.emp_table.column("name", width=100)
        self.emp_table.column("email", width=100)
        self.emp_table.column("gender", width=100)
        self.emp_table.column("contact", width=100)
        self.emp_table.column("dob", width=100)
        self.emp_table.column("doj", width=100)
        self.emp_table.column("utype", width=100)
        self.emp_table.column("pass", width=100)
        self.emp_table.column("salary", width=100)
        self.emp_table.column("address", width=100)

        self.emp_table.pack(fill=BOTH, expand=1)
        self.emp_table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID and Name are required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Employee ID already assigned, try another one",
                                         parent=self.root)
                else:
                    cur.execute("Insert into employee (eid, name, email, gender, contact, dob, doj, pass, utype,"
                                "address, salary) values(?,?,?,?,?,?,?,?,?,?,?)", (
                                    self.var_emp_id.get(),
                                    self.var_name.get(),
                                    self.var_email.get(),
                                    self.var_gender.get(),
                                    self.var_contact.get(),

                                    self.var_dob.get(),
                                    self.var_doj.get(),

                                    self.var_pass.get(),
                                    self.var_utype.get(),
                                    self.txt_address.get("1.0", "end"),
                                    self.var_salary.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Employee added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            cur.execute("Select * from employee")
            rows = cur.fetchall()
            self.emp_table.delete(*self.emp_table.get_children())
            for row in rows:
                self.emp_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def get_data(self, event):
        f = self.emp_table.focus()
        content = self.emp_table.item(f)
        row = content["values"]
        print(row)

        if row and len(row) >= 1:
            self.var_emp_id.set(row[0])
        else:
            self.var_emp_id.set("")

        if row and len(row) >= 2:
            self.var_name.set(row[1])
        else:
            self.var_name.set("")

        if row and len(row) >= 3:
            self.var_gender.set(row[2])
        else:
            self.var_gender.set("")

        if row and len(row) >= 4:
            self.var_contact.set(row[3])
        else:
            self.var_contact.set("")

        if row and len(row) >= 5:
            self.var_dob.set(row[4])
        else:
            self.var_dob.set("")

        if row and len(row) >= 6:
            self.var_doj.set(row[5])
        else:
            self.var_doj.set("")

        if row and len(row) >= 7:
            self.var_email.set(row[6])
        else:
            self.var_email.set("")

        if row and len(row) >= 8:
            self.var_pass.set(row[7])
        else:
            self.var_pass.set("")

        if row and len(row) >= 9:
            self.var_utype.set(row[8])
        else:
            self.var_utype.set("")

        if row and len(row) >= 10:
            self.txt_address.delete("1.0", "end")
            self.txt_address.insert(END, row[9])
        else:
            self.txt_address.delete("1.0", "end")

        if row and len(row) >= 11:
            self.var_salary.set(row[10])
        else:
            self.var_salary.set("")

    def update(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID and Name are required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    cur.execute("Update employee set name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?,"
                                "utype=?, address=?, salary=? where eid=?", (
                                    self.var_name.get(),
                                    self.var_email.get(),
                                    self.var_gender.get(),
                                    self.var_contact.get(),

                                    self.var_dob.get(),
                                    self.var_doj.get(),

                                    self.var_pass.get(),
                                    self.var_utype.get(),
                                    self.txt_address.get("1.0", "end-1c"),
                                    self.var_salary.get(),
                                    self.var_emp_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Employee updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID and Name are required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Employee ID already assigned, try another one",
                                         parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("Delete from employee where eid=?", (self.var_emp_id.get(),))
                        con.commit()
                        reindex_primary_keys("employee")
                        messagebox.showinfo("Success", "Employee deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")

        self.var_dob.set("")
        self.var_doj.set("")

        self.var_pass.set("")
        self.var_utype.set("Select")
        if self.txt_address.get("1.0", "end-1c"):  # Check if the Text widget is not empty
            self.txt_address.delete("1.0", "end")  # Use "end" instead of "END" here
        self.var_salary.set("")
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
                cur.execute("Select * from employee where " + self.var_search_by.get() + " LIKE '%" +
                            self.var_search_txt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.emp_table.delete(*self.emp_table.get_children())
                    for row in rows:
                        self.emp_table.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def on_closing(self):
        if messagebox.askyesno("Confirm Close", "Are you sure you want to close?", parent=self.root):
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()
