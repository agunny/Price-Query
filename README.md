# Price file error approval and logging

This python project was inspired by the current way of which invoices are approved for payment when there is a payment discrepancy between the purchase order raised on the system and the price on the latest price file which has been agreed upon by buyers and suppliers. 

## <a id="background"></a>Background

This project is designed to streamline the process of which invoices logged by purchase ledger clerks/account payable clerks (AP) and the buyers in purchasing. The current method requires AP to set aside the invoices that are due for query and log them to a portal in which purchasing are to review and approve. However, if the buyers are away or miss the approval which is set via email, then the payment process is delayed, possibly resulting in legal action and a soured relationship. These price file errors can arise through many avenues. A delay in the in update of prices, or if prices of the items update overnight, from when the PO is raised vs when the invoice is raised. Logging them in a google spreadsheet allows the purchasing to track the items which are currently being flagged and, via the use of in house generated price and quantity error reports, track the impact of the difference in items.

![image](https://github.com/agunny/Price-Query/assets/133648178/99c644cd-e696-40e8-ada7-79587d037442)
Current method of getting approvals.

## <a id="goals"></a>Goals

### Streamline process

To streamline the process that for accounts payable getting approvals/rejections to pay invoices.

### Easy monitoring and evidence

The back up of the spreadsheet to be clear as to why it was approved/rejected for audit and supplier purposes.

### Easy of use for all users

Ease of use for all users, from maintenance by admins, users and providing usable information to all parties

## **Features**
