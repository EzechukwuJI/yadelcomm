from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.



def  indexView(request):
    return HttpResponse('This admin page worked')



@login_required()
def adminDashboardView(request):
    return render(request, 'yadel/admin-dashboard.html', {})
