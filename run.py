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


# Function to find the item, return price, and buyer depending on item code and site
def query_item_price_and_buyer(invoice_date, item_code, site):
    formatted_date = datetime.strptime(invoice_date, '%d/%m/%Y').strftime('%b-%y')
    data = lpf_sheet.get_all_records()

    item_found = False
    buyer = None
    for entry in data:
        if entry['ItemCode'] == item_code and entry['Site'] == site:
            price = entry.get(formatted_date)
            buyer = entry.get('Buyer')
            if price:
                item_found = True
                return price, buyer
    if not item_found:
        return None, None

    return None, None


# Function to push Rejected and Approved invoices as per the report status
def push_to_approved_sheet(invoice_date, item_code, site, invoice_price, system_price, document_reference, buyer):
    status = "Approved - please pay"
    row = [invoice_date, document_reference, item_code, site, invoice_price, system_price, buyer, status]
    approved_sheet.append_rows([row])

def push_to_rejected_sheet(invoice_date, item_code, site, invoice_price, system_price, document_reference, buyer):
    status = "Rejected - please request credit from the supplier"
    row = [invoice_date, document_reference, item_code, site, invoice_price, system_price, buyer, status]
    rejected_sheet.append_rows([row])

# Function to create sheet with either rejected or approved price differences, 1% difference allowed
def create_rejected_invoices_report():
    print("\n=== Enter Invoice Details ===")
    invoice_date = input("Enter invoice date (dd/mm/yyyy: ")
    item_code = input("Enter item code: ").upper()
    site = input("Enter site: ").upper()
    invoice_price = input("Enter invoice price: ")
    system_price = input("Enter system price: ")
    document_reference = input("Enter document reference: ")

    price, buyer = query_item_price_and_buyer(invoice_date, item_code, site)
    
    print("\n=== Report Results ===")
    if price is not None:
        if abs(float(invoice_price) - float(price)) <= 0.01:
            push_to_approved_sheet(invoice_date, item_code, site, invoice_price, system_price, document_reference, buyer)
            print("Invoice Approved. Details:")
            print("Invoice Date:", invoice_date)
            print("Item Code:", item_code)
            print("Site:", site)
            print("Invoice Price", invoice_price)
            print("System Price", system_price)
            print("Document Reference:", document_reference)
            print("Buyer", buyer)

        else:
            push_to_rejected_sheet(invoice_date, item_code, site, invoice_price, system_price, document_reference, buyer)
            print("Invoice Rejected. Details:")
            print("Invoice Date:", invoice_date)
            print("Item Code:", item_code)
            print("Site:", site)
            print("Invoice Price", invoice_price)
            print("System Price", system_price)
            print("Document Reference:", document_reference)
            print("Buyer", buyer)

# Debugging code below

create_rejected_invoices_report()