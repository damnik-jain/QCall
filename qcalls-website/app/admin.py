from django.contrib import admin
from .models import *


m = [Transcript,Operations,Participants,Meeting]

# Register your models here.
admin.site.register(m)
