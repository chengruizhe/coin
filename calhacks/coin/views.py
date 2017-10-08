from django.shortcuts import render
from .models import StudyGroup, Student
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .forms import ImageUploadForm
import base64
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from . import FaceAPI
from . import DrawRectangle
from django.conf import settings
from PIL import Image

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
		if request.POST.get('pic'):
			picture = request.POST.get('pic') #base64
			form, imgstr = picture.split(';base64,') 
			ext = form.split('/')[-1]
			data = ContentFile(base64.b64decode(imgstr), name = 'temp' + '.'+ext)
			new_group = StudyGroup(picture = data) # need to modify
			new_group.save()

			binImg = base64.b64decode(imgstr)
			service = FaceAPI.FaceAPI()
			detectedFaces, detectedRectangles = service.detectFace(binImg)

			if detectedFaces:
				result = service.identifyFace(detectedFaces, 1)
				matchResult = json.loads(result.decode('utf8'))
			else:
				matchResult = []

				
			faceAndStudentId = {}
			for person in matchResult:
				print(person)
				if person["candidates"]:
					tempID = person["candidates"][0]["personId"]
				else:
					tempID = None
				faceAndStudentId[person["faceId"]] = tempID

			#faceAndStudentId : {faceID, StudentID}
			#dectedRectangles : {faceID, rectangle}
			namedRectangle = []
			print(faceAndStudentId)
			for faceId in faceAndStudentId:
				studentId = faceAndStudentId[faceId]
				print(studentId)
				if studentId:
					name = Student.objects.filter(pk = studentId).values_list("name", flat = True)[0]
				else:
					name = "Unknown Person"
				namedRectangle.append((name, detectedRectangles[faceId]))

			student_ids = [faceAndStudentId[face] for face in faceAndStudentId.keys() if faceAndStudentId[face]]
			
			#draw = DrawRectangle.DrawRectangle(new_group.imageField.url)
			draw = DrawRectangle.DrawRectangle(settings.MEDIA_ROOT+ ".."+new_group.picture.url, namedRectangle)
			#draw = DrawRectangle.DrawRectangle("/Users/ryancheng/Desktop/calhacks/calhacks/coin/plot.png", detectedRectangles)
			draw.produceImg()
			processedImage = Image.open("plot.png")

			for i in student_ids:
				student = Student.objects.filter(person_id = i)
				if student:
					student = student[0]
					student.study_groups.add(new_group)
			
			return JsonResponse({'group':new_group.pk, 'responseText':'success'})
		if request.POST.get('confirm'):
			response = request.POST.get('response')
			name = response['name']
			description = response['description']
			group_id = response['id']
			group = StudyGroup.objects.filter(pk = group_id)[0]
			group.name = name
			group.info = description
			group.save()
			return JsonResponse({'status': 200, 'responseText': 'success'})
	return 

@csrf_exempt
def attendance(request):
	if request.method == 'GET':
		students = Student.objects.all()
		groups = StudyGroup.objects.all()
		return render(request, 'attendence.html',context = {'students': students, 'groups': groups})
	#if request.method == 'POST':





