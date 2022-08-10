from contextlib import redirect_stderr
from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout
from gfg import settings
from django.core.mail import send_mail
# Create your views here. 
def home(request):
    return render(request, 'authentication/index.html')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, 'username already exists! please try some other username.')
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request, 'email already registered')
            return redirect('home')
        if len(username)>10:
            messages.error(request, 'username must be under 10 characters')
        if pass1 != pass2:
            messages.error(request, 'passwords didnt match!')
        if not username.isalnum():
            messages.error(request, 'username must be Alpha-numeric!')
            return redirect('home')



        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname


        myuser.save()

        messages.success(request, 'your account has been succesfully created.we have sent you a confirmation email, please confirm your email in order to activate your account')

           #welcome email

        subject = 'welcome to gfg - django login!'
        message = 'hello' + myuser.first_name + '!! \n' + 'welcome to the gfg!! \n thank you for the visit \n we have also sent you a confirmation email so please confirm your email address in order to activate your account. \n\n thanking you \n Rishabh Gaur'
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        return redirect('signin')






    return render(request, 'authentication/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request,'authentication/index.html',{'fname':fname})
        else:
            messages.error(request, 'bad credentials')
            return redirect ('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


    
