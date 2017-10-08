from django.db import models

class StudyGroup(models.Model):
	name = models.CharField(max_length = 30)
	picture = models.ImageField(upload_to = 'studygroups')
	info = models.CharField(max_length = 30, null = True)

	def __str__(self):
		return self.name

class Student(models.Model):
	person_id = models.CharField(max_length = 60, primary_key = True)
	slack_id = models.CharField(max_length = 60, null=True)
	picture = models.ImageField(upload_to = 'students' , null = True)
	name = models.CharField(max_length = 30)
	email = models.CharField(max_length = 30)
	username = models.CharField(max_length = 20)
	pwd = models.CharField(max_length = 30)
	study_groups = models.ManyToManyField(StudyGroup)

	def __str__(self):
		return self.name