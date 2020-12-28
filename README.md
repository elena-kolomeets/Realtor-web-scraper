## Realtor web scraper
A web scraping tool for automated rental apartment search on https://www.realtor.ca
built for personal use (feel free to modify and use it though!).


**The tool:**

* sends a post request with search parameters,
* receives json-like data, 
* extracts the necessary information about property,
* saves it into a dataframe and in .html and .xlsx files, 
* sends html table with results to the email address.


**The data extracted in the dataframe:**

* number of bedrooms,
* number of bathrooms,
* description,
* rent,
* address,
* link to the details page.


**The search parameters**

You can change search params by modifying the ```data.txt``` file (which you should keep in the same folder as the script).

To find out which parameters are available you can set needed filters and start the search on the website, 
then open Inspect page of the browser (right-click the page), open Network tab and, without reloading the page, 
you will see ```PropertySearch_Post``` element. Open it and find ```Form Data``` at the bottom. 
This is what you need to add in your ```data.txt```.

Alternatively, you can look up the API reference in the README of [this repo](https://github.com/Froren/realtorca).


**Email addresses**

You can set email parameters by creating a file (which you should keep in the same folder as the script) 
```email_credentials.txt``` with this data on each line in this order:
1. sender email address,
2. sender email password,
3. receiver email address.

Be careful not to commit this file to the version control system!