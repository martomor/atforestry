from keras.models import load_model

import os

def get_model():
    model_path = os.path.join('model','vgg16_trained.h5')
    model = load_model(model_path)
    return model


    
