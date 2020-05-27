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
			path('send', views.SenderView.as_view()),
			path('receive', views.ReceiverView),
			path('rec', views.ReceiverViewDuplicate),
			path('syncOperations', views.syncOperations, name="syncOperations"),
               path('getOperations', views.getOperations, name="getOperations"),
               path('organiser', views.organiser, name="organiser"),
               path('viewer', views.viewer, name="viewer"),
               path('getParticipants', views.getParticipants, name="getParticipants"),
               path('video_feed', views.video_feed, name="video_feed"),


     ]
