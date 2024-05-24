from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from app.emailbackend import EmailBackEnd
from django.contrib.auth import authenticate, login, logout


def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(username, email, password)
        # check email
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists")
            return redirect('register')
        
        # check username
        if User.objects.filter(username=username).exists():
            messages.warning(request, "username are already exists")
            return redirect('register')
        
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return redirect('login')
        

    return render(request, 'registration/register.html')

def do_login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        # print(email, password)
        user = EmailBackEnd.authenticate(request,username=email, password=password)
        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'email and password are invalid')
            return redirect('login')
    

def profile(request):
    return render(request, 'registration/profile.html')


def profile_update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile')
