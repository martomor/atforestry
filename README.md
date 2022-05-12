<h1 align="center">Atforestry</h1>

<p align="center">
    <img src="./assets/Atforestry_logo.JPG" alt="isolated" width="600"/>
</p>

> ## Monitoring deforestation using satellite images and computer vision models. 

Tracking deforestation is an essential problem to resolve to fight global warming. This web application monitors satellite images through computer vision models trained to detect critical changes on the earth's surface.

Our MLOps architecture has been set to predict deforestation based upon 2 simple steps: a) classify the type of cover land and (b) compare the cover land at different points in time to detect changes on the surface. 

## Classifying Cover Land

For this task, we are using the [Planet: Understanding the Amazon from Space](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space)  Kaggle competition [dataset](https://www.kaggle.com/competitions/planet-understanding-the-amazon-from-space/data). Additionally, we are leveraging the work done by [EKami](https://github.com/EKami/planet-amazon-deforestation), using a VGG16 convolutional model pre-trained with the Imagenet dataset and retrained to predict the type of cover land on top of the satellite images.

<p align="center">
    <img src="./assets/cover_land_planet.JPG" alt="isolated" width="600"/>
</p>

<h6 align="center">Planet: Understanding the Amazon from Space</h6>


## Comparing Cover Land

With the trained model and fetching satellite images from the [Planet API](https://developers.planet.com/docs/apis/), Atforestry API compares the type of cover land in 2 different periods. If the initial image had a rainforest type of cover land, such as **Primary**,  and the second one has a deforestation tag,  such as **agriculture**, **habitation** or **road**, we can signal  a deforestation case. We are leveraging the work done by [Luis Di Martino](https://github.com/lddm/forests-monitoring) in his article [Monitoring deforestation with open data and Machine Learning](https://medium.com/digital-sense-ai/monitoring-deforestation-with-open-data-and-machine-learning-part-2-c1be298c574b).

<p align="center">
    <img src="./assets/cover_land_change_example.JPG" alt="isolated" width="600"/>
</p>

<h6 align="center">Luis Di Martino - Monitoring deforestation with open data and Machine Learning</h6>

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







