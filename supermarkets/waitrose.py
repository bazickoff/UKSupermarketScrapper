# Develop by Vincent Zhang and GitRepo Owner

import requests
from requests import get
from bs4 import BeautifulSoup

# Varaiable Declaration：
url = 'https://www.waitrose.com/content/waitrose/en/bf_home/branch_finder_a-z.html'
LocList = []
# checker is the controller to decide the starting point for scrapping
def getShopLocationAndCodeList(url):
    r = requests.get(url)
    r = requests.get(url, cookies= r.cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    checker = None
    indexList = []

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
        if checker:
            LocList.append(link.text)
            indexList.append(link['href'][-8:-5])
    return indexList


def getDetailedShopInfo(shopIndex):
    r = get('https://www.waitrose.com/content/waitrose/en/bf_home/bf/'+shopIndex+'.html')
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

if __name__ == '__main__':
    indexList = getShopLocationAndCodeList(url)
    for index in indexList:
        shopDetail = getDetailedShopInfo(index)
        print(ListProcesser(shopDetail))


