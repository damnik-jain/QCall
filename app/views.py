from __future__ import unicode_literals

from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from scipy.io import wavfile

from .models import Operations,Participants,Transcript
import json
# import noisereduce as nr
# import soundfile as sf
# from noisereduce.generate_noise import band_limited_noise
import matplotlib.pyplot as plt
import urllib.request
from scipy.io.wavfile import write
import io
from django.http import HttpResponse
from django.views.generic import TemplateView

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
	email = request.GET.get('email')
	return render(request, 'website/livestream.html', {"id":email})

def meet(request):
	return render(request, 'website/recordedvideo.html')

def processVideo(request):
	pass	


@csrf_exempt
def handleAudio(request):
	if request.method=="GET":
		return render(request, 'website/audioupload.html')
	else:
		# url = request.POST.get("url", "")
		# print(url)
  		  
		# result = hashlib.md5(url.encode())   
		# print("The hexadecimal equivalent of hash is : ", end ="") 
		# print(result.hexdigest()) 
		# filename = result.hexdigest()

		# response = urllib.request.urlopen(url)
		# audio_data, audio_rate = sf.read(io.BytesIO(response.read()))

		# url = "https://raw.githubusercontent.com/timsainb/noisereduce/master/assets/cafe_short.wav"
		# response = urllib.request.urlopen(url)
		# noise_data, noise_rate = sf.read(io.BytesIO(response.read()))

		# noise_reduced = nr.reduce_noise(audio_clip=audio_data, noise_clip=noise_data)

		# write("app/static/output/"+filename+".wav", 44100, noise_reduced)
		# print("done writing")
		# return HttpResponse("static/output/"+filename+".wav")
		return HttpResponse("disable")



def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

@csrf_exempt
def syncOperations(request):
	if request.method=="POST":
		opr = request.POST.get('operations', {})
		email = request.POST.get('email', '')
		if email!='':
			o = None
			try:
				o = Operations.objects.get(email=email)
				o.operations = opr
				o.save()
			except:
				Operations.objects.create(email=email, operations=opr)
		return HttpResponse('Done')

@csrf_exempt
def getOperations(request):
	email = request.GET.get('email', '')
	res = []
	if email!='':
		try:
			o = Operations.objects.get(email=email)
			res = o.operations
		except:
			res = []
	return JsonResponse(res, safe=False)



class SenderView(TemplateView):
    template_name = "sender.html"

def ReceiverView(request):
	email = request.GET.get('email')
	broadcast = request.GET.get('broadcast')
	template_name = "website/receiver-test.html"
	return render(request, template_name, {"id":email, "broadcast":broadcast})
	
def ReceiverViewDuplicate(request):
	email = request.GET.get('email')
	broadcast = request.GET.get('broadcast')
	template_name = "website/receiver-clone.html"
	return render(request, template_name, {"id":email, "broadcast":broadcast})


def organiser(request):
	email = request.GET.get('email')
	request.session['organiser'] = email
	removeParticipants(email)
	return render(request, 'website/organiser.html', {"id":email})

def viewer(request):
	email = request.GET.get('email')
	broadcast = request.GET.get('broadcast')
	addParticipants(str(broadcast), str(email))
	template_name = "website/viewer.html"
	return render(request, template_name, {"id":email, "broadcast":broadcast})


def addParticipants(email, participant):
	if email!='':
		o = None
		try:
			o = Participants.objects.get(mainorg=email)
			pat = json.loads(o.participant)
			pat.append(participant)
			o.participant = json.dumps(pat)
			o.save()
		except:
			Operations.objects.create(mainorg=email, participant=json.dumps([participant]))
	
def removeParticipants(email):
	if email!='':
		o = None
		try:
			o = Participants.objects.get(mainorg=str(email))
			o.participant = json.dumps([])
			o.save()
		except:
			Participants.objects.create(mainorg=str(email), participant=json.dumps([]))

@csrf_exempt
def getParticipants(request):
	email = request.GET.get('email', '')
	res = []
	if email!='':
		try:
			o = Participants.objects.get(mainorg=email)
			res = o.participant
		except:
			res = []
	print(res)
	return JsonResponse(res, safe=False)

import time

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#pip install websocket-client
#pip install ibm_watson
# pip install ibm_cloud_sdk_core

@csrf_exempt
def voice_request(request):
	millis = int(round(time.time() * 1000))
	
	# print(request.body)
	# print(request.POST["audio_data"])
	try:
		print("Email ",request.session['email'])
	except:
		print("Email ","notfound")
	filename = "audio"
	try:
		filename = request.session['email']
	except:
		pass

	filename += str(millis)
	fileurl = '/static/output/'+filename+'.wav'
	filepath = './app'+fileurl
	f = open(filepath, 'wb')
	f.write(request.body)
	f.close()


	api = IAMAuthenticator("rLiffBz3rQNWKyIJKmhmGGb8jMaI4G4DY63gEuc2vDXt")

	stot=SpeechToTextV1(authenticator=api)

	stot.set_service_url("https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/c1d0ac86-901c-42c5-ab92-03cbaff5f3f3")

	with open(filepath,"rb") as audio_file:
		result = stot.recognize(audio=audio_file,content_type="audio/wav").get_result()

	print(result)
	transcript = ""
	for i in result['results']:
		transcript += " "+str(i['alternatives'][0]['transcript'])
		print(i['alternatives'][0]['transcript'])

	Transcript.objects.create(email=request.user['email'],
		transcript=transcript,audio_file=fileurl)
	return HttpResponse(transcript)

#To create meetings resources client receiver
