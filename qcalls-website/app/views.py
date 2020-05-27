from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from scipy.io import wavfile
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Operations,Participants,Transcript,Meeting
import json
from gensim.summarization.summarizer import summarize
# import noisereduce as nr
# import soundfile as sf
# from noisereduce.generate_noise import band_limited_noise
import matplotlib.pyplot as plt
import urllib.request
from scipy.io.wavfile import write
import io
from django.http import HttpResponse
from django.views.generic import TemplateView

from django.views.generic import View
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

@login_required
def organiser(request):
	email = request.user.email
	request.session['organiser'] = email
	removeParticipants(email)
	m = Meeting.objects.create(email=email, status=1)
	request.session["mid"] = m.meeting_id
	return render(request, 'website/organiser.html', {"id":email, "mid":m.meeting_id})

def joinMeet(request):
	mid = request.GET.get('mid')
	return render(request, "website/join.html", {"meeting_id":mid})

def viewer(request):
	email = request.GET.get('email')
	request.session["email"] = email
	mid = request.GET.get('meeting_id')
	try:
		m = Meeting.objects.get(meeting_id=mid)
	except:
		return redirect('meeting404')
	broadcast = m.email
	addParticipants(str(broadcast), str(email))
	template_name = "website/viewer.html"
	return render(request, template_name, {"id":email, "broadcast":broadcast, "mid":mid})

def meeting404(request):
	return render(request, "website/meeting404.html")

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
			Participants.objects.create(mainorg=email, participant=json.dumps([participant]))
	
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
	# print(res)
	return JsonResponse(res, safe=False)

import time

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# pip install websocket-client
# pip install ibm_watson
# pip install ibm_cloud_sdk_core

@csrf_exempt
def voice_request(request):
	millis = int(round(time.time() * 1000))
	
	filename = "audio"
	try:
		filename = request.user.email
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

	transcript = ""
	for i in result['results']:
		transcript += " "+str(i['alternatives'][0]['transcript'])
		print(i['alternatives'][0]['transcript'])
	summary = summarize(transcript,ratio=0.3,split=True)
	transcript += "<br><br><h2>Summary<h2><p>"+str(summary)+"</p>"
	print("Final Transcript: "+transcript)
	Transcript.objects.create(meeting_id=request.session.get("mid",""),
		transcript=transcript,audio_file=fileurl)
	return JsonResponse({'transcript':transcript})

def checkLogin(request):
	if request.user.is_authenticated:
		return True
	else:
		return False


class RegisterFormView(View):
	form_class = RegisterForm
	template_name = 'website/register.html'
	def get(self, request):
		form = self.form_class(None)
		error, err_email = '', ''
		try:
			error = request.session.get('err_mess', '')
			err_email = request.session.get('err_email', '')
			del request.session['err_email']
			del request.session['err_mess']
		except:
			pass

		return render(request, self.template_name, {'cart_size' : request.session.get('cart_size', 0),'form':form, 'err_email': err_email, 'register_error': error})

	def post(self, request):
		form = self.form_class(request.POST)
		if "already exists" in str(form.errors):
			request.session['err_email'] = request.POST.get('username', '')
			request.session['err_mess'] = "duplicate"
			return redirect('/register/')

		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			acount = 0
			for cr in username:
				if cr == "@":
					acount += 1

			if acount != 1:
				request.session['err_mess'] = "invalidemail"
				return redirect('/register/')

			prevuser = User.objects.filter(email=username)
			if prevuser.count()>0:
				request.session['err_mess'] = "duplicate"
				return redirect('/register/')

			user.set_password(password)
			user.email = username
			user.save()
			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					lr = request.session.get("lr","index")
					return redirect(lr)
				else:
					return redirect('/login?login=disabled')
			else:
				return redirect('/login?login=failed')

class LoginFormView(View):
	form_class = LoginForm
	template_name = 'website/login.html'
	def get(self, request):
		# 3 -> login to checkout
		request.session['lr'] = request.GET.get('next','index')
		error = request.GET.get('login_error', '')
		if str(request.GET.get('m')) == '3' :
			error = 'login_to_checkout'

		form = self.form_class(None)
		print("Error Value = "+error)
		return render(request, self.template_name, {'cart_size' : request.session.get('cart_size', 0),'form':form, 'login_error': error })


	def post(self, request):
		form = self.form_class(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		useremail = User.objects.filter(email=username)

		if user is not None:
			if user.is_active:
				login(request, user)
				lr = request.session.get("lr","index")
				return redirect(lr)
			else:
				return redirect('/login?login_error=disabled')
		else:
			if useremail.count()>0:
				return redirect('/login?login_error=incorrect')
			else:
				return redirect('/login?login_error=failed')

from django.contrib.auth import logout


def logoutForm(request):
	logout(request)
	# Redirect to a success page.
	return redirect('index')

@login_required
def endMeeting(request):
	if request.method.lower()=="get":
		m = Meeting.objects.get(meeting_id=request.session.get('mid'))
		m.status = 0
		m.save()
		return HttpResponse('Done')

# To create meetings resources client receiver
@csrf_exempt
def getMeetingStatus(request):
	mid = request.GET.get('mid')
	m = Meeting.objects.get(meeting_id=mid)
	status = m.status
	res = {}
	res["status"] = status
	try:
		t = Transcript.objects.get(email=m.email)
		res["transcript"] = t.transcript
		res["audio_file"] = t.audio_file
		res["present"] = 1
	except:
		res["present"] = 0
		res["transcript"] = "na"
		res["audio_file"] = "na"
	# print(res)
	return JsonResponse(res, safe=False)

@csrf_exempt
def startMeeting(request):
	m = Meeting.objects.get(meeting_id=request.session.get('mid'))
	m.status = 2
	m.save()
	# print("\n\n\n\n\n\n\n Meeting status update to 2\n\n\n\n\n\n\n\n\n")
	m = Meeting.objects.get(meeting_id=request.session.get('mid'))
	# print(str(m.status))
	return HttpResponse('Done')
