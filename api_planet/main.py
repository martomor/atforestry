from fastapi import FastAPI
#from app.utils import download_quads_tiff, get_mosaic_id, get_quads_from_mosaic, store_quads_metadata, generate_raster_png_files
#from app.models import MosaicName
from app.views import PlanetAPI, Mosaic
import logging
from logging.config import dictConfig
from app.log_config import log_config
import os

dictConfig(log_config)

logger = logging.getLogger("planet_api_logger")

import requests

app = FastAPI(
    title='Atforesty Planet Web API pull',
    description='This API allows to fetch data from the Planet interface',
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Authenticates to Planet API

    Raises:
        SystemError: If no PLANET_API_KEY is provided
    """    
    global planet_api
    planet_api = PlanetAPI()
    #setup session
    global session
    session = requests.Session()
    #authenticate
    if planet_api.api_key == None:
        raise SystemError('environment PLANET_API_KEY variable is empty!!')

    session.auth = (planet_api.api_key, "") 


@app.get("/v1/check_planet_connection")
async def check_connection():
    """Checks connection status tu planet API

    Returns:
        res.status_code: Response should be 200
    """    
    parameters = {
    "name__is" :'planet_medres_normalized_analytic_2022-04_mosaic'
    }
    res = session.get(planet_api.api_url, params = parameters)
    logger.info("Health connection to Planet")
    return {'response':res.status_code,
            'description':'acces confirmed'
    }

@app.get("/v1/fetch_mosaics")
async def fetch_mosaics(mosaic_name:str, date:str, bbox:str):
    mosaic = Mosaic(name = mosaic_name, date=date, session=session, url=planet_api.api_url)
    #Set the mosaic id
    mosaic.set_mosaic_id()
    #Get the quads
    mosaic.get_quads_from_mosaic(bbox=bbox)
    logger.info("Requesting quads tiffs")
    #Download quads
    mosaic.download_quads_tiff()
    logger.info("Pushing metadata")
    #Store metadata
    mosaic.store_quads_metadata()   
    logger.info("Converting tiff to rgb files")    
    #Store rgb rasters
    mosaic.generate_raster_files()
    logger.info("Files Generated")    
    return {'status': 'success'}




