from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

from yadel_main import views


# Create your urls here.
urlpatterns  =  [
             
	url(r'^$',                         					views.indexView,          name='index'),
	url(r'^about_us/$',                					views.aboutUsView,        name='about_us'),
	url(r'^services/(?P<service_type>[-\w]+)/$',         views.servicesView,       name='services'),
	url(r'^newsroom/$',                					views.newsroomView,       name='newsroom'),
	url(r'^contact_us/$',      		   					views.contactView,        name='contact_us'),
	url(r'^sign_up/$',         		   					views.signUpView,         name='sign_up'),
	url(r'^login/$',           		   					views.loginView,          name='login'),
	url(r'^logout/$',          		   					views.logoutView,         name='logout'),

	url(r'^user/dashboard/$',          					views.dashboardView,      name='user-dashboard'),

	url(r'^article/create/new/$',      					views.createArticleView,  name='create-article'),


	
]


