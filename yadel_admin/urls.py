from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

from yadel_admin import views


# Create your urls here.
urlpatterns  =  [
             
	url(r'^$',                            views.indexView,               name='admin_dashboard'),
	url(r'^dashboard/$',            views.adminDashboardView,      name='admin-dashboard'),
	
]


