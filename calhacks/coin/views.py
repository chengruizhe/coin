from django.shortcuts import render
from .models import StudyGroup, Student
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .forms import ImageUploadForm
import base64
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from . import FaceAPI
import json

@csrf_exempt
def index(request):
	if request.method == 'GET':
		if request.GET.get('log in'):
			return
	if request.POST.get == 'log out':
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
		info = request.POST.get('info')
		form, imgstr = picture.split(';base64,') 
		ext = form.split('/')[-1]
		data = ContentFile(base64.b64decode(imgstr), name = name + '.'+ext)
		new_group = StudyGroup(name = name, picture = data) # need to modify
		new_group.save()

		student_ids = personIDsFromImg(imgstr)
		
		for i in student_ids:
			student = Student.objects.filter(person_id = i)
			if student:
				student = student[0]
				student.study_groups.add(new_group)
		return JsonResponse({'status': 200, 'responseText': 'success'})
	return 

@csrf_exempt
def attendence(request):
	if request.method == 'GET':
		students = Student.objects.all()
		groups = StudyGroup.objects.all()
		return render(request, 'attendence.html',context = {'students': students, 'groups': groups})
	#if request.method == 'POST':


def personIDsFromImg(imgstr):
	binImg = base64.b64decode(imgstr)
	service = FaceAPI.FaceAPI()
	detectedFaces = service.detectFace(binImg)
	result = service.identifyFace(detectedFaces, 1)

	student_ids = []

	matchResult = json.loads(result.decode('utf8'))
	for person in matchResult:
		if person["candidates"]:
			student_ids.append(person["candidates"][0]["personId"])
	return student_ids





