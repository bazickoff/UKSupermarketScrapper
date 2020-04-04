import json
import requests
import utils
from requests import get
from bs4 import BeautifulSoup


# get the dic infor return for individual shop
def getTescoShopInfo(host, i):
    r = get(host+str(i))
    r = requests.get(host+str(i), cookies= r.cookies)
    soup= BeautifulSoup(r.text, 'html.parser')
    storeName=soup.find("h1",itemprop="name")
    if (storeName):
        storeName = storeName.text
        shopDetail = (soup.find("span", itemprop="streetAddress").text).split(",")
        shopAddress = ' '.join([str(elem) for elem in shopDetail[0:len(shopDetail) - 1]])
        shopPostcode = shopDetail[-1].strip()
        shopTel = soup.find("span", itemprop="telephone").text
        geolocation = utils.getGeoLocation(shopPostcode)

        dict = {
            'id': i,
            'sname': storeName,
            'address': shopAddress,
            'postcode': shopPostcode,
            'longitude': geolocation['longitude'],
            'latitude': geolocation['latitude'],
            'tel': shopTel
        }
        return dict
    else:
        return ("no informtion for bid", i)

if __name__ == '__main__':
    host = 'https://www.tesco.com/store-locator/uk/?bid='
    for i in range(1000,10000):
        tesco_dict = getTescoShopInfo(host,i)
        print("=============RUNNING=============")
    with open('../data/tesco.json', 'w') as json_file:
        json.dump(tesco_dict, json_file)