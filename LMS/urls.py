"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .import views, user_login
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('base', views.BASE, name = 'base'),
    path('404', views.page_not_found, name= '404'),
    path('', views.HOME, name= "home"),
    path('courses', views.single_course, name= 'single_course'),
    path('product/filter-data', views.filter_data, name= "filter_data"),
    path('course/<slug:slug>', views.course_details, name="course_details"),
    path('search', views.search_course, name="search_course"),
    path('contact-us', views.contact_us, name="contact_us"),
    path('about-us', views.about_us, name='about_us'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register',user_login.register , name='register'),
    path('do-login', user_login.do_login, name="do_login"),
    path('profile', user_login.profile, name='profile'),
    path('profile-update',user_login.profile_update ,name='profile_update'),
    path('checkout/<slug:slug>', views.checkout, name='checkout'),
    path('my-course', views.my_course, name = "my_course"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

