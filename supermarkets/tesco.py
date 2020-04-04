import json
import requests
import utils
from requests import get
from bs4 import BeautifulSoup
import sys, getopt


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
        print ("no informtion for bid", i)


# parse command line agrs to define the starting and ending points
def main(argv):
   startingpoint = ''
   endingpoint = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["spoint=1000","epoint=9999"])
   except getopt.GetoptError:
      print ('tesco.py -startingpoint <startingpoint> -endingpoint <endingpoint>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('tesco.py -startingpoint <startingpoint> -endingpoint <endingpoint>')
         sys.exit()
      elif opt in ("-startingpoint", "--spoint"):
         startingpoint = arg
      elif opt in ("-endingpoint", "--epoint"):
         endingpoint = arg


if __name__ == '__main__':
    host = 'https://www.tesco.com/store-locator/uk/?bid='
    # for i in range(1000,1011):
    start=int(sys.argv[2])
    end=int(sys.argv[4])
    for i in range(start,end):
        tesco_dict = getTescoShopInfo(host,i)
        print("=============RUNNING=============",i)
        print(tesco_dict)
    with open('../data/tesco.json', 'w') as json_file:
        json.dump(tesco_dict, json_file)