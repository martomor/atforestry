
import os
import requests
import json
import urllib.request



def get_mosaic_id(mosaic_name:str, session:requests.Session, url:str)->str:
    """Returns the mosaic id

    Args:
        mosaic_name (str): Name of the mosaic that we want to pull
        session (requests.Session): Requests session on Planet API
        url (str): Url of the planet api to fetch

    Returns:
        mosaic_id (str): Id of the mosaic to pull quads from
    """    

    parameters = {
    "name__is" :mosaic_name 
    }
    #make get request to access mosaic from basemaps API
    res = session.get(url, params = parameters)

    if res.status_code != 200:
        print('Mosaic not found!')
        exit

    mosaic = res.json()
    mosaic_id = mosaic['mosaics'][0]['id']
    return mosaic_id

def get_quads_from_mosaic(mosaic_id:str, bbox:str, session:requests.Session, url:str)->dict:
    """Gets quads from mosaic data

    Args:
        mosaic_id (str): Id of the mosaic that was pulled
        bbox (str): Bounding Box to target for quads
        session (requests.Session): Requests session on Planet API
        url (str): Url of the planet api to fetch

    Returns:
        quads = dict: dictionary with quads data
    """    
    #search for mosaic quad using AOI
    search_parameters = {
        'bbox': bbox,
        'minimal': True
    }
    #accessing quads using metadata from mosaic
    quads_url = "{}/{}/quads".format(url, mosaic_id)
    res = session.get(quads_url, params=search_parameters, stream=True)
    quads = res.json()
    #Store Mosaic metadata data
    for quad in quads['items']:
        quad['mosaic_id']=mosaic_id
        quad['master_bbox']=bbox

    return quads

def store_quads_metadata(quads:dict, path:str=os.path.join('..','data','planet_data','mosaics'))->bool:
    """Stores quads metadata

    Args:
        quads (dict): Quads data
        path (str): Path to save the metadata

    Returns:
        bool: Returns True
    """    

    #check if directory exists, if not create it
    if not os.path.exists(path):
            os.mkdir(path)

    data_path = os.path.join(path,'planet_metadata.json')

    #check if file exists
    if os.path.exists(data_path)==False:
        with open(os.path.join(data_path),'w+') as f:
            f.write(json.dumps([]))

    with open(data_path, "r+", encoding="utf-8") as f: #r+ is for reading and writing
        results = json.loads(f.read())
        if results == []:
            results.append(quads['items'])
            f.seek(0) #Move across bytes of the file to insure you are at the start
            f.write(json.dumps(results[0]))
        else:
            results.append(quads['items'])
            f.seek(0) #Move across bytes of the file to insure you are at the start
            f.write(json.dumps(results))

    return True

def download_quads_tiff(mosaic_id:str, quads:dict, path:str=os.path.join('..','data','planet_data','mosaics'))->bool:

     #check if directory exists, if not create it
    if not os.path.exists(path):
            os.mkdir(path)

    #Create directory with mosaic_name
    if not os.path.exists(os.path.join(path,mosaic_id)):
            os.mkdir(os.path.join(path,mosaic_id))

    items = quads['items']

    #Iterate dict and start saving
    for i in items:
        link = i['_links']['download']
        name = i['id']
        name = name + '.tiff'
        filename = os.path.join(path,mosaic_id,name)

        #checks if file already exists before s
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(link, filename)
    
    return True
        