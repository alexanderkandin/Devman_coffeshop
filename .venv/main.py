import json
import requests
import folium
from geopy import distance
from pprint import pprint
from flask import Flask


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


def coffeeshop_map():
    with open('map.html') as file:
      return file.read()


def main():
    with open('coffee.json', 'r', encoding='CP1251') as my_file:
        file_contents = json.loads(my_file.read())

    location = input('Укажите локацию: ')
    location_x,location_y = fetch_coordinates(apikey,location)
    your_location = (location_x,location_y)

    coffeeshop = []
    for coffee_shop in file_contents:
        coffe_name = coffee_shop['Name']
        coffe_coordinates = coffee_shop['geoData']['coordinates']
        your_distance = (distance.distance(your_location, coffe_coordinates).km)
        coffe = dict()
        coffe['title'] = coffe_name
        coffe['distance'] = your_distance
        coffe['latitude'] = coffe_coordinates[1]
        coffe['longitude'] = coffe_coordinates[0]
        coffeeshop.append(coffe)


    def get_coffe_dist(coffeeshop):
        return coffeeshop['distance']


    five_coffeeshop = sorted(coffeeshop,key=get_coffe_dist)[:6]
    m = folium.Map([55.75426247479371, 37.620765484236614], zoom_start=12)


    for i in five_coffeeshop:
        folium.Marker(
            location= [i['latitude'], i['longitude']],
            tooltip="Click me!",
            popup="Mt. Hood Meadows",
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)


    m.save('map.html')

    app = Flask(__name__)
    app.add_url_rule('/', 'hello', coffeeshop_map)
    app.run('0.0.0.0')


if __name__ == "__main__":
    main()



