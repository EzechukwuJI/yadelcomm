from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


# Create your views here.



def  indexView(request):
    return render(request, 'yadel/index.html', {})


def  aboutUsView(request):
    return render(request, 'yadel/index.html', {})


def  servicesView(request, service_type):
    return render(request, 'yadel/services.html', {})



def  newsroomView(request):
    return render(request, 'yadel/newsroom.html', {})



def  contactView(request):
    return render(request, 'yadel/contact.html', {})


def  signUpView(request):
    return render(request, 'yadel/signup.html', {})


def  loginView(request):
    return render(request, 'yadel/signin.html', {})



def  logoutView(request):
    return render(request, 'yadel/index.html', {})

@login_required()
def dashboardView(request):
	return render(request, 'yadel/index.html', {})


@login_required()
def createArticleView(request):
	return render(request, 'yadel/index.html', {})



















