import time
import requests as re
import json
from bs4 import BeautifulSoup
sheypoor_url = 'https://www.sheypoor.com/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-%DA%A9%D8%A7%D8%B1%D8%B4%D9%86%D8%A7%D8%B3-%D8%B4%D8%A8%DA%A9%D9%87'
urls = [sheypoor_url, ]
def get_phone(url):
    ph = []
    s_headers = {
        "Host": "www.sheypoor.com",
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
    }
    r2 = re.get(url, headers=s_headers)

    r1_bs4 = BeautifulSoup(r2.text, 'html.parser')
    phones = r1_bs4.select("article > div > div > div > span")
    for i in phones:
        s2 = re.Session()
        s2.headers = {
            "Host": "www.sheypoor.com",
            "User-Agent": "curl/7.64.0",
            "Accept": "*/*",
        }
        url = 'https://www.sheypoor.com/api/web/listings/%s/number'%i['data-reveal-number']
        print('number id: %s'%i['data-reveal-number'])
        r1 = s2.get(url, allow_redirects=False)
        # print(r1.url)          
        try:
            print(json.loads(r1.text)['data']['mobileNumber'])
            ph.append(json.loads(r1.text)['data']['mobileNumber'])
            #with open('phonenumbers','a') as f:
            #    f.write(json.loads(r1.text)['data']['mobileNumber']+'\n')
        except:
            print("# Can`t get number :(")
        time.sleep(4.5)
        print("-----")
    return ph    
print(get_phone(sheypoor_url))
