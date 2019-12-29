import requests as re
import json
import time
from bs4 import BeautifulSoup
from getPhoneNumbers import get_phone

sheypoor_url = 'https://www.sheypoor.com/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-%DA%A9%D8%A7%D8%B1%D8%B4%D9%86%D8%A7%D8%B3-%D8%B4%D8%A8%DA%A9%D9%87'
urls = [sheypoor_url, ]

headers = {
    'User-Agent': 'test/1545',
}

s_headers = {
    "Host": "www.sheypoor.com",
    "User-Agent": "curl/7.64.0",
    "Accept": "*/*",
}

item_dic = {}

page_counter = 1
for u in urls:
    item_counter = 1
    item_dic['page%d'%page_counter] = {}

    print("--> page %d"%page_counter)

    r1_bs4 = BeautifulSoup(re.get(u, headers=headers).text, 'html.parser')

    phones = get_phone(u)
    item_head = r1_bs4.select("div > h2 > a")
    location = r1_bs4.select("article > div > p:nth-of-type(2)")

    c_counter = 0
    for m in item_head:
        each_item_url = m['href']
        req_to_each_item = re.get(each_item_url, headers=headers)
        req_to_each_item_bs4 = BeautifulSoup(req_to_each_item.text, 'html.parser')
        item_dic['page%d'%page_counter]['item%d'%item_counter] = {}
        item_dic['page%d'%page_counter]['item%d'%item_counter]['description'] = req_to_each_item_bs4.select("div > section > p:nth-of-type(1)")[0].text[:-25].strip()
        item_dic['page%d'%page_counter]['item%d'%item_counter]['location'] = location[c_counter].text.split()
        item_dic['page%d'%page_counter]['item%d'%item_counter]['phoneNumber'] = phones[c_counter]
        print("#%d"%item_counter)
        item_counter += 1
        c_counter += 1
    next_txt = "\n                            بعدی                        "
    next_page = (r1_bs4.select("nav > ul > li > a"))
    for k in next_page:
        if k.text == next_txt:
            urls.append(k['href'])
            break
    page_counter+=1
finnal_json = {'item_dic': item_dic}
with open('whole_items.json', 'w') as f:
    f.write(json.dumps(finnal_json))
