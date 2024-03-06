===================
Google Books Driver
===================

Load csv reports from google books. There are two options:

- Option 1: Input the google credentials and download the report csv 
  requested within a date range, it will return a string holding the csv report
  content.

- Option 2: Process a csv uploaded by the user with the option of checking
  the expected headers.


Note: If the option 1 is required it's recommended to use the option 2
afterwards to convert the result (string representation of the csv report) to
a list of dict.


Troubleshooting
===============

First of all if the scraping with Selenium is needed, 
we have to create a google account only for the purpose of this driver. 
Such account has to have a recovery email account to allow the Selenium
download the report freely.

It is very important to check the output the first time the driver is run as it 
is very likely that Google will block the 'suspicious' login attempt. If it
does, you will need to login with the same credentials you have provided the
driver with and review the security settings, Google will ask if you
were prevented from logging in and you must confirm so. Afterwards 
re-run the driver and it should work just fine.

The alternative to the scraping is uploading the report manually to bypass 
the scraping functionality as it could be unreliable because of the frontend
and/or backend changes from google.


Release Notes:
==============

[0.0.8] - 2024-03-05
---------------------
Changed
.......
    - Corrections of the README.rst to be more precise and enforced code
      styling corrections using flake8. 


[0.0.7] - 2024-02-27
---------------------
Changed
.......
    - Corrections bug account.


[0.0.6] - 2024-02-27
---------------------
Changed
.......
    - Rename of the variable 'gb_account' to 'account' in the fetch_report
      method.


[0.0.5] - 2024-01-12
---------------------
Changed
.......
    - Small correction of the driver interacting with google books.


[0.0.4] - 2023-10-09
---------------------
Added
.....
    - Allowed support for chrome and chromium browsers.
    - Allow a user to specify browser and user agent.

Changed
.......
    - Added driver options to improve report fetching reliability.


[0.0.1] - 2023-09-22
---------------------
Added
.......
    - Logic to initialise the webdriver.
    - Log in to Google.
    - Fetch a Google Play Books report.
