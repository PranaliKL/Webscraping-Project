import requests
from lxml import etree, html
import json
import pandas as pd
import time
import random
from datetime import date,datetime
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
date_str = date.today().strftime('%d-%b-%y')
db_name = f'Yatra_Bus_Data_{date_str}'
db = client[db_name]
bus_col = db.Bus_Data
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'currencyId=1; bm_mi=AA37E7182A5F024E43C25F6E4367623D~YAAQHl8sMbGhNLuPAQAAQlBNyBfnBsDKsX/k+z+LOriv1pD8k7lX1X0Fhi4QVSFEm8Te1bu3jzKvGtIQu6iNuIPp2Ic+IDSAF/kn3+0eIH7IrOb07f84tk85X6RhdMYlc9aUmC1/i0GXr06t90wMRsugqdwauSLuIUhJiebfwS7lJaVCQb3C6CPl3tpJNPAhKj9E29n4iaaBvE2k/L5bPdmQU2a7UBnp7WIomIotFG0PA6B93BJUggPTFeplSHAZHlG1ejq3DmhPG8GnSEkPYaT1g443UH+DGY9b7RooqwEq+DJOwBAoDekTbs6DKIX3BcB2UWhgWH5dVGRcZTMf9TV/aimQJA==~1; SessionVX=d0d09cb8-bfa5-4b99-a6e1-5c53277b3410; _gid=GA1.2.996591810.1717052461; ak_time=1717052462; __utma=39525803.1905930093.1717052461.1717052461.1717052461.1; __utmc=39525803; __utmz=39525803.1717052461.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=39525803.1.10.1717052461; ak_bmsc=4A8163D421AEAF726D05946B9A80CF8D~000000000000000000000000000000~YAAQHl8sMa6iNLuPAQAAC1dNyBfFcDjJigTIuFjYnyLekwsXVsWl0aJMXqJwwxkm0iA34+otibHm4swQd6gXu/Beyqboa/uOHdU5gG2acyoh/qgNcvtl7gvkFTkLbQ1aVPVwDgMcDhr8wAyzYZyMf6A/VGdKlZtMDh/zElLa0t/7WIt///KTlqagp5S5ldDO0Ugu0gtlJmziTRCeo9Nf8ac64Zcf2kGC4dmtKC1ZxUEN3/6i2ygyD4FNbRxL+5rUwQipge6KbqKT/DLjJRQ7XZRW5ppi0raGqaIqdMs8zWMMx5YabPfk54lkQvQ3F2voL1PeyEumRbL+p/HmyO4OS8pPvQnfGAHC3PgKgwvDMDCBSedZY+f8dpNmfnbXdnuzJ6/rabiIlOrA9VA9AGiEpT/wRGntFM85D+0Sna+hQi3GusD2rnPFgKJd16xuSQEMymFp+X4KK9+2LA88Q6s30BuHyR656wX99VdEwA==; _ga_DT1P1TBSQJ=GS1.2.1717052462.1.0.1717052462.60.0.0; _gcl_au=1.1.2126182191.1717052464; _ga=GA1.1.1905930093.1717052461; _fbp=fb.1.1717052465189.1968556815; _abck=B96D22CDCF7FA8DE42101B8D750BD770~0~YAAQHl8sMX/WNLuPAQAAsLlOyAtZKJZb6MlrLbjTiVq2QAf3LpMbCWU+yA0R2co2Z+kYsF5duxMatOVpttbZQTxzB3L88H3qoTW24ARIMwbO1T8F0UcA46jPQffxkqukHjZaDh5OU6sEuK/wJis5t8OFOf8nQN1hntBOyH9zoONn0Zks5y2uFPTJo1nk0mnnbVdN+FUhy4IQbuWTqfFCT8WeGVqMsvqSTytDEnjw7ydfzFY0I0c10en+hIclC5O6Har2+P9Ehl/FJJfulfrI/otWCSQObwodOYCS5+xVUHvkhOLEseqtXlw6Sfm6ie32CKUP+uEMb8mlKuKgroa6DIkhn4qWzQTSi3hJmS5T8Z0CGBIAJovsT7MmQg5U2O4jawhT8o6ZIppwQ7nPuDDfAriPX7f+GxV9tMP4Lw==~-1~-1~-1; bm_sv=9F13A2AC76176F49C8854FF499FB208D~YAAQHl8sMYDWNLuPAQAAsLlOyBeJBY28Huicyu9DSrhy7DI362x6K06PaJXMZA+QzWHBMW30lftmLMpdf3oqzmItTjbQUP6LagtQ2JD2Mia2xoDNFUrj2GXG0VO9ZRDRAvIGLbAmh0vwknV+pUBRBtvk16xiTUUHutuR8O/EtyET+zpUfxSgtQumJEuPqUZeoOpT0NIfrRN8UB5RaT3keXVAylecMIQGbf2BTenjuqp70iLx0jVklq11OCEVnCU=~1; bm_sz=A6D806CC67AAB603CDC83592F10C985C~YAAQHl8sMYHWNLuPAQAAsLlOyBeQq+yx7d3p8frg5af3wIasvBGImKXkaVts5KqTFgFK5QIAMX+5kby8K4yuP170WD3PofqAQ9VwYDbOdjhlKlUnZFXqRyeLxQIlSZqazmc5Ggqoy+H4ykl6rWpBWHxy2+O77AJBskp+wF1Ai8sY6E6cXjieuiINcUl/O7sQulfBzHFhvGCNPwi8OUOQHJuu2eFW//mB6lBM0OoKHxSX+jlVcFe1FdGDwvILTujs08mwaOP2gJ5DlLazhY33zpEt/5Ul8Ot2yfJO9XfVAKOjQD6zFyh4d+bzz/b/bsZj0BUTkbC2s42XSa5yBkLsQwpKUIOilgmKN6uYFregVeat5hwUL5D07bZIvy4++VfZd3Xh6SbVtKP+~3291460~3359798; _ga_V6YSFESQE4=GS1.1.1717052462.1.1.1717052552.0.0.0; _ga_WST37LHVJY=GS1.1.1717052464.1.1.1717052552.0.0.0; _ga_XHPXDWP1H4=GS1.1.1717052464.1.1.1717052552.60.0.0; RT="z=1&dm=yatra.com&si=1eb8fd1d-d903-41d8-9b4d-f44041f9274f&ss=lwswp85f&sl=1&tt=3zu&bcn=%2F%2F684d0d4a.akstat.io%2F"',
    'Referer': 'https://ebus.yatra.com/busview/busdesktop/search?src=Delhi&srcStnCode=YTDelhi&dest=Jaipur&destStnCode=YTJaipur&tt=O&ddate=2024-05-31&qty=1&source=fresco',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'corelationId': 'C943F2EC-AF81-4DE9-C44D-2169ED958E04',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# params = {
