from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'orgo.views.home', name='home'),
    url(r'^api/signup/$', 'orgo.views.signUp', name='signUp'),
#    url(r'^api/home/$', 'orgo.views.returnToLoggedInHome', name='returnToLoggedInHome'),
    url(r'^api/login/$', 'orgo.views.logIn', name='logIn'),
    url(r'^logout/$', 'orgo.views.logOut', name='logOut'),
    url(r'^api/problemInterface/$', 'orgo.views.renderProblem', name='renderProblem'),    
    url(r'^api/checkSingleStepReaction/$', 'orgo.views.checkNameReagent', name='checkNameReagent'),    
    url(r'^api/outpsmiles/$', 'orgo.views.outpSmiles', name='outpSmiles'),  ###Can delete; this is me learning Django  
    url(r'^homeMoleculeChanger/$', 'orgo.views.homeMoleculeChanger', name='homeMoleculeChanger'),
    url(r'^namereagent/$', 'orgo.views.renderNameReagent', name='renderNameReagent'),
    url(r'^namereagent/resume/$', 'orgo.views.renderOldNameReagent', name='renderOldNameReagent'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)





if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

