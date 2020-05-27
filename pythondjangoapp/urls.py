from django.contrib import admin

from django.urls import path
from django.conf.urls import include
from app.views import *
urlpatterns = [
                path('', include('app.urls'))
               ]