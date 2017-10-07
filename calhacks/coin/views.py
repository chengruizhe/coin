from django.shortcuts import render
from .models import StudyGroup, Student
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .forms import ImageUploadForm
import base64
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from . import FaceAPI

@csrf_exempt
def index(request):
	if request.method == 'GET':
		if request.GET.get('log in'):
			return
	if request.POST.post == ('log out'):
		return
	else:
		return HttpResponseBadRequest

@csrf_exempt
def creategroup(request):
	if request.method == 'GET':
		return render(request, 'creategroup.html')
	if request.method == 'POST':
		picture = request.POST.get('pic') #base64
		name = request.POST.get('name')
		form, imgstr = picture.split(';base64,') 
		ext = form.split('/')[-1]
		data = ContentFile(base64.b64decode(imgstr), name = name + '.'+ext) 

		binaryImage = base64.decodebytes(imgstr)
		print(binaryImage)
		
		print(binaryImage)
		service = FaceAPI.FaceAPI()

		detectedFaces = service.detectFace(binaryImage)
		print(service.identifyFace(detectedFaces, 1))

		new_group = StudyGroup(name = name, picture = data)
		new_group.save()
		return JsonResponse({'status': 200, 'responseText': binaryImage})
	return 


#def 

