from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt

from database import get_all_records


class ChartsWindow:

    def __init__(self):

        self.window = Toplevel()
        self.window.title("Business Management Charts")
        self.window.geometry("400x300")

        Label(self.window,
              text="DATA VISUALIZATION DASHBOARD",
              font=("Arial", 14, "bold")).pack(pady=20)

        Button(self.window, text="Bar Chart",
               width=20, bg="blue", fg="white",
               command=self.bar_chart).pack(pady=10)

        Button(self.window, text="Pie Chart",
               width=20, bg="green", fg="white",
               command=self.pie_chart).pack(pady=10)

        Button(self.window, text="Line Graph",
               width=20, bg="orange",
               command=self.line_graph).pack(pady=10)

    # ================= BAR CHART =================
    def bar_chart(self):

        records = get_all_records()

        if not records:
            messagebox.showwarning("No Data", "No records available")
            return

        status_count = {"Active": 0, "Inactive": 0, "Pending": 0}

        for row in records:
            status = row[3]
            if status in status_count:
                status_count[status] += 1

        labels = list(status_count.keys())
        values = list(status_count.values())

        plt.figure(figsize=(7, 5))
        plt.bar(labels, values)

        plt.title("Customer Status Distribution")
        plt.xlabel("Status")
        plt.ylabel("Number of Records")

        plt.tight_layout()
        plt.show()

    # ================= PIE CHART =================
    def pie_chart(self):

        records = get_all_records()

        if not records:
            messagebox.showwarning("No Data", "No records available")
            return

        gender_count = {"Male": 0, "Female": 0, "Other": 0}

        for row in records:
            gender = row[2]
            if gender in gender_count:
                gender_count[gender] += 1
            else:
                gender_count["Other"] += 1

        labels = list(gender_count.keys())
        values = list(gender_count.values())

        plt.figure(figsize=(7, 5))
        plt.pie(values, labels=labels, autopct="%1.1f%%")

        plt.title("Gender Distribution")
        plt.show()

    # ================= LINE GRAPH =================
    def line_graph(self):

        records = get_all_records()

        if not records:
            messagebox.showwarning("No Data", "No records available")
            return

        monthly_counts = {}

        for row in records:

            date_str = str(row[5])

            # safe extraction (YYYY-MM)
            try:
                month = date_str[:7]
            except:
                continue

            monthly_counts[month] = monthly_counts.get(month, 0) + 1

        if not monthly_counts:
            messagebox.showwarning("No Data", "No valid dates found")
            return

        months = sorted(monthly_counts.keys())
        totals = [monthly_counts[m] for m in months]

        plt.figure(figsize=(8, 5))
        plt.plot(months, totals, marker="o")

        plt.title("Monthly Registration Trend")
        plt.xlabel("Month")
        plt.ylabel("Number of Records")
        plt.grid(True)

        plt.tight_layout()
        plt.show()