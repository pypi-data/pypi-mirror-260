import os
import pandas as pd
from fpdf import FPDF
import glob
from pathlib import Path


def generate(invoices_path, pdfs_path, image_path, col1='product_id',
             col2='product_name', col3='amount_purchased',
             col4='price_per_unit', col5='total_price'):

    """
    This functino converts invoice Excel files into PDF invoices.
    :param invoices_path: The path where the Excel files are
    :param pdfs_path: The path where the PDF files will be stored
    :param image_path: The path of the company's image
    :param col1: The name of the first column on the PDF invoice, default=product_id
    :param col2: The name of the second column on the PDF invoice, default=product_name
    :param col3: The name of the third column on the PDF invoice, default=amount_purchased
    :param col4: The name of the forth column on the PDF invoice, default=price_per_unit
    :param col5: The name of the fifth column on the PDF invoice, default=total_price
    :return: A PDF invoice for each Excel invoice
    """
    filepaths = glob.glob(f'{invoices_path}/*.xlsx')

    for filepath in filepaths:
        pdf = FPDF(orientation='P', unit='mm', format='a4')
        pdf.add_page()

        filename = Path(filepath).stem
        invoice_nr, date = filename.split('-')

        pdf.set_font(family='Times', size=16, style='B')
        pdf.cell(w=50, h=8, txt=f'Invoice nr.{invoice_nr}', ln=1)

        pdf.set_font(family='Times', size=16, style='B')
        pdf.cell(w=50, h=8, txt=f'Date {date}', ln=1)
        pdf.ln(10)

        df = pd.read_excel(filepath, sheet_name='Sheet 1')

        # Add headers
        col_names = df.columns
        col_names = [x.replace('_',' ').title() for x in col_names]
        pdf.set_font(family='Times', size=10, style='B')
        pdf.set_draw_color(40,40,40)
        pdf.cell(w=30, h=8, txt=col_names[0], border=1)
        pdf.cell(w=70, h=8, txt=col_names[1], border=1)
        pdf.cell(w=35, h=8, txt=col_names[2], border=1)
        pdf.cell(w=25, h=8, txt=col_names[3], border=1)
        pdf.cell(w=30, h=8, txt=col_names[4], border=1, ln=1)

        # Add rows to the table
        for index, row in df.iterrows():
            pdf.set_font(family='Times', size=10)
            pdf.set_text_color(80,80,80)
            pdf.set_draw_color(40,40,40)
            pdf.cell(w=30, h=8, txt=str(row[col1]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[col2]), border=1)
            pdf.cell(w=35, h=8, txt=str(row[col3]), border=1)
            pdf.cell(w=25, h=8, txt=str(row[col4]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[col5]), border=1, ln=1)

        # Add the total price
        total_price = df['total_price'].sum()
        pdf.cell(w=30, h=8, txt='', border=1)
        pdf.cell(w=70, h=8, txt='', border=1)
        pdf.cell(w=35, h=8, txt='', border=1)
        pdf.cell(w=25, h=8, txt='', border=1)
        pdf.cell(w=30, h=8, txt=str(total_price), border=1, ln=1)

        # Add total sum sentence
        pdf.ln(10)
        pdf.set_font(family='Times', size=14, style='B')
        pdf.set_text_color(0,0,0)
        pdf.cell(w=0, h=8, txt=f'The total price is {total_price}', ln=1)

        # Add company name and logo
        pdf.cell(w=30, h=8, txt='PythonHow')
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f'{pdfs_path}/inv_nr{invoice_nr}.pdf')