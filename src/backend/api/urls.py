from django.urls import path
from . import views

app_name = "api"
urlpatterns = [
    path("getRisk/", views.getRisk, name="getRisk"),
    path("getShapPlot/", views.getShapPlot, name="getShapPlot"),
]
