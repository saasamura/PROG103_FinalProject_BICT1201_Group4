from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt

from database import get_all_records


class ChartsWindow:

    def __init__(self):

        self.window = Toplevel()

        self.window.title("Business Management Charts")
        self.window.geometry("400x300")

        Label(
            self.window,
            text="DATA VISUALIZATION DASHBOARD",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

        Button(
            self.window,
            text="Bar Chart",
            width=20,
            bg="blue",
            fg="white",
            command=self.bar_chart
        ).pack(pady=10)

        Button(
            self.window,
            text="Pie Chart",
            width=20,
            bg="green",
            fg="white",
            command=self.pie_chart
        ).pack(pady=10)

        Button(
            self.window,
            text="Line Graph",
            width=20,
            bg="orange",
            command=self.line_graph
        ).pack(pady=10)

    # ==========================
    # BAR CHART
    # ==========================

    def bar_chart(self):

        records = get_all_records()

        active = 0
        inactive = 0
        pending = 0

        for row in records:

            if row[3] == "Active":
                active += 1

            elif row[3] == "Inactive":
                inactive += 1

            elif row[3] == "Pending":
                pending += 1

        labels = ["Active", "Inactive", "Pending"]
        values = [active, inactive, pending]

        plt.figure(figsize=(7, 5))
        plt.bar(labels, values)

        plt.title("Records by Status")
        plt.xlabel("Status")
        plt.ylabel("Number of Records")

        plt.show()

    # ==========================
    # PIE CHART
    # ==========================

    def pie_chart(self):

        records = get_all_records()

        male = 0
        female = 0
        other = 0

        for row in records:

            if row[2] == "Male":
                male += 1

            elif row[2] == "Female":
                female += 1

            else:
                other += 1

        labels = ["Male", "Female", "Other"]

        values = [male, female, other]

        plt.figure(figsize=(7, 5))

        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%"
        )

        plt.title("Gender Distribution")

        plt.show()

    # ==========================
    # LINE GRAPH
    # ==========================

    def line_graph(self):

        records = get_all_records()

        monthly_counts = {}

        for row in records:

            month = row[5][:7]

            if month not in monthly_counts:
                monthly_counts[month] = 1

            else:
                monthly_counts[month] += 1

        months = list(monthly_counts.keys())
        totals = list(monthly_counts.values())

        plt.figure(figsize=(8, 5))

        plt.plot(
            months,
            totals,
            marker="o"
        )

        plt.title("Monthly Record Registrations")
        plt.xlabel("Month")
        plt.ylabel("Records")

        plt.grid(True)

        plt.show()