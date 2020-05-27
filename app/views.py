from __future__ import unicode_literals

from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from scipy.io import wavfile

from .models import Operations,Participants
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
			o = Participants.objects.get(mainorg=email)
			o.participant = json.dumps([])
			o.save()
		except:
			Operations.objects.create(mainorg=email, participant=json.dumps([]))

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


# from imutils.video import VideoStream
# outputFrame = None
# lock = threading.Lock()
# vs = VideoStream(src="https://macabre-industries.000webhostapp.com/song.mp4").start()
# time.sleep(2.0)

# def index():
# 	return render_template("index.html")

# def detect_motion(frameCount):
# 	global vs, outputFrame, lock

# 	# loop over frames from the video stream
# 	while True:
# 		# read the next frame from the video stream, resize it,
# 		# convert the frame to grayscale, and blur it
# 		frame = vs.read()
# 		frame = imutils.resize(frame, width=400)

# 		# acquire the lock, set the output frame, and release the
# 		# lock
# 		with lock:
# 			outputFrame = frame.copy()
		
# def generate():
# 	# grab global references to the output frame and lock variables
# 	global outputFrame, lock

# 	# loop over frames from the output stream
# 	while True:
# 		# wait until the lock is acquired
# 		with lock:
# 			# check if the output frame is available, otherwise skip
# 			# the iteration of the loop
# 			if outputFrame is None:
# 				continue

# 			# encode the frame in JPEG format
# 			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

# 			# ensure the frame was successfully encoded
# 			if not flag:
# 				continue

# 		# yield the output frame in the byte format
# 		return (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
# 			bytearray(encodedImage) + b'\r\n')

# def video_feed():
# 	return Response(generate(),
# 		mimetype = "multipart/x-mixed-replace; boundary=frame")
