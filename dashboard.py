from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from database import (
    get_all_records,
    insert_record,
    search_records,
    filter_records
)


class Dashboard:

    def __init__(self):

        self.root = Tk()

        self.root.title("Business Management System Dashboard")
        self.root.geometry("1200x700")

        title = Label(
            self.root,
            text="BUSINESS MANAGEMENT SYSTEM DASHBOARD",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=10)

        # ==========================
        # TOP FRAME
        # ==========================

        top_frame = Frame(self.root)
        top_frame.pack(fill=X, padx=10)

        Label(top_frame, text="Full Name").grid(row=0, column=0)

        self.name_entry = Entry(top_frame, width=25)
        self.name_entry.grid(row=0, column=1)

        Label(top_frame, text="Gender").grid(row=0, column=2)

        self.gender_combo = ttk.Combobox(
            top_frame,
            values=["Male", "Female", "Other"],
            state="readonly",
            width=15
        )
        self.gender_combo.grid(row=0, column=3)

        Label(top_frame, text="Status").grid(row=0, column=4)

        self.status_combo = ttk.Combobox(
            top_frame,
            values=["Active", "Inactive", "Pending"],
            state="readonly",
            width=15
        )
        self.status_combo.grid(row=0, column=5)

        Label(top_frame, text="Contact").grid(row=0, column=6)

        self.contact_entry = Entry(top_frame, width=20)
        self.contact_entry.grid(row=0, column=7)

        Button(
            top_frame,
            text="Add Record",
            bg="green",
            fg="white",
            command=self.add_record
        ).grid(row=0, column=8, padx=5)

        # ==========================
        # SEARCH FRAME
        # ==========================

        search_frame = Frame(self.root)
        search_frame.pack(fill=X, pady=10)

        Label(
            search_frame,
            text="Search"
        ).pack(side=LEFT, padx=5)

        self.search_entry = Entry(
            search_frame,
            width=30
        )

        self.search_entry.pack(side=LEFT)

        Button(
            search_frame,
            text="Search",
            command=self.search_data
        ).pack(side=LEFT, padx=5)

        Button(
            search_frame,
            text="Refresh",
            command=self.load_records
        ).pack(side=LEFT)

        # ==========================
        # FILTER FRAME
        # ==========================

        filter_frame = Frame(self.root)
        filter_frame.pack(fill=X)

        Label(
            filter_frame,
            text="Gender"
        ).pack(side=LEFT)

        self.filter_gender = ttk.Combobox(
            filter_frame,
            values=["Male", "Female", "Other"],
            state="readonly",
            width=15
        )

        self.filter_gender.pack(side=LEFT, padx=5)

        Label(
            filter_frame,
            text="Status"
        ).pack(side=LEFT)

        self.filter_status = ttk.Combobox(
            filter_frame,
            values=["Active", "Inactive", "Pending"],
            state="readonly",
            width=15
        )

        self.filter_status.pack(side=LEFT, padx=5)

        Button(
            filter_frame,
            text="Apply Filter",
            command=self.apply_filter
        ).pack(side=LEFT, padx=5)

        # ==========================
        # TABLE
        # ==========================

        self.tree = ttk.Treeview(
            self.root,
            columns=(
                "ID",
                "Name",
                "Gender",
                "Status",
                "Contact",
                "Date"
            ),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Full Name")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Date", text="Created Date")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=250)
        self.tree.column("Gender", width=100)
        self.tree.column("Status", width=100)
        self.tree.column("Contact", width=150)
        self.tree.column("Date", width=150)

        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ==========================
        # BOTTOM BUTTONS
        # ==========================

        bottom_frame = Frame(self.root)
        bottom_frame.pack(pady=10)

        Button(
            bottom_frame,
            text="Charts",
            bg="blue",
            fg="white",
            command=self.open_charts
        ).pack(side=LEFT, padx=5)

        Button(
            bottom_frame,
            text="PDF Reports",
            bg="orange",
            command=self.open_reports
        ).pack(side=LEFT, padx=5)

        Button(
            bottom_frame,
            text="Exit",
            bg="red",
            fg="white",
            command=self.root.destroy
        ).pack(side=LEFT, padx=5)

        self.load_records()

        self.root.mainloop()

    # ==========================
    # LOAD RECORDS
    # ==========================

    def load_records(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        records = get_all_records()

        for record in records:
            self.tree.insert(
                "",
                END,
                values=record
            )

    # ==========================
    # ADD RECORD
    # ==========================

    def add_record(self):

        name = self.name_entry.get()
        gender = self.gender_combo.get()
        status = self.status_combo.get()
        contact = self.contact_entry.get()

        if (
            name == ""
            or gender == ""
            or status == ""
            or contact == ""
        ):
            messagebox.showerror(
                "Error",
                "Please fill all fields"
            )
            return

        insert_record(
            name,
            gender,
            status,
            contact
        )

        messagebox.showinfo(
            "Success",
            "Record Added Successfully"
        )

        self.load_records()

        self.name_entry.delete(0, END)
        self.contact_entry.delete(0, END)

    # ==========================
    # SEARCH
    # ==========================

    def search_data(self):

        keyword = self.search_entry.get()

        results = search_records(keyword)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for record in results:
            self.tree.insert(
                "",
                END,
                values=record
            )

    # ==========================
    # FILTER
    # ==========================

    def apply_filter(self):

        gender = self.filter_gender.get()
        status = self.filter_status.get()

        results = filter_records(
            gender,
            status
        )

        for row in self.tree.get_children():
            self.tree.delete(row)

        for record in results:
            self.tree.insert(
                "",
                END,
                values=record
            )

    # ==========================
    # OPEN CHARTS
    # ==========================

    def open_charts(self):

        try:
            from charts import ChartsWindow
            ChartsWindow()

        except:
            messagebox.showinfo(
                "Charts",
                "charts.py not created yet"
            )

    # ==========================
    # OPEN REPORTS
    # ==========================

    def open_reports(self):

        try:
            from reports import ReportWindow
            ReportWindow()

        except:
            messagebox.showinfo(
                "Reports",
                "reports.py not created yet"
            )