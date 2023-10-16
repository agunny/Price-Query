# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
spreadsheet = GSPREAD_CLIENT.open('LPFMWFY23')


lpf_sheet = spreadsheet.worksheet('LPF')
approved_sheet = spreadsheet.worksheet('Approved')
rejected_sheet = spreadsheet.worksheet('Rejected')


# Function to find the item and return price depending on item code and date of the invoice
def query_item_price(invoice_date, item_code, site):
    formatted_date = datetime.strptime(invoice_date, '%d/%m/%Y').strftime('%b-%y')
    data = lpf_sheet.get_all_records()

    item_found = False
    for entry in data:
        if entry['ItemCode'] == item_code and entry['Site'] == site:
            price = entry.get(formatted_date)
            if price:
                item_found = True
                return price
    if not item_found:
        return "Item not found in LPF file, please check the PO/Invoice for the item code again"
    return "Error in LPF sheet"

# Function to create sheet with either rejected or approved price differences

def create_rejected_invoices_report(invoice_date, item_code, site, invoice_price):
    approved_price = query_item_price(invoice_date, item_code, site)
    if approved_price:
        if abs(float(invoice_price) - float(approved_price)) <=0.01:
            return "Approved"
        else:
            return "Rejected"





# Debugging code below
invoice_date = "15/10/2023"
item_code = "P34309"
site = "MANTON WOOD"
invoice_price = "0.0543"
report_status = create_rejected_invoices_report(invoice_date, item_code, site, invoice_price)
print(f"Report Status: {report_status}")