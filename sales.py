import os
from tkinter import *
from tkinter import messagebox


class SalesClass:
    def __init__(self, element):
        self.root = element
        self.root.geometry("820x500")
        self.root.title("Sales")
        self.root.config(bg="white")
        self.root.minsize(820, 500)
        self.root.focus_force()

        # =============== Variables ===============
        self.var_invoice = StringVar()
        self.bill_list = []

        # =============== Title ===============
        lbl_title = Label(self.root, text="Manage Sales", font=("times new roman", 20, "bold"), bg="#4d636d",
                          fg="white")
        lbl_title.place(x=0, y=0, relwidth=1, height=50)

        # =============== Content ===============
        lbl_invoice = Label(self.root, text="Invoice No.", font=("times new roman", 15, "bold"), bg="white")
        lbl_invoice.place(x=50, y=80)

        txt_invoice = Entry(self.root, font=("times new roman", 15, "bold"), bg="lightyellow")
        txt_invoice.place(x=160, y=80, width=150)

        # =============== Sales Frame ===============
        sales_frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_frame.place(x=50, y=140, width=200, height=330)

        scroll_y = Scrollbar(sales_frame, orient=VERTICAL)
        self.sales_list = Listbox(sales_frame, font=("times new roman", 15, "bold"), yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH, expand=1)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        # =============== Bill Area ===============
        bill_frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_frame.place(x=280, y=140, width=490, height=330)

        lbl_title_2 = Label(bill_frame, text="Bill Area", font=("times new roman", 15, "bold"), bg="#4d636d",
                            fg="white")
        lbl_title_2.pack(side=TOP, fill=X)

        scroll_y_2 = Scrollbar(bill_frame, orient=VERTICAL)
        self.bill_area = Text(bill_frame, font=("times new roman", 15, "bold"), bg="lightyellow",
                              yscrollcommand=scroll_y_2.set)
        scroll_y_2.pack(side=RIGHT, fill=Y)
        scroll_y_2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # =============== Buttons ===============
        btn_search = Button(self.root, text="Search", font=("times new roman", 15, "bold"), bg="#4d636d", fg="white",
                            cursor="hand2", command=self.search)
        btn_search.place(x=325, y=76, width=100, height=35)

        btn_clear = Button(self.root, text="Clear", font=("times new roman", 15, "bold"), bg="lightgray", fg="black",
                           cursor="hand2", command=self.clear)
        btn_clear.place(x=440, y=76, width=100, height=35)

        self.show()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0, END)  # Use "end" to delete all items
        for i in os.listdir("billing/"):
            if i.split(".")[-1] == "txt":
                self.sales_list.insert(END, i)
                self.bill_list.append(i.split(".")[0])

    def get_data(self, event):
        try:
            index = self.sales_list.curselection()[0]
            selected_file = self.sales_list.get(index)
            self.bill_area.delete("1.0", END)  # Use "end" to delete all items
            file = open(f"billing/{selected_file}", "r")
            for i in file:
                self.bill_area.insert(END, i)
            file.close()
        except IndexError:
            pass  # No selection or invalid index
        except Exception as ex:
            messagebox.showerror("Error", f"Error while reading data: {str(ex)}")

    def search(self):
        if self.var_invoice.get() != "":
            messagebox.showinfo("Success", "Search Successful")
        else:
            if self.var_invoice.get() in self.bill_list:
                file = open(f"billing/{self.var_invoice.get()}", "r")
                self.bill_area.delete("1.0", END)  # Use "end" to delete all items
                for i in file:
                    self.bill_area.insert(END, i)
                file.close()
            else:
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete("1.0", END)  # Use "end" to delete all items

    def on_closing(self):
        if messagebox.askyesno("Confirm Close", "Are you sure you want to close?", parent=self.root):
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = SalesClass(root)
    root.mainloop()
