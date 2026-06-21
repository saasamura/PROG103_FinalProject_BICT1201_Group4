from tkinter import *
from tkinter import messagebox


class LoginWindow:

    def __init__(self):

        self.root = Tk()

        self.root.title("Business Management System Login")

        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # Title
        title = Label(
            self.root,
            text="BUSINESS MANAGEMENT SYSTEM",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)

        subtitle = Label(
            self.root,
            text="User Login",
            font=("Arial", 12)
        )
        subtitle.pack()

        # Username
        Label(
            self.root,
            text="Username"
        ).pack(pady=5)

        self.username_entry = Entry(
            self.root,
            width=30
        )
        self.username_entry.pack()

        # Password
        Label(
            self.root,
            text="Password"
        ).pack(pady=5)

        self.password_entry = Entry(
            self.root,
            width=30,
            show="*"
        )
        self.password_entry.pack()

        # Login Button
        Button(
            self.root,
            text="Login",
            width=20,
            bg="green",
            fg="white",
            command=self.login
        ).pack(pady=15)

        # Forgot Password Button
        Button(
            self.root,
            text="Forgot Password?",
            command=self.forgot_password
        ).pack()

        self.root.mainloop()

    def login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        # Hardcoded credentials
        if username == "admin" and password == "admin123":

            messagebox.showinfo(
                "Success",
                "Login Successful!"
            )

            self.root.destroy()

            from dashboard import Dashboard

            Dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password"
            )

    def forgot_password(self):

        messagebox.showinfo(
            "Forgot Password",
            "Default Username: admin\nDefault Password: admin123"
        )