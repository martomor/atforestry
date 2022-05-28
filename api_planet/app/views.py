import os
import json
import urllib.request
from app.utils import generate_raster_png_files, list_files_in_directory


PLANET_API_KEY = os.environ.get('PLANET_API_KEY')
PLANET_URL = "https://api.planet.com/basemaps/v1/mosaics"

class PlanetAPI():
    def __init__(self, api_key=PLANET_API_KEY, api_url=PLANET_URL):
        self.api_key = api_key
        self.api_url = api_url

class Mosaic():
    def __init__(self, name, date, session, url):
        self.name = name
        self.date = date
        self.session = session
        self.url = url
        self.api_name = name + '_'+ str(date)+ '_mosaic'

    def set_mosaic_id(self):
        """
        Returns mosaic_id if exists
        """

        #create headers
        parameters = {
        "name__is" :self.api_name
        }

        #request access to basemaps
        res = self.session.get(url = self.url, params = parameters)

        mosaic = res.json()
        mosaic_id = mosaic['mosaics'][0]['id']
        self.id = mosaic_id
        return None
    
    def get_quads_from_mosaic(self, bbox:str):
        """
        Gets quads from mosaic data

        Args:
            mosaic_id (str): Id of the mosaic that was pulled
            bbox (str): Bounding Box to target for quads

        Returns:
            quads = dict: dictionary with quads data
        """

        self.bbox = bbox

        search_parameters = {
        'bbox': bbox,
        'minimal': True
        }
        #accessing quads using metadata from mosaic
        quads_url = "{}/{}/quads".format(self.url, self.id)
        res = self.session.get(quads_url, params=search_parameters, stream=True)
        quads = res.json()
        #Store Mosaic metadata data
        for quad in quads['items']:
            quad['mosaic_id']=self.id
            quad['master_bbox']=self.bbox
            quad['mosaic_name']=self.name
            quad['mosaic_date']=self.date

        self.quads=quads
        return None

    def store_quads_metadata(self, path:str=os.path.join('..','data','planet_data','mosaics'))->bool:
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
                results.append(self.quads['items'])
                f.seek(0) #Move across bytes of the file to insure you are at the start
                f.write(json.dumps(results[0]))
            else:
                results.append(self.quads['items'])
                f.seek(0) #Move across bytes of the file to insure you are at the start
                f.write(json.dumps(results))

        return None

    def download_quads_tiff(self, path:str=os.path.join('..','data','planet_data','mosaics'))->bool:

        #check if directory exists, if not create it
        if not os.path.exists(path):
                os.mkdir(path)

        #Create directory with mosaic_name
        if not os.path.exists(os.path.join(path,self.id)):
                os.mkdir(os.path.join(path,self.id))

        items = self.quads['items']

        #Iterate dict and start saving
        for i in items:
            link = i['_links']['download']
            name = i['id']
            name = name + '.tiff'
            filename = os.path.join(path,self.id,name)

            #checks if file already exists before s
            if not os.path.isfile(filename):
                urllib.request.urlretrieve(link, filename)
        
        return True

    def generate_raster_files(self):
        tiff_files = list_files_in_directory(os.path.join('..','data','planet_data','mosaics',self.id))
        for tiff_file in tiff_files:
            generate_raster_png_files(tiff_file=tiff_file,mosaic_code=self.id, path='../data/planet_data/mosaics/')
        return None
            












