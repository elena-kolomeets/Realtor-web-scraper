## Realtor web scraper
A web scraping tool for automated apartment search on https://www.realtor.ca
built for personal use (feel free to modify and use it though!).


**The tool:**

* sends a post request with search parameters,
* receives json-like data, 
* extracts the necessary information about property,
* saves it into a dataframe and in .html and .xlsx files, 
* sends html table with results to the email address.
  

**Email addresses**

You can set email parameters by creating a file (which you should keep in the same folder) 
```email_credentials.txt``` with data in this order:
1. sender email address,
2. sender email password,
3. receiver email address.

Be careful not to commit this file to the version control system!


**The search parameters**

You can change search params by modifying the ```data.txt``` file (which you should keep in the same folder).

Default parameters I use:

50 newly listed apartments for rent in South Core district of Toronto, Ontario 
with 1+ bedrooms and a balcony, rent $2000-2300 CAD/month, in English, 
  sorted by date it was listed (from new to old).
