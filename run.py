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
    formatted_date = datetime.strptime(
        invoice_date, '%d/%m/%Y').strftime('%b-%y')
    data = lpf_sheet.get_all_records()

    item_found = False
    buyer = None
    price_from_lpf = None

    for entry in data:
        if entry['ItemCode'] == item_code and entry['Site'] == site:
            price = entry.get(formatted_date)
            price_from_lpf = price
            buyer = entry.get('Buyer')
            if price:
                item_found = True
                return price, buyer, price_from_lpf
    if not item_found:
        return None, None, None

    return None, None, None


# Function to push Rejected and Approved invoices as per the report status
def push_to_approved_sheet(invoice_date, item_code, site, invoice_price, system_price, document_reference, buyer, price_from_lpf):
    status = "Approved - please pay"
    row = [invoice_date, document_reference, item_code, site,
           invoice_price, system_price, price_from_lpf, buyer, status]
    approved_sheet.append_rows([row])
    print("Succesfully added to the approved log")


def push_to_rejected_sheet(invoice_date, item_code, site, invoice_price, system_price, document_reference, buyer, price_from_lpf):
    status = "Rejected - please request credit from the supplier"
    row = [invoice_date, document_reference, item_code, site,
           invoice_price, system_price, price_from_lpf, buyer, status]
    rejected_sheet.append_rows([row])
    print("Succesfully added to the rejected log")

# Function to create sheet with either rejected or approved price differences, 1% difference allowed


def create_rejected_invoices_report():
    while True:
        print("\n=== Enter Invoice Details ===")
        invoice_date = input("Enter invoice date (dd/mm/yyyy): ")
        document_reference = input("Enter document reference: ")
        item_code = input("Enter item code: ").upper()
        site_input = input("Enter site: ").upper()
        site = "MW" if site_input == "MW" else "MANTON WOOD"
        invoice_price = input("Enter invoice price: ")
        system_price = input("Enter system price: ")

        correct_details = input("Are the details correct? (yes/no): ")
        if correct_details.lower() != 'yes':
            resubmit = input(
                "Do you want to resubmit or cancel (resubmit/cancel): ")
            if resubmit.lower() == 'cancel':
                break
            else:
                continue

        price, buyer, price_from_lpf = query_item_price_and_buyer(
            invoice_date, item_code, site)

        print("\n=== Report Results ===")
        if price is not None:
            if abs(float(invoice_price) - float(price)) <= 0.01:
                push_to_approved_sheet(invoice_date, item_code, site, invoice_price,
                                       system_price, document_reference, buyer, price_from_lpf)
                print("Invoice Approved, please pay")
                print("Invoice Date:", invoice_date)
                print("Item Code:", item_code)
                print("Site:", site)
                print("Invoice Price", invoice_price)
                print("System Price", system_price)
                print("Price from LPF:", price_from_lpf)
                print("Document Reference:", document_reference)
                print("Buyer", buyer)

            else:
                push_to_rejected_sheet(invoice_date, item_code, site, invoice_price,
                                       system_price, document_reference, buyer, price_from_lpf)
                print("Invoice Rejected. Please request credit")
                print("Invoice Date:", invoice_date)
                print("Item Code:", item_code)
                print("Site:", site)
                print("Invoice Price", invoice_price)
                print("System Price", system_price)
                print("Price from LPF:", price_from_lpf)
                print("Document Reference:", document_reference)
                print("Buyer", buyer)

        continue_input = input(
            "Do you want to submit another invoice? (yes/no): ")
        if continue_input.lower() != 'yes':
            break

# Debugging code below


create_rejected_invoices_report()
