from django.contrib import admin
from .models import *

# Register your models here.




class What_You_Learn_TabularInline(admin.TabularInline):
    model = What_You_Learn

class Requirements_TabularInline(admin.TabularInline):

    model = Requirements

class VideoTabularline(admin.TabularInline):

      model = Video


class Course_Admin(admin.ModelAdmin):
    
    inlines = [What_You_Learn_TabularInline, Requirements_TabularInline, VideoTabularline]




admin.site.register([Categories, Author, Level, What_You_Learn, Requirements,Lession, Video, Language, UserCourse, Payment])
admin.site.register(Course, Course_Admin)