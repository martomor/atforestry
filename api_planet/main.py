from planet import api
import os
import requests
import json
import urllib.request


PLANET_API_KEY = os.getenv("PLANET_API_KEY")

API_URL = "https://api.planet.com/basemaps/v1/mosaics"

#setup session
session = requests.Session()

#authenticate
session.auth = (PLANET_API_KEY, "") 

#set params for search using name of mosaic
parameters = {
    "name__is" :"planet_medres_normalized_analytic_2020-06_2020-08_mosaic" # <= customize to your use case
}
#make get request to access mosaic from basemaps API
res = session.get(API_URL, params = parameters)
#response status code
print(res.status_code)

#print metadata for mosaic
mosaic = res.json()
print(json.dumps(mosaic, indent=2))

#get id
mosaic_id = mosaic['mosaics'][0]['id']
#get bbox for entire mosaic
mosaic_bbox = mosaic['mosaics'][0]['bbox']
#converting bbox to string for search params
string_bbox = ','.join(map(str, mosaic_bbox))

print('Mosaic id: '+ mosaic_id)
print('Mosaic bbox: '+ string_bbox)

#search for mosaic quad using AOI
search_parameters = {
    'bbox': string_bbox,
    'minimal': True
}
#accessing quads using metadata from mosaic
quads_url = "{}/{}/quads".format(API_URL, mosaic_id)
res = session.get(quads_url, params=search_parameters, stream=True)
print(res.status_code)

quads = res.json()
items = quads['items']
#printing an example of quad metadata
print(json.dumps(items[0], indent=2))

breakpoint()

#iterate over quad download links and saving to folder by id
for i in items:
    link = i['_links']['download']
    name = i['id']
    name = name + '.tiff'
    DIR = 'quads/' # <= a directory i created, feel free to customize
    filename = os.path.join(DIR, name)

    #checks if file already exists before s
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(link, filename)

