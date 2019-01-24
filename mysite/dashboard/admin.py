from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin

from .models import AirKoreaData, AirKoreaStations, PredData

admin.site.register(AirKoreaData)
admin.site.register(AirKoreaStations, LeafletGeoAdmin)
admin.site.register(PredData)
