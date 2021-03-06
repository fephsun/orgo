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
    url(r'^api/returnReagentHtml/$', 'orgo.views.makeReagentHtml', name='makeReagentHtml'),
    url(r'^api/resetPW/$', 'orgo.views.resetPW', name='resetPW'),
    url(r'^api/changePW/$', 'orgo.views.changePW', name='changePW'),
    url(r'^logout/$', 'orgo.views.logOut', name='logOut'),
    url(r'^api/problemInterface/$', 'orgo.views.renderProblem', name='renderProblem'),    
    url(r'^api/checkSingleStepReaction/$', 'orgo.views.checkNameReagent', name='checkNameReagent'), 
    url(r'^api/showSingleStepAnswer/$', 'orgo.views.showNRAnswer', name='showNRAnswer'),   
    url(r'^api/outpsmiles/$', 'orgo.views.outpSmiles', name='outpSmiles'),  ###Can delete; this is me learning Django  
    url(r'^homeMoleculeChanger/$', 'orgo.views.homeMoleculeChanger', name='homeMoleculeChanger'),
    url(r'^chat/helperpoll/$', 'orgo.views.helperWaitPoll', name='helperWaitPoll'),
    url(r'^chat/helpeepoll/$', 'orgo.views.helpeeWaitPoll', name='helpeeWaitPoll'),
    url(r'^chat/askforhelp/$', 'orgo.views.askForHelp', name='askForHelp'),
    url(r'^chat/volunteertohelp/$', 'orgo.views.volunteerToHelp', name='volunteerToHelp'),
    url(r'^chat/helpeechatpoll/$', 'orgo.views.helpeeChatPoll', name='helpeeChatPoll'),
    url(r'^chat/helperchatpoll/$', 'orgo.views.helperChatPoll', name='helperChatPoll'),
    
    url(r'^renderProblem/$', 'orgo.views.renderProblem', name='renderProblem'),
    
    url(r'^renderSynthesis/$', 'orgo.views.renderSynthesis', name='renderSynthesis'),
    url(r'^renderSynthesis/resume/$', 'orgo.views.renderOldSynthesis', name='renderOldSynthesis'),
    url(r'^namereagent/$', 'orgo.views.renderNameReagent', name='renderNameReagent'),
    url(r'^namereagent/resume/$', 'orgo.views.renderOldNameReagent', name='renderOldNameReagent'),
                       
                       
    url(r'^reactions/$', 'orgo.views.renderReactions', name='renderReactions'),
    url(r'^faq/$', 'orgo.views.renderFaq', name='renderFaq'),
    
    
    url(r'^api/getSynthesisData/$', 'orgo.views.getSynthesisData', name = 'getSynthesisData'),
    url(r'^api/displaySolution/$', 'orgo.views.getSolutionData', name = 'getSolutionData'),
    url(r'^api/addMoleculeToMolecule/$', 'orgo.views.addMoleculeToMolecule', name = 'addMoleculeToMolecule'),
    url(r'^api/addReagentToMolecule/$', 'orgo.views.addReagentToMolecule', name = 'addReagentToMolecule'),
    url(r'^api/deleteMolecule/$', 'orgo.views.deleteMolecule', name = 'deleteMolecule'),
    url(r'^api/saveProblem/$', 'orgo.views.saveProblem', name = 'saveProblem'),
    url(r'^loadSynthesisFromId/$', 'orgo.views.loadSynthesisFromId', name = 'loadSynthesisFromId'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)





if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

