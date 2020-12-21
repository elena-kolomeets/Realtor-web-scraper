import functools
import json
from datetime import datetime, date
import pandas
import requests


def check(func):
    """
    decorator that will check when the request is made
    and will not allow to repeat it for next 24 hours
    """
    @functools.wraps(func)
    def wrapper_check(*args, **kwargs):
        now = datetime.now()


# realtor.ca
url = 'https://api2.realtor.ca/Listing.svc/PropertySearch_Post'
data = {'LatitudeMax': '43.65620',
        'LongitudeMax': '-79.33324',
        'LatitudeMin': '43.63135',
        'LongitudeMin': '-79.41430',
        'PropertyTypeGroupID': '1',
        'PropertySearchTypeId': '1',
        'TransactionTypeId': '3',
        'RentMin': '1800',
        'RentMax': '2300',
        'BedRange': '1-1',
        'BuildingTypeId': '17',
        'Currency': 'CAD',
        'CultureId': '1',
        'ApplicationId': '37'}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Chrome/87.0.4280.88 Safari/537.36'}
response = requests.post(url=url, data=data, headers=headers)

# with open('realtor_data.txt', mode='w', encoding='utf-8') as file:
#     file.write(response.text)
extract = json.loads(response.text)

# with open("realtor_data.txt") as file1:
#     extract = json.load(file1)

records = extract['Paging']['TotalRecords']
data['RecordsPerPage'] = records
response = requests.post(url=url, data=data, headers=headers)
extract = json.loads(response.text)
print(extract)

# the_list = list()
# results = extract["Results"]
# for result in results:
#     the_dict = dict()
#     try:
#         the_dict['Bedrooms'] = result['Building']['Bedrooms']
#     except:
#         the_dict['Bedrooms'] = 'Not given'
#     try:
#         the_dict['Bathrooms'] = result['Building']['BathroomTotal']
#     except:
#         the_dict['Bathrooms'] = 'Not given'
#     try:
#         the_dict['Description'] = result['PublicRemarks']
#     except:
#         the_dict['Description'] = 'Not given'
#     try:
#         the_dict['Rent'] = result['Property']['LeaseRent']
#     except:
#         the_dict['Rent'] = 'Not given'
#     try:
#         the_dict['Address'] = result['Property']['Address']['AddressText']
#     except:
#         the_dict['Address'] = 'Not given'
#     try:
#         the_dict['Link'] = 'https://www.realtor.ca' + result['RelativeURLEn']
#     except:
#         the_dict['Link'] = 'Not given'
#     the_list.append(the_dict)
# df = pandas.DataFrame(the_list)
# try:
#     df.to_csv('realtor_'+str(date.today())+'.csv')
# except:
#     print("Could not save to .csv file")

# make a table and save in pdf?


# torontorentals.com

# url1 = 'https://www.torontorentals.com'
# city = '/toronto/'
# pets = 'pet-friendly-rentals?'
# params = {
#     'beds': '1+',
#     'property-type': 'Condo',
#     'rent-max': '2300',
#     'rent-min': '1900'
# }
# url1 += city + pets + urlencode(params, doseq=True)
# headers1 = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                   'Chrome/87.0.4280.88 Safari/537.36'}
# response1 = requests.get(url1, headers1)
# parser = BeautifulSoup(response1.content, 'html.parser')
# results = parser.find_all('script', {'type': 'application/ld+json'})[2:102]
