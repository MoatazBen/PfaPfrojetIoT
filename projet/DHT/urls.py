from django.urls import path
from . import views, api

urlpatterns = [
    path('', views.index, name='index'),
    path("api",api.Dlist,name='json'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('index/',views.table,name='table'),
    path('myChart/',views.graphique,name='myChart'),
]
