from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from yadel_main import views


# Create your urls here.
urlpatterns  =  [
             
	url(r'^$',                         					views.indexView,          name='index'),
	url(r'^about_us/$',                					views.aboutUsView,        name='about_us'),
	url(r'^services/(?P<service_type>[-\w]+)/$',        views.servicesView,       name='services'),
	url(r'^newsroom/$',                					views.newsroomView,       name='newsroom'),
	url(r'^contact_us/$',      		   					views.contactView,        name='contact_us'),
	url(r'^sign_up/$',         		   					views.signUpView,         name='sign_up'),
	url(r'^login/$',           		   					views.loginView,          name='login'),
	url(r'^logout/$',          		   					views.logoutView,         name='logout'),
	url(r'^accounts/posts/$',          	                views.dashboardView,      name='user-dashboard'),
	url(r'^terms-and-conditions/$',          		    views.TandCView,          name='tandc'),

	# url(r'^client/feedback/$',                          views.clientFeedback,           name = 'user-feedback'),
	url(r'^article/create/new/$',      					views.createArticleView,  name='create-article'),
	url(r'^thank-you/$',      					        TemplateView.as_view(template_name = "yadel/general/thank-you.html"), name='registration_success'),
	url(r'^confirm-registration/(?P<code>[-\w]+)/$',    views.confirmEmail, name = 'confirm-email'),
	# url(r'^news/(?P<pk>[-\d]+)/(?P<news_title>[-\w]+)/url=(?P<url_link>[-\w]+)/$',  views.loadExternalNews, name = 'news-details')

	url(r'^news/(?P<pk>[-\d]+)/(?P<news_title>[-\w]+)/$',  views.loadExternalNews, name = 'news-details')

	]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)