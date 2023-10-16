# Price file error approval and logging

This python project was inspired by the current way of which invoices are approved for payment when there is a payment discrepancy between the purchase order raised on the system and the price on the latest price file which has been agreed upon by buyers and suppliers. 


## Contents

* [Background](#background)
* [Goals](#goals)
* [Features](#features)
* [Technologies Used](#tech)
* [Credits](#Credits)




## <a id="background"></a>Background

This project is designed to streamline the process of which invoices logged by purchase ledger clerks/account payable clerks (AP) and the buyers in purchasing. The current method requires AP to set aside the invoices that are due for query and log them to a portal in which purchasing are to review and approve. However, if the buyers are away or miss the approval which is set via email, then the payment process is delayed, possibly resulting in legal action and a soured relationship. These price file errors can arise through many avenues. A delay in the in update of prices, or if prices of the items update overnight, from when the PO is raised vs when the invoice is raised. Logging them in a google spreadsheet allows the purchasing to track the items which are currently being flagged and, via the use of in house generated price and quantity error reports, track the impact of the difference in items. Essentially the code works like a like multiple vlookups all at once.

Also having worked in accounts payable and managing the current price portal gave me a great understanding as to how the process is supposed to work, therefore I knew already what was needed and how it’s going to be used by others.

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

Data transferred into a google sheet, which can be read only to people adding and only certain people allowed to make edits. This still allows for information to be extrapolated via the use of pivot tables or simply using filters to identify which items are causing the biggest hits and why.
Filters allow for AP to quicky relay information onto suppliers as to why the invoices where rejected.
![image](https://github.com/agunny/Price-Query/assets/133648178/fa6d21ad-b3ae-4622-96ad-42352569ce97)


## <a id="tech"></a>Technologies Used

**Github** - Used for storage and version control.\
**Codeanywhere** - The IDE used for editing my site and pushing changes.\
**Python** - Used python 3 via terminal to preview the results of changes to the code.\
**Heroku** - Used for deployment and final version testing.\

### Deployment

I deployed my website via the use of Heroku. [https://dashboard.heroku.com/apps]

## Testing

![image](https://github.com/agunny/Price-Query/assets/133648178/ee6433d2-6016-4bb0-96ec-4860efc284ff)
[https://extendsclass.com/python-tester.html]

PEP8 linter was used to verify the code has no issues and passed.


### Bugs

One of the bugs encounted was the fact that the values for the item prices was hard coded in so the values weren't numbers but in fact text therefore when trying to pull numbers, it threw an errorm. This was simply fixed via the use of find and place.
![image](https://github.com/agunny/Price-Query/assets/133648178/18745502-74da-421f-b0f8-189d21254679)

Another issue was the dates in the headings was "Price Dec 23" which wouldn't correlate with the fact that I was searching for the month and year which wouldn’t match. This, again, was solved with a simple find and replace.

No other buds remaining.

## <a id="credits"></a>Credits

<https://www.programiz.com/python-programming/datetime/strptime> 
The link above was used to extract the date in the format that I wanted to use to find the price corresponding to the month.

<https://stackoverflow.com/questions/15707532/import-datetime-v-s-from-datetime-import-datetime>
The link above was used to allow formatting of the date.


### Content
The information for the LPF was provided to me by Greencore. This file is used for accounts payable and purchasing to stay in the loop as to what the prices have already been agreed to. The names of people where stripped out prevent the GDPR leaks.

### Future implementations

In the future, I would like to adapt this to be used by multiple sites either all feeding into the same spreadsheet or keeping them separate. This would require some upkeep as each site as their own individual price sheet as costs vary per site and items vary per site.









