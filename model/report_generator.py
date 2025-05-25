import xlsxwriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import math

def generate_excel_report(capital_stack, cash_flows, irr, dscr, filepath):
    workbook = xlsxwriter.Workbook(filepath)
    sheet = workbook.add_worksheet("Summary")

    row = 0
    sheet.write(row, 0, "Capital Stack")
    row += 1
    for key, value in capital_stack.items():
        sheet.write(row, 0, key)
        if type(value) is dict:
            for k, v in value.items():
                sheet.write(row, 1, k)
                sheet.write(row, 2, f"{v}")
        else:
            sheet.write(row, 1, f"{value}")
            row += 1
    
    row += 1
    sheet.write(row, 0, "IRR")
    sheet.write(row, 1, "NaN%") if math.isnan(irr) else sheet.write(row, 1, irr)
    row += 1
    sheet.write(row, 0, "DSCR")
    sheet.write(row, 1, dscr)

    # row += 2
    # sheet.write(row, 0, "Add Test")
    # sheet.write(row, 1, "=2+2")
    # sheet.write(row, 2, f"=B{row + 1}+3")
    # sheet.write(row, 3, f"=C{row + 1}+3")

    row += 2
    sheet.write(row, 0, "Annual Cash Flows")
    for i, cf in enumerate(cash_flows):
        sheet.write(row + i + 1, 0, f"Year {i + 1}")
        sheet.write(row + i + 1, 1, cf)
    
    workbook.close()

def generate_pdf_report(capital_stack, cash_flows, irr, dscr, filepath):
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    x = 40
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Affordable Housing Finance Report")
    
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(x, y, "Capital Stack")
    y -= 20
    for key, value in capital_stack.items():
        if type(value) is dict:
            c.drawString(x + 20, y, f"{key}:")
            y -= 15
            for k, v in value.items():
                c.drawString(x + 40, y, f"{k}: ${v:,.2f}")
                y -= 15
        else:
            c.drawString(x + 20, y, f"{key}: ${value:,.2f}")
            y -= 15
    
    y -= 15
    c.drawString(x, y, f"IRR: {irr}%")
    y -= 15
    c.drawString(x, y, f"DSCR: {dscr}")

    y -= 30
    c.drawString(x, y, "Annual Cash Flows")
    y -= 20
    for i, cf in enumerate(cash_flows):
        c.drawString(x + 20, y, f"Year {i + 1}: ${cf:,.2f}")
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 40
    
    c.save()