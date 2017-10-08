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
from . import slack, interval
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
			new_group = StudyGroup(picture = data, name = 'temp') # need to modify
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
			
			return JsonResponse({'status':200, 'responseText':'success', 'group_id' : new_group.id})
		if request.POST.get('description'):
			name = request.POST.get('name')
			description = request.POST.get('description')
			group_id = request.POST.get('group_id')
			group = StudyGroup.objects.filter(id = group_id)[0]
			group.name = name
			group.info = description
			group.save()

			#Create slack group
			#if request.POST.get('slack'):
			slack_ids = group.student_set.all().values_list('slack_id', flat = True)
			link = slack.createnewgp(name, slack_ids)
			return JsonResponse({'status':200, 'link':link})
	return render(request, 'creategroup.html')

@csrf_exempt
def attendance(request):
	if request.method == 'GET':
		students = Student.objects.all()
		groups = StudyGroup.objects.all()
		return render(request, 'attendance.html',context = {'students': students, 'groups': groups})
	#if request.method == 'POST':

@csrf_exempt
def slack(request):
	if request.method == 'GET':
		return render(request, 'slack.html', context = {'link': request.GET.get('link')})
@csrf_exempt
def monitor(request):
	if request.method == 'GET':
		return render(request, 'monitor.html')
	if request.method == 'POST':
		if request.POST.get('action') == 'start':
			interval.run()
		if request.POST.get('action') == 'pic':
			picture = request.POST.get('pic') #base64
			form, imgstr = picture.split(';base64,') 
			ext = form.split('/')[-1]
			data = ContentFile(base64.b64decode(imgstr), name = 'temp' + '.'+ext)

			with open('/Users/ryancheng/Desktop/calhacks/coin/media/monitor/status.png', 'wb') as fh:
				fh.write(base64.b64decode(imgstr))
			return JsonResponse({'status': 200})
		#if request.POST.get('action') == 'end':

def img(request):
	if request.method == 'GET':
		return render(request, 'img.html')

def createattend(request):
	if request.method == 'GET':
		return render(request, 'createattend.html')




