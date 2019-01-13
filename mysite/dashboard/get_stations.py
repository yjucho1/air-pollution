import xml.etree.ElementTree as ET
import pandas as pd
import requests
import sqlite3
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


if __name__ == "__main__":

    ## 1. 측정소 정보 가져오기
    cols = ['stationName', 'addr', 'year', 'oper', 'photo', 'map', 'mangName', 'item', 'dmX', 'dmY']
    OPEN_API_KEY = get_env_variable("OPEN_API_KEY")
    user_agent_url = 'http://openapi.airkorea.or.kr/openapi/services/rest/MsrstnInfoInqireSvc/' + \
                     'getMsrstnList?serviceKey=' + OPEN_API_KEY + '&numOfRows=999&pageSize=100&pageNo=1&startPage=1'
    xml_data = requests.get(user_agent_url).content
    root = ET.XML(xml_data)
    df = []
    for body in root.findall('body'):
        for items in body.findall('items'):
            for item in items.findall('item'):
                parsed = dict()
                for col in cols:
                    parsed[col] = item.find(col).text
                df.append(parsed)

    df = pd.DataFrame(df)
    df.index.name = 'ID'
    df = df.loc[(~df.dmX.isnull()) & (~df.dmY.isnull())]
    df['geom'] = [str({'type': 'Point', 'coordinates': [float(y), float(x)]}) for y, x in zip(df.dmX, df.dmY)]
    df.index += 1
    df = df.reset_index()
    con = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    df.to_sql('dashboard_airkoreastations', con=con, if_exists='append', index=False)
    con.close()
