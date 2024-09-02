import json
import requests
import Folium
from geopy import distance
from pprint import pprint

apikey = 'b222220d-81ea-4425-bff5-8f6f8fe47f65'

def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


location = input('Укажите город: ')
location_x,location_y = fetch_coordinates(apikey,location)
your_location = (location_x,location_y)


wellington = (-41.32, 174.81)
salamanca = (40.96, -5.50)
x= (distance.distance(wellington, salamanca).km)


with open('coffee.json', 'r', encoding='CP1251') as my_file:
    file_contents = json.loads(my_file.read())

coffeeshop = []

for index, coffee_shop in enumerate(file_contents, start=1):
    coffe_name = coffee_shop['Name']
    coffe_coordinates = coffee_shop['geoData']['coordinates']
    your_distance = (distance.distance(your_location, coffe_coordinates).km)
    coffe = dict()
    coffe['title'] = coffe_name
    coffe['distance'] = your_distance
    coffe['latitude'] = coffe_coordinates[1]
    coffe['longitude'] = coffe_coordinates[0]
    coffeeshop.append(coffe)
# pprint(coffeeshop)


def get_coffe_dist(coffeeshop):
    return coffeeshop['distance']


min_dist = sorted(coffeeshop,key=get_coffe_dist)[:5]


    # print(coffe_name,your_distance,coffe_coordinates[0],coffe_coordinates[1])


