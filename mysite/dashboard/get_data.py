import xml.etree.ElementTree as ET
import pandas as pd
import requests
import sqlite3
import datetime as dt
import os
import json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_env_variable(setting):
    secret_file = os.path.join(BASE_DIR, 'secret.json')

    with open(secret_file, 'r') as f:
        secret = json.loads(f.read())

    try:
        return secret[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


def my_to_datetime(date_str):
    if date_str[11:13] != '24':
        return pd.to_datetime(date_str, format='%Y-%m-%d %H:%M')
    date_str = date_str[0:11] + '00'
    return pd.to_datetime(date_str, format='%Y-%m-%d %H:%M') + dt.timedelta(days=1)


if __name__ == "__main__":

    cols = ['dataTime', 'mangName', 'so2Value',
            'coValue', 'o3Value', 'no2Value', 'pm10Value',
            'pm10Value24', 'pm25Value', 'pm25Value24', 'khaiValue',
            'khaiGrade', 'so2Grade', 'coGrade', 'o3Grade',
            'no2Grade', 'pm10Grade', 'pm25Grade', 'pm10Grade1h',
            'pm25Grade1h']
    numeric_cols =['so2Value',
            'coValue', 'o3Value', 'no2Value', 'pm10Value',
            'pm10Value24', 'pm25Value', 'pm25Value24', 'khaiValue',
            'khaiGrade', 'so2Grade', 'coGrade', 'o3Grade',
            'no2Grade', 'pm10Grade', 'pm25Grade', 'pm10Grade1h',
            'pm25Grade1h']
    OPEN_API_KEY = get_env_variable("OPEN_API_KEY")

    con = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    df = pd.read_sql("select * from dashboard_airkoreastations;", con)
    df = df[['stationName', 'ID']]
    df = df.set_index('stationName')
    df = df.to_dict()
    stnName_dict = df['ID']

    for idx, stnName in enumerate(stnName_dict.keys()):
        user_agent_url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/' + \
                         'getMsrstnAcctoRltmMesureDnsty?serviceKey=' + OPEN_API_KEY + \
                         '&numOfRows=9999&pageSize=9999&pageNo=1' + \
                         '&startPage=1&stationName=' + stnName + '&dataTerm=DAILY&ver=1.3'
        xml_data = requests.get(user_agent_url).content
        try:
            root = ET.XML(xml_data)
        except:
            pass
        df = []
        for item in root.findall('body/items/item'):
            parsed = dict()
            for col in cols:
                parsed[col] = item.find(col).text
            df.append(parsed)
        df = pd.DataFrame(df)
        df['stnfk_id'] = stnName_dict[stnName]
        try:
            df.dataTime = df.dataTime.apply(my_to_datetime)
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
            df = df.loc[df.dataTime >= (dt.datetime.now().replace(microsecond=0, second=0, minute=0)
                                       - dt.timedelta(hours=1))]
            df.to_sql('dashboard_airkoreadata', con=con, if_exists='append', index=False)
        except:
            pass

        if idx % 10 == 0:
            print("{0} stations's data is loaded.".format(str(idx)))

    con.close()
