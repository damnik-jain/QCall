from django.urls import path

from . import views

urlpatterns = [
               path('', views.index, name='index'),
               path('record', views.record, name='record'),
               path('conference', views.conference, name='conference'),
               path('livestream', views.livestream, name='livestream'),
               path('meet', views.meet, name='meet'),
               path('audio', views.handleAudio, name='audio'),
               path('processVideo', views.processVideo, name='processVideo'),
               path('health', views.health, name='health'),
               path('404', views.handler404, name='404'),
               path('500', views.handler500, name='500'),
               ]
