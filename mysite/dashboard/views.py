from django.shortcuts import render
from .models import AirKoreaStations, AirKoreaData
import datetime as dt
from django.db.models import Count
from django.db.models.functions import Substr
import numpy as np
import pandas as pd
import requests
import json

def index(request):
    yesterday = dt.datetime.now().replace(microsecond=0,second=0,minute=0, hour=0)
    num_of_stations = AirKoreaData.objects.filter(datatime__range=(yesterday - dt.timedelta(days=1), yesterday)).\
            values('stnfk').distinct()
    num_of_failure = AirKoreaStations.objects.exclude(id__in=num_of_stations).values('stationname').count()
    num_of_polluted = AirKoreaData.objects.filter(datatime__range=(yesterday - dt.timedelta(days=1), yesterday)). \
        filter(khaigrade__gt=2).values('stnfk').distinct().count()
    num_of_clean = AirKoreaData.objects.filter(datatime__range=(yesterday - dt.timedelta(days=1), yesterday)). \
        filter(khaigrade__lt=2). values('stnfk').distinct().count()

    context = {
        "num_of_stations": num_of_stations.count(),
        "num_of_failure": num_of_failure,
        "num_of_polluted": num_of_polluted,
        "num_of_clean": num_of_clean,
        "stations": AirKoreaStations.objects.exclude(dmx__isnull=True).exclude(dmy__isnull=True)
    }

    return render(request, "dashboard/index.html", context)



def detail(request, station_name):
    yesterday = dt.datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)
    recent_data = AirKoreaData.objects.filter(stnfk__stationname=station_name).\
        filter(datatime__range=(yesterday - dt.timedelta(days=1), yesterday)).order_by('datatime')
    try :
        x = list(recent_data.values_list('pm25value', flat=True))
        x = pd.Series(x[-24:])
        x = x.interpolate()
        x = np.array(x)
        x = x.reshape(-1, 24, 1)

        payload = {"instances": x.tolist()}
        r = requests.post('http://localhost:8501/v1/models/lstm:predict', json=payload)
        y_pred = json.loads(r.content.decode('utf-8'))
        y_pred = y_pred['predictions'][0]
        y_pred = [i * 200 for i in y_pred]

        forecast_dt = []
        for i in range(1, 7):
            forecast_dt.append(yesterday + dt.timedelta(hours=i))
    except :
        recent_data = None
        y_pred = None
        forecast_dt = None

    return render(request, "dashboard/detail.html", {'recent_data': recent_data, 'forecast': y_pred,
                                                     'forecast_dt' : forecast_dt})


def list_table(request, status):
    yesterday = dt.datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)
    if status == 'polluted':
        stations_list = AirKoreaData.objects.filter(datatime__range=(yesterday - dt.timedelta(days=1), yesterday)). \
            filter(khaigrade__gt=2).values('stnfk').distinct()
    elif status == 'clean':
        stations_list = AirKoreaData.objects.filter(datatime__range=(yesterday - dt.timedelta(days=1), yesterday)). \
            filter(khaigrade__lt=2).values('stnfk').distinct()
    elif status == 'failure':
        stations_list = AirKoreaData.objects.filter(datatime__range=(yesterday - dt.timedelta(days=1), yesterday)).\
            values('stnfk').distinct()
        stations_list = AirKoreaStations.objects.exclude(id__in=stations_list).values('id')
    else :
        stations_list = AirKoreaStations.objects.values('id')

    stations = AirKoreaStations.objects.filter(id__in=stations_list)

    return render(request, "dashboard/list.html", {"status": status, "Stations": stations})

def stations_stat(request):
    mangname_count = AirKoreaStations.objects.values('mangname').annotate(total=Count('mangname')).order_by('-total')
    area_count = AirKoreaStations.objects.values('addr').annotate(area=Substr('addr', 1, 2)).values('area').annotate(total=Count('area')).order_by('-total')

    return render(request, "dashboard/stat.html", {"mangname_count": mangname_count, "area_count" :area_count})

def overall_map(request):
    yesterday = dt.datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)
    recent_data = AirKoreaData.objects.filter(datatime__range=(yesterday - dt.timedelta(hours=1), yesterday)).exclude(pm25value__isnull=True).order_by('datatime')
    forecast_data = AirKoreaData.objects.filter(datatime__range=(yesterday+dt.timedelta(hours=5), yesterday + dt.timedelta(hours=6))).exclude(pm25value__isnull=True).order_by('datatime')

    return render(request, "dashboard/map.html", {'recent_data' : recent_data, 'forecast_data':forecast_data})

