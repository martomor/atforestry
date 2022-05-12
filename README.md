<h1 align="center">Atforestry</h1>

<p align="center">
    <img src="./assets/Atforestry_logo.JPG" alt="isolated" width="600"/>
</p>

> ### Monitoring deforestation using satellite images and computer vision models. 

Tracking deforestation is an essential problem to resolve in order to fight global warming. We have taken 

## Training Environment
Run the below on your bash terminal

`conda env create -f environment.yml`

`conda activate python35`

`pip install -r requirements.txt`

## Inference Environment
For serving the APIs you will need to use another environment as python 3.5 doesn't work on FastAPI. You can use virtualenv for that:

`virtualenv venv`

`source venv/bin/activate`

`pip install -r app/requirements.txt`

After installing all dependencies in virtualenv you can run uvicorn:

`uvicorn api.main:app`







