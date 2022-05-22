from fastapi import FastAPI
from app.views import download_quads_tiff, get_mosaic_id, get_quads_from_mosaic, store_quads_metadata, generate_raster_png_files
#from app.models import MosaicName
from app.utils import PlanetAPI, list_files_in_directory
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
async def fetch_mosacis_by_name_bbox(mosaic_name:str, bbox:str):
    """Downloads planet quads tiffs based on mosaic names and bounding box

    Args:
        mosaic_name (str): Name of the mosaic to fetch
        bbox (str): Bounding box of the mosic to fetch

    """    
    mosaic_id = get_mosaic_id(mosaic_name, session=session, url= planet_api.api_url)
    quads = get_quads_from_mosaic(mosaic_id=mosaic_id, bbox=bbox, session=session, url=planet_api.api_url)
    logger.info("Requesting quads tiffs")
    download_quads_tiff(mosaic_id=mosaic_id, quads=quads)
    logger.info("Pushing metadata")
    store_quads_metadata(quads=quads)
    return {'images downloaded!'}

@app.get("/v1/generate_raster_files")
async def generate_raster_files_by_mosaic_code(mosaic_name:str):
    """Creates rasters from tif files and stores them as png images

    Args:
        mosaic_name (str): mosaic name (has to be stored in system)

    """    
    logger.info("Requesting mosaic id")
    mosaic_id = get_mosaic_id(mosaic_name, session=session, url= planet_api.api_url)
    logger.info("Converting tiff to rgb files")
    tiff_files = list_files_in_directory(os.path.join('..','data','planet_data','mosaics',mosaic_id))
    for tiff_file in tiff_files:
        generate_raster_png_files(tiff_file=tiff_file,mosaic_code=mosaic_id, path='../data/planet_data/mosaics/')
    return {'files generated'}