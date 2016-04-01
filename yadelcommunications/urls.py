from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yadelcommunications.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/',                            include(admin.site.urls)),
    url(r'^',                                          include('yadel_main.urls',    namespace       =  'yadel_main'  )),
    url(r'^admin-dashboard/',        include('yadel_admin.urls',   namespace      =    'yadel_admin'  )),
)
