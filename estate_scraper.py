import ast
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import date
import smtplib
import ssl
import pandas
import requests


def send_request():
    """
    Send request to realtor.ca to get a list of 50 newest listings
    of real estate properties with characteristics set in data.txt file.
    """
    url = 'https://api2.realtor.ca/Listing.svc/PropertySearch_Post'
    try:
        with open('data.txt', mode='r', encoding='utf-8') as file:
            data = ast.literal_eval(file.read())
    except:
        data = {'LatitudeMax': '43.65531',
                'LongitudeMax': '-79.33186',
                'LatitudeMin': '43.62916',
                'LongitudeMin': '-79.41262',
                'Sort': '6-D',
                'PropertyTypeGroupID': '1',
                'PropertySearchTypeId': '1',
                'TransactionTypeId': '3',
                'RentMin': '2000',
                'RentMax': '2300',
                'BedRange': '1-0',
                'BuildingTypeId': '17',
                'Keywords': 'balcony',
                'Currency': 'CAD',
                'RecordsPerPage': '50',
                'CultureId': '1',
                'ApplicationId': '37'}
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/87.0.4280.88 Safari/537.36'}
    # get 50 newest records
    try:
        response = requests.post(url=url, data=data, headers=headers)
        extract = json.loads(response.text)
        return extract
    except:
        print('Could not send the request.')
        return None


def extract_data(extract):
    """Extract necessary info about property and store it in a dataframe."""
    the_list = list()
    try:
        results = extract["Results"]
        for result in results:
            the_dict = dict()
            try:
                the_dict['Bedroom'] = result['Building']['Bedrooms']
            except:
                the_dict['Bedroom'] = 'Not given'
            try:
                the_dict['Bathroom'] = result['Building']['BathroomTotal']
            except:
                the_dict['Bathroom'] = 'Not given'
            try:
                the_dict['Description'] = result['PublicRemarks']
            except:
                the_dict['Description'] = 'Not given'
            try:
                the_dict['Rent'] = result['Property']['LeaseRent']
            except:
                the_dict['Rent'] = 'Not given'
            try:
                the_dict['Address'] = result['Property']['Address']['AddressText']
            except:
                the_dict['Address'] = 'Not given'
            try:
                the_dict['Link'] = 'https://www.realtor.ca' + result['RelativeURLEn']
            except:
                the_dict['Link'] = 'Not given'
            the_list.append(the_dict)
        df = pandas.DataFrame(the_list)
        return df
    except:
        print('Could not extract data about property.')
        return None


def save_files(df):
    """Save extracted data into .xlsx and .html files."""
    if df is not None:
        try:
            with pandas.ExcelWriter('realtor-'+str(date.today())+'.xlsx') as writer:
                df.to_excel(writer)
        except:
            print('Could not save to Excel file')
        try:
            df.to_html('realtor-'+str(date.today())+'.html', justify='center', index_names=False, render_links=True)
        except:
            print('Could not save to HTML file')


def send_email(df):
    """Send an email with web scraping results as html table."""
    if df is not None:
        try:
            with open('email_credentials.txt', mode='r', encoding='utf-8') as file2:
                sender_email = file2.readline().strip()
                sender_pass = file2.readline().strip()
                receiver_email = file2.readline().strip()
        except:
            print('No file with email credentials.')
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Your realtor.ca search results '+str(date.today())
        message['From'] = sender_email
        message['To'] = receiver_email

        # Create the plain-text and HTML version of the message
        text = """\
        Hi,
        
        Here should be fresh real estate search results from https://www.realtor.ca.
        If you do not see them, your email client does not display HTML content by default.   
        You can turn it on or use the .html or .xlsx files created with the same results!
        
        Elena Kolomeets
        https://github.com/elena-kolomeets"""

        # add results table to the end of html
        html = """\
        <html>
          <body>
            <p>Hi,</br>
               Here are fresh real estate search results from <a href="https://www.realtor.ca" target="_blank">Realtor Canada</a> 
               </br>
               (Made by <a href="https://github.com/elena-kolomeets" target="_blank">Elena Kolomeets</a>)
            </p>
          </body>
        </html>
        """+'\n'+df.to_html(justify='center', index_names=False, render_links=True)

        # Turn these into plain/html MIMEText objects and add to MIMEMultipart message
        message.attach(MIMEText(text, 'plain'))
        message.attach(MIMEText(html, 'html'))

        # Create secure connection with server and send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                try:
                    server.login(sender_email, sender_pass)
                except:
                    print('Could not login in the sender email.')
                try:
                    server.sendmail(sender_email, receiver_email, message.as_string())
                except:
                    print('Could not send an email to '+receiver_email+'.')
        except:
            print('Could not connect to the server to send an email.')
    else:
        print('No dataframe to save in files.')


def main():
    """
    A web scraping tool for automated apartment search on https://www.realtor.ca
    for personal use (feel free to modify and use it though!);
    json-like data is received with a post request, necessary results are
    extracted into a dataframe and saved in .html and .xlsx files,
    html table is also sent to the personal email address.
    """
    scraped_data = send_request()
    extracted_data = extract_data(scraped_data)
    save_files(extracted_data)
    send_email(extracted_data)


if __name__ == '__main__':
    main()
