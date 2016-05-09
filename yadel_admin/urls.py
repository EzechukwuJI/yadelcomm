from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

from yadel_admin import views


# Create your urls here.
urlpatterns  =  [
             
	url(r'^$',                                   				      		views.indexView,                name='admin-index'),
	url(r'^dashboard/submissions/(?P<status>[-\w]+)/$',               		views.adminDashboardView,       name='admin-dashboard'),
	url(r'^dashboard/user-manager/$',            				      		views.adminUserManager,         name='user-manager'),
	url(r'^dashboard/content-manager/$',            				  		views.contentManager,        	name='content-manager'),
	url(r'^article/(?P<pk>[-\d]+)/action=(?P<action>[-\w]+)/$',       		views.publishArticle,           name='publish-article'),
	url(r'^delete_content/(?P<pk>[-\d]+)/model=(?P<model>[-\w]+)/$',       views.delete_content,            name='delete-content'),
	
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


