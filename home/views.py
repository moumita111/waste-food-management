from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib import messages
from django.contrib.sessions.models import Session
from .forms import *
from .models import Ngo
from .models import Donation
from django.contrib.auth.decorators import login_required


def home(request):
   return render(request,template_name='index.html')
def contact(request):
   return render(request,template_name='contact.html')
def about(request):
   return render(request,template_name='aboutus.html')
@login_required
def profile(request):
   return render(request,template_name='profile.html')
def thankyou(request):
   return render(request,template_name='thankyou.html')

def ngo(request):
   return render(request,template_name='ngo.html')   


def dlist(request):
    dlist=Donation.objects.all()
    context= {
        'dlist': dlist,
    }

    return render(request,template_name='dlist.html', context=context )

def donation(request):
    form = DonationForm()
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('thankyou')
    context ={
        'form':form,
    }
    return render(request,template_name='donation.html', context=context)
   

def user_sign(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username , email=email , password = password)

        request.session['signup_username']= username
        request.session['signup_email'] = email
        request.session['signup_password'] = password

        user = authenticate(request,username=username , password = password)

        if user is not None :
            auth_login(request,user)
            messages.success(request,'Successfulyy signed up!')
            return redirect('user_login')
    return render(request,template_name='user_sign.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None :
            auth_login(request,user)
            messages.success(request,'Successfulyy Logged In!')
            return redirect('home')
    return render(request,template_name='user_login.html')

def logout_user(request):
     logout(request)
     messages.success(request,'Youre logged out!')
     return redirect('user_sign')


def ngo_login(request):
    if  request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        if Ngo.objects.filter(name = name).exists():
            ngo= Ngo.objects.get(name= name)

            if ngo.password==password :
               request.session['ngo_name'] = ngo.name
               request.session['ngo_email'] = ngo.email
               request.session['ngo_company_name'] = ngo.company_name
               request.session['ngo_password'] = ngo.password

               return redirect("ngo")

            else :
                messages.error(request,'please fillup the form')

                return redirect('ngo_login')

        else :
            messages.error(request,'invalid username!')

    return render(request,template_name='Ngo_Login.html')

def complete(request, id):
    donation = Donation.objects.get(pk=id)
    if request.method=='POST':
        donation.delete()
        return redirect('dlist')
    
    
    return render(request,template_name='complete.html')