import xlsxwriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import math

def generate_excel_report(capital_stack, lihtc_info, cash_flows, irr, dscr, filepath):
    workbook = xlsxwriter.Workbook(filepath)
    sheet = workbook.add_worksheet("Summary")

    bold = workbook.add_format({'bold': True})

    row = 0
    sheet.write(row, 0, "Capital Stack", bold)
    for key, value in capital_stack.items():
        row += 1
        sheet.write(row, 0, key)
        if type(value) is dict:
            start_row = row
            sub_cells = []
            for k, v in value.items():
                row += 1
                sheet.write(row, 1, k)
                sheet.write(row, 2, f"{v}")
                sub_cells.append(f"C{row + 1}")
            
            sheet.write(start_row, 1, f"={'+'.join(sub_cells)}")
        else:
            sheet.write(row, 1, f"{value}")
    
    row += 2
    sheet.write(row, 0, "LIHTC Disbursement", bold)
    for key, value in lihtc_info["Disbursement Schedule"].items():
        row += 1
        sheet.write(row, 0, key)
        sheet.write(row, 0, value)

    # row += 2
    # sheet.write(row, 0, "Add Test")
    # sheet.write(row, 1, "=2+2")
    # sheet.write(row, 2, f"=B{row + 1}+3")
    # sheet.write(row, 3, f"=C{row + 1}+3")

    row += 2
    sheet.write(row, 0, "Annual Cash Flows", bold)
    for i, cf in enumerate(cash_flows):
        sheet.write(row + i, 0, f"Year {i + 1}")
        sheet.write(row + i, 1, cf)
    
    row += len(cash_flows) + 2
    sheet.write(row, 0, "IRR", bold)
    sheet.write(row, 1, "NaN%") if math.isnan(irr) else sheet.write(row, 1, irr)
    row += 1
    sheet.write(row, 0, "DSCR", bold)
    sheet.write(row, 1, dscr)

    workbook.close()

def generate_pdf_report(capital_stack, lihtc_info,  cash_flows, irr, dscr, filepath):
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    x = 40
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Affordable Housing Finance Report")
    
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "Capital Stack")
    c.setFont("Helvetica", 10)
    for key, value in capital_stack.items():
        y -= 15
        if type(value) is dict:
            c.drawString(x + 20, y, f"{key}:")
            for k, v in value.items():
                y -= 15
                c.drawString(x + 40, y, f"{k}: ${v:,.2f}")
        else:
            c.drawString(x + 20, y, f"{key}: ${value:,.2f}")

    y -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "LIHTC Disbursement")
    c.setFont("Helvetica", 10)
    for key, value in lihtc_info["Disbursement Schedule"].items():
        y -= 15
        c.drawString(x + 20, y, f"{key}: ${value:,.2f}")

    y -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "Annual Cash Flows")
    c.setFont("Helvetica", 10)
    for i, cf in enumerate(cash_flows):
        y -= 15
        c.drawString(x + 20, y, f"Year {i + 1}: ${cf:,.2f}")
    
    y -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, f"IRR: {irr}%")
    y -= 15
    c.drawString(x, y, f"DSCR: {dscr}")
    
    c.save()