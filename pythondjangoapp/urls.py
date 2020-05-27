from django.contrib import admin

from django.urls import path
from django.conf.urls import include
from app.views import *

from django.contrib import admin

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('app.urls')),
]