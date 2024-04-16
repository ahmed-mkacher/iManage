import time
from tkinter import *
from PIL import ImageTk
import sqlite3
import os
from tkinter import messagebox
import email_pass
import smtplib


class LoginClass:
    def __init__(self, element):
        self.btn_update = None
        self.btn_otp = None
        self.var_confirm_pass = None
        self.otp = None
        self.im = None
        self.forget_window = None
        self.var_new_pass = None
        self.var_otp = None
        self.root = element
        self.root.title("Login System")
        self.root.geometry("1350x700")
        self.root.minsize(1250, 700)
        self.root.maxsize(1250, 700)
        self.root.config(bg="white")
        self.root.minsize(1250, 700)

        # =============== Variables ===============
        self.var_employee_id = StringVar()
        self.var_password = StringVar()

        # =============== Images ===============
        self.phone = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phone_image = Label(self.root, image=self.phone, bd=0, bg="white")
        self.lbl_phone_image.place(x=200, y=50)

        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_img = Label(self.root, bd=0, bg="white")
        self.lbl_change_img.place(x=338, y=140, width=240, height=411)

        # =============== Login Frame ===============
        login_frame = Frame(self.root, bg="white", bd=3, relief=RIDGE)
        login_frame.place(x=650, y=90, width=350, height=460)

        title = Label(login_frame, text="Login System", font=("times new roman", 30, "bold"), bg="white", fg="#4d636d")
        title.place(x=0, y=30, relwidth=1)

        lbl_employee_id = Label(login_frame, text="Employee ID", font=("times new roman", 20, "bold"), bg="white",
                                fg="#4d636d")
        lbl_employee_id.place(x=50, y=120)
        txt_employee_id = Entry(login_frame, textvariable=self.var_employee_id, font=("times new roman", 15, "bold"),
                                bg="lightyellow")
        txt_employee_id.place(x=50, y=160, width=250, height=35)

        lbl_password = Label(login_frame, text="Password", font=("times new roman", 20, "bold"), bg="white",
                             fg="#4d636d")
        lbl_password.place(x=50, y=200)
        txt_password = Entry(login_frame, textvariable=self.var_password, font=("times new roman", 15, "bold"),
                             bg="lightyellow", show="*")
        txt_password.place(x=50, y=240, width=250, height=35)

        btn_login = Button(login_frame, text="Login", font=("times new roman", 15, "bold"), bg="#01a2f5", fg="white",
                           cursor="hand2", command=self.login)
        btn_login.place(x=50, y=300, width=100, height=35)

        hr = Label(login_frame, bg="lightgray")
        hr.place(x=50, y=350, width=250, height=2)
        or_ = Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold"))
        or_.place(x=160, y=340)

        btn_forget = Button(login_frame, text="Forget Password?", font=("times new roman", 15, "bold"), bg="white",
                            fg="#4d636d", bd=0, cursor="hand2", command=self.reset_window)
        btn_forget.place(x=50, y=370, width=250, height=35)

        # =============== Register Frame ===============
        register_frame = Frame(self.root, bg="white", bd=3, relief=RIDGE)
        register_frame.place(x=650, y=560, width=350, height=60)

        lbl_reg = Label(register_frame, text="Don't have an account?", font=("times new roman", 15), bg="white",
                        fg="lightgray")
        lbl_reg.place(x=20, y=15)

        self.animate()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # =============== All Functions ===============
    def login(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_employee_id.get() == "" or self.var_password.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("Select utype from employee where eid = ? AND pass = ?", (
                    self.var_employee_id.get(),
                    self.var_password.get(),))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Error", "Invalid ID or password", parent=self.root)
                else:
                    if user[0] == "Admin":
                        messagebox.showinfo("Success", "Welcome", parent=self.root)
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        messagebox.showinfo("Success", "Welcome", parent=self.root)
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_img.config(image=self.im)
        self.lbl_change_img.after(2000, self.animate)

    def on_closing(self):
        if messagebox.askyesno("Confirm Close", "Are you sure you want to close?", parent=self.root):
            self.root.destroy()

    def reset_window(self):
        con = sqlite3.connect(database=r"idata.db")
        cur = con.cursor()
        try:
            if self.var_employee_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required", parent=self.root)
            else:
                cur.execute("Select email from employee where eid = ?", (self.var_employee_id.get(),))
                email = cur.fetchone()
                if email is None:
                    messagebox.showerror("Error", "Invalid Employee ID, try again", parent=self.root)
                else:
                    # =============== Forget Password Window ===============
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_confirm_pass = StringVar()
                    chk = self.send_email(email[0])
                    if chk is False:
                        messagebox.showerror("Error", "Error sending OTP", parent=self.root)
                    else:
                        pass
                    self.forget_window = Toplevel(self.root)
                    self.forget_window.title("Reset Password")
                    self.forget_window.geometry("400x380")
                    self.forget_window.config(bg="white")
                    self.forget_window.minsize(400, 380)
                    self.forget_window.maxsize(400, 380)
                    self.forget_window.focus_force()

                    title = Label(self.forget_window, text="Reset Password", font=("times new roman", 20, "bold"),
                                  bg="lightgray", fg="#4d636d")
                    title.pack(side=TOP, fill=X)

                    lbl_otp = Label(self.forget_window, text="Enter OTP sent on registered email",
                                    font=("times new roman", 15), bg="white", fg="#4d636d")
                    lbl_otp.place(x=20, y=60)
                    txt_otp = Entry(self.forget_window, textvariable=self.var_otp, font=("times new roman", 15),
                                    bg="lightyellow")
                    txt_otp.place(x=20, y=100, width=250, height=35)

                    btn_otp = Button(self.forget_window, text="Submit", font=("times new roman", 15, "bold"),
                                     bg="#01a2f5", fg="white", cursor="hand2", command=self.verify)
                    btn_otp.place(x=280, y=99, width=100, height=35)

                    lbl_new_pass = Label(self.forget_window, text="Enter New Password", font=("times new roman", 15),
                                         bg="white", fg="#4d636d")
                    lbl_new_pass.place(x=20, y=153)
                    txt_new_pass = Entry(self.forget_window, textvariable=self.var_new_pass,
                                         font=("times new roman", 15), bg="lightyellow")
                    txt_new_pass.place(x=20, y=188, width=250, height=35)

                    lbl_confirm_pass = Label(self.forget_window, text="Confirm New Password",
                                             font=("times new roman", 15), bg="white", fg="#4d636d")
                    lbl_confirm_pass.place(x=20, y=240)
                    txt_confirm_pass = Entry(self.forget_window, textvariable=self.var_confirm_pass,
                                             font=("times new roman", 15), bg="lightyellow")
                    txt_confirm_pass.place(x=20, y=275, width=250, height=35)

                    btn_update = Button(self.forget_window, text="Update", cursor="hand2", bg="#01a2f5", fg="white",
                                        font=("times new roman", 15, "bold"), state=DISABLED, command=self.update)
                    btn_update.place(x=150, y=325, width=100, height=35)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def update(self):
        if self.var_new_pass.get() == "" or self.var_confirm_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.forget_window)
        elif self.var_new_pass.get() != self.var_confirm_pass.get():
            messagebox.showerror("Error", "Passwords do not match", parent=self.forget_window)
        else:
            con = sqlite3.connect(database=r"idata.db")
            cur = con.cursor()
            try:
                cur.execute("Update employee set pass = ? where eid = ?", (
                    self.var_new_pass.get(),
                    self.var_employee_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Password updated successfully", parent=self.forget_window)
                self.forget_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.forget_window)

    def send_email(self, to):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email = email_pass.main_email
        password = email_pass.password
        s.login(email, password)
        self.otp = str(time.strftime("%H:%M:%S")) + str(time.strftime("%S"))
        print(self.otp)
        subj = "OTP for iData"
        msg = "Your OTP is " + self.otp
        msg = 'Subject: {}\n\n{}'.format(subj, msg)
        s.sendmail(email, to, msg)
        chk = s.ehlo()
        if chk[0] == 250:
            messagebox.showinfo("Success", "OTP sent successfully", parent=self.root)
            return True
        else:
            messagebox.showerror("Error", "Error sending OTP", parent=self.root)
            return False

    def verify(self):
        if int(self.var_otp.get()) == int(self.otp):
            self.btn_update.config(state=NORMAL)
            self.btn_otp.config(state=DISABLED)
            messagebox.showinfo("Success", "OTP verified successfully", parent=self.root)
            return True
        else:
            messagebox.showerror("Error", "Invalid OTP", parent=self.root)
            return False


if __name__ == "__main__":
    root = Tk()
    obj = LoginClass(root)
    root.mainloop()
