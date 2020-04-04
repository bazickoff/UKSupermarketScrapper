import json
import requests
import utils
from requests import get

# get shop's Geolocation, make it easy for later visualizaiton for GIS
def getGeoLocation(postcode):
    geolocation = {'longitude': float, 'latitude': float}
    data = requests.get('http://api.getthedata.com/postcode/' + postcode)
    geolocation['longitude'] =data.json()['data']['longitude']
    geolocation['latitude'] = data.json()['data']['latitude']
    return geolocation