import requests
from lxml import etree, html
import json
import pandas as pd
import time
import random
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'If-None-Match': 'W/"ae080-P7buX4yALjJYkCg9WHY4e6F/THM"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get('https://www.myntra.com/saree', headers=headers)
page_source = response.text
html_string = html.fromstring(page_source)
product_data = html_string.xpath("//script[contains(text(),'window.__myx =')]//text()")

print(response.status_code)
excel_filename = 'Myntra_data.xlsx'

product_data_text = str(product_data[0])
item = product_data_text.strip("window.__myx =").strip(',"dataExpired":fa')
json_string = json.loads(item)
data_list = []
total_count = json_string["searchData"]["results"]['totalCount']
total_page = int(total_count) // 50
if total_page < 1:
    product_list = json_string["searchData"]["results"]["products"]
    product_data_dic = {}
    for index,prod_dict in enumerate(product_list):
        product_data_dic = {
            'Product Name': prod_dict['productName'],
            'Product Link': "https://www.myntra.com/"+str(prod_dict['landingPageUrl']),
            'Rating': prod_dict['rating'],
            'Rating Count':prod_dict['ratingCount'],
            'Price':prod_dict['mrp'],
            'Discounted Price':prod_dict['price'],
            'Discount':prod_dict['discountDisplayLabel'],
            'Size':prod_dict['sizes']
        }
        data_list.append(product_data_dic)
else:
    for page in range(1,51):
        url = 'https://www.myntra.com/saree?p='+str(page)
        time.sleep(random.randint(2, 4))
        response = requests.get(url, headers=headers)
        page_source = response.text
        html_string = html.fromstring(page_source)
        product_data = html_string.xpath("//script[contains(text(),'window.__myx =')]//text()")
        product_data_text = str(product_data[0])
        item = product_data_text.strip("window.__myx =").strip(',"dataExpired":fa')
        json_string = json.loads(item)
        product_list = json_string["searchData"]["results"]["products"]
        product_data_dic = {}
        print(url)
        print(response)
        for index, prod_dict in enumerate(product_list):
            product_data_dic = {
                'Product Name': prod_dict['productName'],
                'Product Link': "https://www.myntra.com/" + str(prod_dict['landingPageUrl']),
                'Rating': prod_dict['rating'],
                'Rating Count': prod_dict['ratingCount'],
                'Price': prod_dict['mrp'],
                'Discounted Price': prod_dict['price'],
                'Discount': prod_dict['discountDisplayLabel'],
                'Size': prod_dict['sizes']
            }
            data_list.append(product_data_dic)

    df = pd.DataFrame(data_list)
    df.to_excel(excel_filename)

print("File Saved Succesfully !!")
