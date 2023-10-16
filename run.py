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


# Function to push Rejected and Approved invoices as per the report status

def push_to_approved_sheet(invoice_date, item_code, site, invoice_price, system_price, document_reference):
    status = "Approved - please pay"
    row = [invoice_date, document_reference, item_code, site, invoice_price, system_price, status]
    approved_sheet.append_rows([row])

def push_to_rejected_sheet(invoice_date, item_code, site, invoice_price, system_price, document_reference):
    status = "Rejected - please request credit from the supplier"
    row = [invoice_date, document_reference, item_code, site, invoice_price, system_price, status]
    rejected_sheet.append_rows([row])

# Function to create sheet with either rejected or approved price differences, 1% difference allowed

def create_rejected_invoices_report(invoice_date, item_code, site, invoice_price, system_price, document_reference):
    approved_price = query_item_price(invoice_date, item_code, site)
    if approved_price:
        if abs(float(invoice_price) - float(approved_price)) <= 0.01:
            push_to_approved_sheet(invoice_date, item_code, site, invoice_price, system_price, document_reference)
        else:
            push_to_rejected_sheet(invoice_date, item_code, site, invoice_price, system_price, document_reference)


# Debugging code below
invoice_date = "15/10/2023"
item_code = "P34309"
site = "MANTON WOOD"
invoice_price = "0.2"
system_price = "0.0571"
document_reference = "000xxxxxx"
create_rejected_invoices_report(invoice_date, item_code, site, invoice_price, system_price, document_reference)