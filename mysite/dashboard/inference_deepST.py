from keras.models import load_model
from keras.engine.topology import Layer
from Preprocessor import Preprocessor
from GIS_processor import GIS_processor
import datetime as dt
import keras.backend as K
import numpy as np
import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class iLayer(Layer):
    def __init__(self, **kwargs):
        super(iLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        initial_weight_value = np.random.random(input_shape[1:])
        self.W = K.variable(initial_weight_value)
        self.trainable_weights = [self.W]

    def call(self, x, mask=None):
        return x * self.W

    def compute_output_shape(self, input_shape):
        return input_shape


weights_file = os.path.dirname(os.path.abspath(__file__)) + "/weights/DeepST_150x150_2_flow.h5"
model = load_model(weights_file, custom_objects={'iLayer': iLayer()})

preprocessor = Preprocessor()
gis_processor = GIS_processor()

infer_time = dt.datetime.now().replace(microsecond=0, second=0, minute=0) + dt.timedelta(hours=1)

df_x = preprocessor.make_sample(infer_time)
y_pred = model.predict([df_x[:, 0, :], df_x[:, 1, :], df_x[:, 2, :]])


pm25Pred = y_pred[:, :, :, 0].reshape(150, 150)
pm25Pred_data = []
for index, x in np.ndenumerate(pm25Pred):
    gridy = 254 - (index[0] + 100)
    gridx = index[1]
    lat, lon = gis_processor.gridToMap(x=gridx, y=gridy)
    pm25Pred_data.append([lat, lon, x])
pm25Pred = pd.DataFrame(pm25Pred_data, columns=['lat', 'lon', 'predValue'])
pm25Pred['type'] = 'pm25'

pm10Pred = y_pred[:, :, :, 1].reshape(150, 150)
pm10Pred_data = []
for index, x in np.ndenumerate(pm10Pred):
    gridy = 254 - (index[0] + 100)
    gridx = index[1]
    lat, lon = gis_processor.gridToMap(x=gridx, y=gridy)
    pm10Pred_data.append([lat, lon, x])
pm10Pred = pd.DataFrame(pm10Pred_data, columns=['lat', 'lon', 'predValue'])
pm10Pred['type'] = 'pm10'

predData = pd.concat([pm25Pred, pm10Pred], axis=0)
predData['dataTime'] = infer_time.strftime("%Y-%m-%d %H:%M:00")

con = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
predData.to_sql('dashboard_preddata', con=con, if_exists='append', index=False)
con.close()