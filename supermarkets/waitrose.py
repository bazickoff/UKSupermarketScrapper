# Develop by Vincent Zhang and GitRepo Owner

import json
import requests
import utils
from bs4 import BeautifulSoup


def getShopLocationAndCodeList(url):
    r = requests.get(url)
    r = requests.get(url, cookies= r.cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    # checker is the controller to decide the starting point for scrapping
    checker = None
    indexList = []
    LocList = []
    for link in soup.select('p a[href]'):
        if link.text=='Abergavenny':
            checker= True
    # Note: Barry Branch is closed, the html content still exists but page is blank
        if link.text == 'Barry':
            continue
    # This is because the waitrose website are not well formatted
    # some of its page has suffix as html.html instead of html
        if link.text == 'Greenwich' or link.text == 'Oakgrove-Milton Keynes' or link.text == 'Wells':
            LocList.append(link.text)
            indexList.append(link['href'][-13:-5])
            continue
    # The Peterborough branch is a bit weired the web link is code so have to manually add it
        if link.text == 'Peterborough':
            LocList.append(link.text)
            indexList.append('531')
            continue
        if checker:
            LocList.append(link.text)
            indexList.append(link['href'][-8:-5])
    return indexList, LocList


def getDetailedShopInfo(shopIndex):
    r = requests.get('https://www.waitrose.com/content/waitrose/en/bf_home/bf/'+shopIndex+'.html')
    r = requests.get('https://www.waitrose.com/content/waitrose/en/bf_home/bf/'+shopIndex+'.html', cookies= r.cookies)
    soup= BeautifulSoup(r.text, 'html.parser')
    shopDetail = soup.find("div", class_="col branch-details").select('p')
    return shopDetail

def ListProcesser(shopDetail):
    SingleListFinal=[]
    returnString=' '.join(map(str, shopDetail))
    replacedList=returnString.replace('<p>','').replace('\r','').replace('\n','').replace('\t','').replace('</p >','').replace('<br/>',';')
    newList = replacedList.strip().split(";")[0:-1]
    for i in newList:
        j = i.strip()
        SingleListFinal.append(j)
    return SingleListFinal

# Convert a single shop Deatil into a dictionary format
def jsonConverter(SingleShopDetail,id, shopName):
    geolocation =utils.getGeoLocation(SingleShopDetail[-2])
    #create an empty dict
    dict = {
        'id': id,
        'sname':shopName,
        'address': SingleShopDetail[0],
        'postcode': SingleShopDetail[-2],
        'longitude':geolocation['longitude'],
        'latitude': geolocation['latitude'],
        'tel': SingleShopDetail[-1],

    }
    return dict


if __name__ == '__main__':
    # Varaiable Declaration：
    url = 'https://www.waitrose.com/content/waitrose/en/bf_home/branch_finder_a-z.html'
    # shop id and shop name
    id = 0
    shopname = 'Waitrose & Partners'
    waitrose_dict ={'items': []}
    indexList = (getShopLocationAndCodeList(url))[0]
    locList = (getShopLocationAndCodeList(url))[1]
    for index in range(len(indexList)):
        id = id + 1
        sname = shopname + ' ' + locList[index]
        shopDetail = getDetailedShopInfo(indexList[index])
        SingleShopDeatil = ListProcesser(shopDetail)
        print(SingleShopDeatil)
        waitrose_dict['items'].append(jsonConverter(SingleShopDeatil,id,sname))

    with open('../data/waitrose.json', 'w') as json_file:
        json.dump(waitrose_dict, json_file)