#     'src': 'Delhi',
#     'dest': 'Jaipur',
#     'ddate': '2024-05-31',
#     'tt': 'O',
#     'qty': '1',
#     'srcStnCode': 'YTDelhi',
#     'destStnCode': 'YTJaipur',
# }

params = {
    'src': 'Mumbai',
    'dest': 'Pune',
    'ddate': '2024-06-01',
    'tt': 'O',
    'qty': '1',
    'srcStnCode': 'YTMumbai',
    'destStnCode': 'YTPune',
}
date_str = date.today().strftime('%d-%b-%y')
excel_filename = f'yatra_bus_output_{date_str}.xlsx'
response = requests.get('https://ebus.yatra.com/businfo/busdesktop/search', params=params, headers=headers)
data_list =[]
page_responce = response.text
bus_data = json.loads(page_responce)
for bus in bus_data['result']['buses']:
    bus_data_dic = {}
    product_data_dic = {
        'Operator Code': bus['opId'],
        'Operator Name': bus['opNm'],
        'Departure Time': bus['dt'],
        'Arrival Time': bus['at'],
        'Total Duration': bus['du'],
        'Price': bus['fare'],
        'Bus Type': bus['bType'],
        'Seat Type': bus['st'],
        'Amenities': bus['amenities']
    }
    data_list.append(product_data_dic)

bus_col.insert_many(data_list)
df = pd.DataFrame(data_list)
df.to_excel(excel_filename)

print("File Saved Succesfully !!")

print(response.status_code)