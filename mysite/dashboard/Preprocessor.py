import sqlite3
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
import numpy as np
from GIS_processor import GIS_processor

prepro = GIS_processor()
input_shape = 150
gridy_e = 250
gridy_s = 100
    
class Preprocessor:
    
    def extract_data(self, sttime):
        con = sqlite3.connect("/Users/jyj0729/PycharmProjects/air-pollution/mysite/db.sqlite3")
        time_string = sttime.strftime("%Y-%m-%d %H:%M:00")
        sql = 'select * from dashboard_airkoreadata a join dashboard_airkoreastations b on a.stnfk_id=b.id where datatime="'
        sql = sql + time_string + '";'
        df = pd.read_sql(sql, con)
        con.close()
        return df
    
    def make_sample(self, sttime):
        
        con = sqlite3.connect("/Users/jyj0729/PycharmProjects/air-pollution/mysite/db.sqlite3")

        for i in range(1,4):
            ctime = sttime - timedelta(hours=i)
            
            time_string = ctime.strftime("%Y-%m-%d %H:%M:00")
            sql = 'select * from dashboard_airkoreadata a join dashboard_airkoreastations b on a.stnfk_id=b.id where datatime="'
            sql = sql + time_string + '";'
            df = pd.read_sql(sql, con)
            
            gridx, gridy = [], []
            for idx, data in df.iterrows():
                x, y = prepro.mapToGrid(data.dmX, data.dmY)
                gridx.append(x), gridy.append(y)
            df = df.assign(gridx = gridx, gridy = gridy)

            grid_array = np.zeros((253+1, 149+1, 2))
            for idx, data in df.iterrows():
                try :
                    grid_array[253+1-data.gridy, data.gridx, 0] = int(data.pm25Value)
                    grid_array[253+1-data.gridy, data.gridx, 1] = int(data.pm10Value)
                except :
                    pass
            grid_array = grid_array[gridy_s:gridy_e,:, :]

            if i==1:
                df_c = grid_array.reshape(input_shape, input_shape, 2)
            else :
                df_c = np.concatenate((df_c, grid_array.reshape(input_shape, input_shape, 2)), axis=2)

                
        for i in range(1,4):
            ptime = sttime - timedelta(days=i)
            
            time_string = ptime.strftime("%Y-%m-%d %H:%M:00")
            sql = 'select * from dashboard_airkoreadata a join dashboard_airkoreastations b on a.stnfk_id=b.id where datatime="'
            sql = sql + time_string + '";'
            df = pd.read_sql(sql, con)

            gridx, gridy = [], []
            for idx, data in df.iterrows():
                x, y = prepro.mapToGrid(data.dmX, data.dmY)
                gridx.append(x), gridy.append(y)
            df = df.assign(gridx = gridx, gridy = gridy)

            grid_array = np.zeros((253+1, 149+1, 2))
            for idx, data in df.iterrows():
                try :
                    grid_array[253+1-data.gridy, data.gridx, 0] = int(data.pm25Value)
                    grid_array[253+1-data.gridy, data.gridx, 1] = int(data.pm10Value)
                except :
                    pass
            grid_array = grid_array[gridy_s:gridy_e,:, :]

            if i==1:
                df_p = grid_array.reshape(input_shape, input_shape, 2)
            else :
                df_p = np.concatenate((df_p, grid_array.reshape(input_shape, input_shape, 2)), axis=2)

        for i in [10, 20, 30]:
            ttime = sttime - timedelta(days=i)
            
            time_string = ttime.strftime("%Y-%m-%d %H:%M:00")
            sql = 'select * from dashboard_airkoreadata a join dashboard_airkoreastations b on a.stnfk_id=b.id where datatime="'
            sql = sql + time_string + '";'
            df = pd.read_sql(sql, con)
            
            gridx, gridy = [], []
            for idx, data in df.iterrows():
                x, y = prepro.mapToGrid(data.dmX, data.dmY)
                gridx.append(x), gridy.append(y)
            df = df.assign(gridx = gridx, gridy = gridy)

            grid_array = np.zeros((253+1, 149+1, 2))
            for idx, data in df.iterrows():
                try :
                    grid_array[253+1-data.gridy, data.gridx, 0] = int(data.pm25Value)
                    grid_array[253+1-data.gridy, data.gridx, 1] = int(data.pm10Value)
                except :
                    pass
            grid_array = grid_array[gridy_s:gridy_e,:, :]

            if i==10:
                df_t = grid_array.reshape(input_shape, input_shape, 2)
            else :
                df_t = np.concatenate((df_t, grid_array.reshape(input_shape, input_shape, 2)), axis=2)


        df_x = np.concatenate((df_c.reshape(1, input_shape, input_shape, 6), 
                                df_p.reshape(1, input_shape, input_shape, 6), 
                                df_t.reshape(1, input_shape, input_shape, 6)), axis=0)
        df_x = df_x.reshape(1, 3, input_shape, input_shape, 6)
        con.close()
        return df_x
    