from django.contrib import admin

from .models import StudyGroup
from .models import Student

admin.site.register(Student)
admin.site.register(StudyGroup)
# Register your models here.
