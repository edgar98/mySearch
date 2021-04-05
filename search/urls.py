from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('result/<slug:string>/', views.results, name='results')
]