import os

import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdf_path, image_path, product_id, product_name, amount_purchased,
             price_per_unit, total_price):
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:
        filename = Path(filepath).stem
        invoice_num = filename.split("-")[0]

        date = filename.split("-")[1]

        pdf = FPDF(orientation="P", unit="mm", format="a4")
        pdf.add_page()

        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"invoice nr. {invoice_num}", ln=1)

        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Date. {date}", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")
        column = [column.replace("_", " ").title() for column in df.columns]
        pdf.set_font(family="Times", size=10, style="b")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, border=1, txt=column[0])
        pdf.cell(w=60, h=8, border=1, txt=column[1])
        pdf.cell(w=35, h=8, border=1, txt=column[2])
        pdf.cell(w=30, h=8, border=1, txt=column[3])
        pdf.cell(w=30, h=8, border=1, txt=column[4], ln=1)

        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, border=1, txt=str(row[product_id]))
            pdf.cell(w=60, h=8, border=1, txt=str(row[product_name]))
            pdf.cell(w=35, h=8, border=1, txt=str(row[amount_purchased]))
            pdf.cell(w=30, h=8, border=1, txt=str(row[price_per_unit]))
            pdf.cell(w=30, h=8, border=1, txt=str(row[total_price]), ln=1)

        sum = df[total_price].sum()
        pdf.cell(w=30, h=8, border=1, txt="")
        pdf.cell(w=60, h=8, border=1, txt="")
        pdf.cell(w=35, h=8, border=1, txt="")
        pdf.cell(w=30, h=8, border=1, txt="")
        pdf.set_font(family="Times", size=10, style="b")
        pdf.cell(w=30, h=8, border=1, txt=str(sum), ln=1)

        pdf.set_font(family="Times", size=10, style="b")
        pdf.cell(w=30, h=10, txt=f"The total due sum is {sum}")

        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt="Sher")
        pdf.image(image_path, w=10)
        if not os.path.exists(image_path):
            os.makedirs(pdf_path)
        pdf.output(f"{pdf_path}/{filename}.pdf")
