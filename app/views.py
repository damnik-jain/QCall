from __future__ import unicode_literals

from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from scipy.io import wavfile
import noisereduce as nr
import soundfile as sf
from noisereduce.generate_noise import band_limited_noise
import matplotlib.pyplot as plt
import urllib.request
import numpy as np
from scipy.io.wavfile import write
import io
from django.http import HttpResponse

import moviepy

import hashlib 

#REQUIREMENTS.txt
#moviepy
#noisereduce
#soundfile

def index(request):
    return render(request, 'website/index.html')


def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)

def record(request):
	dec = request.GET.get('dec', 0)
	return render(request, 'record.html', {"dec":dec})

def conference(request):
	return render(request, 'website/conference.html')

def livestream(request):
	return render(request, 'website/livestream.html')

def meet(request):
	return render(request, 'website/recordedvideo.html')

def processVideo(request):
	pass	


@csrf_exempt
def handleAudio(request):
	if request.method=="GET":
		return render(request, 'website/audioupload.html')
	else:
		url = request.POST.get("url", "")
		print(url)
  		  
		result = hashlib.md5(url.encode())   
		print("The hexadecimal equivalent of hash is : ", end ="") 
		print(result.hexdigest()) 
		filename = result.hexdigest()

		response = urllib.request.urlopen(url)
		audio_data, audio_rate = sf.read(io.BytesIO(response.read()))

		url = "https://raw.githubusercontent.com/timsainb/noisereduce/master/assets/cafe_short.wav"
		response = urllib.request.urlopen(url)
		noise_data, noise_rate = sf.read(io.BytesIO(response.read()))

		noise_reduced = nr.reduce_noise(audio_clip=audio_data, noise_clip=noise_data)

		write("app/static/output/"+filename+".wav", 44100, noise_reduced)
		print("done writing")
		return HttpResponse("static/output/"+filename+".wav")




def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)



