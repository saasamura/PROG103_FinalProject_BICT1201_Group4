from tkinter import *
from tkinter import ttk, messagebox

from database import (
    get_all_records,
    insert_record,
    search_records,
    filter_records,
    update_record,
    delete_record
)


class Dashboard:

    def __init__(self):

        self.root = Tk()
        self.root.title("Business Management System Dashboard")
        self.root.geometry("1200x700")

        Label(self.root, text="BUSINESS MANAGEMENT SYSTEM DASHBOARD",
              font=("Arial", 18, "bold")).pack(pady=10)

        # ================= TOP FRAME =================
        top_frame = Frame(self.root)
        top_frame.pack(fill=X, padx=10)

        Label(top_frame, text="Full Name").grid(row=0, column=0)
        self.name_entry = Entry(top_frame, width=25)
        self.name_entry.grid(row=0, column=1)

        Label(top_frame, text="Gender").grid(row=0, column=2)
        self.gender_combo = ttk.Combobox(top_frame, values=["Male", "Female", "Other"], state="readonly", width=15)
        self.gender_combo.grid(row=0, column=3)

        Label(top_frame, text="Status").grid(row=0, column=4)
        self.status_combo = ttk.Combobox(top_frame, values=["Active", "Inactive", "Pending"], state="readonly", width=15)
        self.status_combo.grid(row=0, column=5)

        Label(top_frame, text="Contact").grid(row=0, column=6)
        self.contact_entry = Entry(top_frame, width=20)
        self.contact_entry.grid(row=0, column=7)

        Button(top_frame, text="Add Record", bg="green", fg="white",
               command=self.add_record).grid(row=0, column=8, padx=5)

        # ================= SEARCH FRAME =================
        search_frame = Frame(self.root)
        search_frame.pack(fill=X, pady=10)

        self.search_entry = Entry(search_frame, width=30)
        self.search_entry.pack(side=LEFT)

        Button(search_frame, text="Search", command=self.search_data).pack(side=LEFT, padx=5)
        Button(search_frame, text="Refresh", command=self.load_records).pack(side=LEFT)

        # ================= FILTER FRAME =================
        filter_frame = Frame(self.root)
        filter_frame.pack(fill=X)

        self.filter_gender = ttk.Combobox(filter_frame, values=["Male", "Female", "Other"], state="readonly", width=15)
        self.filter_gender.pack(side=LEFT, padx=5)

        self.filter_status = ttk.Combobox(filter_frame, values=["Active", "Inactive", "Pending"], state="readonly", width=15)
        self.filter_status.pack(side=LEFT, padx=5)

        Button(filter_frame, text="Apply Filter", command=self.apply_filter).pack(side=LEFT, padx=5)

        # ================= TABLE =================
        self.tree = ttk.Treeview(self.root,
                                 columns=("ID", "Name", "Gender", "Status", "Contact", "Date"),
                                 show="headings")

        for col in ("ID", "Name", "Gender", "Status", "Contact", "Date"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill=BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.select_record)

        # ================= BUTTONS =================
        bottom = Frame(self.root)
        bottom.pack(pady=10)

        Button(bottom, text="Update", bg="orange", command=self.update_selected).pack(side=LEFT, padx=5)
        Button(bottom, text="Delete", bg="red", fg="white", command=self.delete_selected).pack(side=LEFT, padx=5)
        Button(bottom, text="Exit", bg="black", fg="white", command=self.root.destroy).pack(side=LEFT, padx=5)

        self.selected_id = None

        self.load_records()
        self.root.mainloop()

    # ================= LOAD =================
    def load_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for record in get_all_records():
            self.tree.insert("", END, values=record)

    # ================= ADD =================
    def add_record(self):
        if not all([self.name_entry.get(), self.gender_combo.get(),
                    self.status_combo.get(), self.contact_entry.get()]):
            messagebox.showerror("Error", "Fill all fields")
            return

        insert_record(
            self.name_entry.get(),
            self.gender_combo.get(),
            self.status_combo.get(),
            self.contact_entry.get()
        )

        messagebox.showinfo("Success", "Record Added")
        self.load_records()

    # ================= SELECT =================
    def select_record(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if not values:
            return

        self.selected_id = values[0]

        self.name_entry.delete(0, END)
        self.name_entry.insert(0, values[1])

        self.gender_combo.set(values[2])
        self.status_combo.set(values[3])

        self.contact_entry.delete(0, END)
        self.contact_entry.insert(0, values[4])

    # ================= UPDATE =================
    def update_selected(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select record first")
            return

        update_record(
            self.selected_id,
            self.name_entry.get(),
            self.gender_combo.get(),
            self.status_combo.get(),
            self.contact_entry.get()
        )

        messagebox.showinfo("Success", "Updated")
        self.load_records()

    # ================= DELETE =================
    def delete_selected(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select record first")
            return

        if messagebox.askyesno("Confirm", "Delete this record?"):
            delete_record(self.selected_id)
            self.load_records()

    # ================= SEARCH =================
    def search_data(self):
        keyword = self.search_entry.get()

        self.tree.delete(*self.tree.get_children())

        for record in search_records(keyword):
            self.tree.insert("", END, values=record)

    # ================= FILTER =================
    def apply_filter(self):
        self.tree.delete(*self.tree.get_children())

        for record in filter_records(
            self.filter_gender.get(),
            self.filter_status.get()
        ):
            self.tree.insert("", END, values=record)