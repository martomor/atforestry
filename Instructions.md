## Training Environment
Run the below on your bash terminaweb l

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