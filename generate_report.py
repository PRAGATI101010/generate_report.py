# generate_report.py
# This script reads employee data from a CSV file,
# analyzes it, and generates a formatted PDF report.

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# --- STEP 1: READ DATA ---
data = pd.read_csv("sample_data.csv")

# --- STEP 2: ANALYZE DATA ---
summary = data.groupby("Department")["Salary"].agg(["mean", "max", "min", "count"]).reset_index()
summary.columns = ["Department", "Avg Salary", "Max Salary", "Min Salary", "Employee Count"]

# --- STEP 3: CREATE PDF REPORT ---
pdf_file = "Employee_Report.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4)
styles = getSampleStyleSheet()

elements = []

# Title
elements.append(Paragraph("<b>Employee Salary Report</b>", styles["Title"]))
elements.append(Spacer(1, 12))

# Summary text
elements.append(Paragraph("This report summarizes employee salaries by department.", styles["Normal"]))
elements.append(Spacer(1, 12))

# Table Data
table_data = [summary.columns.tolist()] + summary.values.tolist()

# Table Styling
table = Table(table_data, hAlign="LEFT")
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
]))

elements.append(table)
elements.append(Spacer(1, 24))
elements.append(Paragraph("Report generated using Python and ReportLab.", styles["Italic"]))

# --- STEP 4: BUILD PDF ---
doc.build(elements)

print(f"✅ Report generated successfully: {pdf_file}")
