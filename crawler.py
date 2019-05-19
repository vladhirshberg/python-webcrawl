import re
import urllib2
from collections import OrderedDict

from bs4 import BeautifulSoup
import json

#get the web page data and parse it with BeautifulSoup
urlpath = 'https://weather.com/weather/hourbyhour/l/ISXX0026:1:IS'
page = urllib2.urlopen(urlpath)
soup = BeautifulSoup(page, 'html.parser')

#find the table and get the table data
table_html = soup.find(attrs={'class': 'twc-table'})
table_data = table_html.find_all('tr')

col_names = []
rows_data = []
#iterate over all the table rows(column names and actual data)
for table_row in table_data:
    tags = table_row.find_all('th')
    #get the column names
    for tag in tags:
        col_names.append(tag.text)

    data = table_row.find_all('td')
    row_data = []
    #get the actual data and create a list with each row as a seperate object
    for cell in data:
        if cell.text != u'':
            row_data.append(re.sub('[A-Z][a-z][a-z]$', '', cell.text.replace('\n', '').replace(u'\xb0', '')))

    #do not include the column names row as a data row
    if row_data != []:
        rows_data.append(row_data)

row_collection = []
#iterate over the data list to create the final array structure
for block in rows_data:
    row_json_data = {}
    row_order_list = []
    #match each data value with the coresponding column name
    for counter in range(1, len(block)):
        row_order_list.append((col_names[counter], block[counter]))
        #row_json_data.update({col_names[counter] : [block[counter]]})

    whole_row = {}
    #create an key value pair with the time as the key and all other data as the value
    #whole_row.update({block[0] : row_json_data})
    whole_row.update({block[0]: OrderedDict(row_order_list)})
    #add the data to the final array
    row_collection.append(whole_row)

#open a file and dump the data as a json into it
f = open("forcast_data.json", "w+")
json.dump(row_collection, f)
f.close()
