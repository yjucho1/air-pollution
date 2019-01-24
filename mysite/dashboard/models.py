from django.db import models
from djgeojson.fields import PointField

class AirKoreaStations(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    addr = models.TextField(blank=True, null=True)
    dmx = models.DecimalField(db_column='dmX', blank=True, null=True, decimal_places=10, max_digits=15)  # Field name made lowercase.
    dmy = models.DecimalField(db_column='dmY', blank=True, null=True, decimal_places=10, max_digits=15)  # Field name made lowercase.
    item = models.TextField(blank=True, null=True)
    mangname = models.TextField(db_column='mangName', blank=True, null=True)  # Field name made lowercase.
    map = models.TextField(blank=True, null=True)
    oper = models.TextField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    stationname = models.TextField(db_column='stationName', blank=True, null=True)  # Field name made lowercase.
    year = models.TextField(blank=True, null=True)
    geom = PointField(default=[37.4026616, 127.1010097])


class AirKoreaData(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    cograde = models.IntegerField(db_column='coGrade', blank=True, null=True)  # Field name made lowercase.
    covalue = models.FloatField(db_column='coValue', blank=True, null=True)  # Field name made lowercase.
    datatime = models.DateTimeField(db_column='dataTime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    khaigrade = models.IntegerField(db_column='khaiGrade', blank=True, null=True)  # Field name made lowercase.
    khaivalue = models.IntegerField(db_column='khaiValue', blank=True, null=True)  # Field name made lowercase.
    mangname = models.TextField(db_column='mangName', blank=True, null=True)  # Field name made lowercase.
    no2grade = models.IntegerField(db_column='no2Grade', blank=True, null=True)  # Field name made lowercase.
    no2value = models.FloatField(db_column='no2Value', blank=True, null=True)  # Field name made lowercase.
    o3grade = models.IntegerField(db_column='o3Grade', blank=True, null=True)  # Field name made lowercase.
    o3value = models.FloatField(db_column='o3Value', blank=True, null=True)  # Field name made lowercase.
    pm10grade = models.IntegerField(db_column='pm10Grade', blank=True, null=True)  # Field name made lowercase.
    pm10grade1h = models.IntegerField(db_column='pm10Grade1h', blank=True, null=True)  # Field name made lowercase.
    pm10value = models.IntegerField(db_column='pm10Value', blank=True, null=True)  # Field name made lowercase.
    pm10value24 = models.IntegerField(db_column='pm10Value24', blank=True, null=True)  # Field name made lowercase.
    pm25grade = models.IntegerField(db_column='pm25Grade', blank=True, null=True)  # Field name made lowercase.
    pm25grade1h = models.IntegerField(db_column='pm25Grade1h', blank=True, null=True)  # Field name made lowercase.
    pm25value = models.IntegerField(db_column='pm25Value', blank=True, null=True)  # Field name made lowercase.
    pm25value24 = models.IntegerField(db_column='pm25Value24', blank=True, null=True)  # Field name made lowercase.
    so2grade = models.IntegerField(db_column='so2Grade', blank=True, null=True)  # Field name made lowercase.
    so2value = models.FloatField(db_column='so2Value', blank=True, null=True)  # Field name made lowercase.
    stnfk = models.ForeignKey(AirKoreaStations, on_delete=models.CASCADE)


class PredData(models.Model):
    lat = models.DecimalField(db_column='lat', blank=True, null=True, decimal_places=10, max_digits=15)
    lon = models.DecimalField(db_column='lon', blank=True, null=True, decimal_places=10, max_digits=15)
    predValue = models.DecimalField(db_column='predValue', blank=True, null=True, decimal_places=10, max_digits=15)
    type = models.TextField(db_column='type', blank=True, null=True)
    dataTime = models.DateTimeField(db_column='dataTime', blank=True, null=True)