from django.urls import path, include
import dashboard.views as views
from django.conf.urls import url

urlpatterns = [
    path('status/<str:status>/', views.list_table, name='list_table'),
    path('detail/<str:station_name>/', views.detail, name='detail'),
    path('stat/', views.stations_stat, name='stat'),
    path('map/', views.overall_map, name='map'),
    path('', views.index, name='index'),
]