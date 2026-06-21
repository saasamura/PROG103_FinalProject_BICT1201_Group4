from tkinter import *
from tkinter import messagebox

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime
import os

from database import get_all_records


class ReportWindow:

    def __init__(self):

        self.window = Toplevel()
        self.window.title("PDF Reports")
        self.window.geometry("400x300")

        Label(self.window,
              text="PDF REPORT GENERATION",
              font=("Arial", 14, "bold")).pack(pady=20)

        Button(self.window, text="Generate Weekly Report",
               width=25, command=self.weekly_report).pack(pady=10)

        Button(self.window, text="Generate Monthly Report",
               width=25, command=self.monthly_report).pack(pady=10)

        Button(self.window, text="Generate Yearly Report",
               width=25, command=self.yearly_report).pack(pady=10)

    # ================= WEEKLY =================
    def weekly_report(self):
        self.generate_pdf("Weekly_Report.pdf", "Weekly Business Report")

    # ================= MONTHLY =================
    def monthly_report(self):
        self.generate_pdf("Monthly_Report.pdf", "Monthly Business Report")

    # ================= YEARLY =================
    def yearly_report(self):
        self.generate_pdf("Yearly_Report.pdf", "Yearly Business Report")

    # ================= PDF GENERATOR =================
    def generate_pdf(self, filename, title):

        records = get_all_records()

        if not records:
            messagebox.showwarning("No Data", "No records found to generate report")
            return

        # Create folder for reports
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)

        doc = SimpleDocTemplate(filepath)
        styles = getSampleStyleSheet()

        content = []

        content.append(Paragraph(title, styles['Title']))
        content.append(Spacer(1, 20))

        content.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                styles['Normal']
            )
        )

        content.append(Spacer(1, 20))

        content.append(
            Paragraph(f"Total Records: {len(records)}", styles['Normal'])
        )

        content.append(Spacer(1, 20))

        for row in records:

            text = (
                f"<b>ID:</b> {row[0]} | "
                f"<b>Name:</b> {row[1]} | "
                f"<b>Gender:</b> {row[2]} | "
                f"<b>Status:</b> {row[3]} | "
                f"<b>Contact:</b> {row[4]} | "
                f"<b>Date:</b> {row[5]}"
            )

            content.append(Paragraph(text, styles['Normal']))
            content.append(Spacer(1, 10))

        doc.build(content)

        messagebox.showinfo(
            "Success",
            f"Report saved in /reports/{filename}"
        )