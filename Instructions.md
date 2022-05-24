## Training Environment

Run the below on your bash terminal. You will need this environment to run nooteboks 1 and 2 and for being able to train the model.

`conda env create -f ml_environment.yml`

`conda activate atforestry`

`pip install -r notebooks/requirements_ml.txt`


## Planet Environment
Run the below on your bash terminal. You will need this environment to run notebooks 3 and 4 and to service api_planet

`conda env create -f planet_environment.yml`

`conda activate atforestry-planet`

`pip install -r api_planet/requirements.txt`

## Inference Environment
For serving the API you will need to use another environment as python 3.5 doesn't work on FastAPI. You will use this one to run the api_inference. 

`virtualenv venv`

`source venv/bin/activate`

`pip install -r app_inference/requirements.txt`

