# Create your views here.
from django.shortcuts import render
from django.contrib.auth import *
from django.template import RequestContext
import orgo.engine.serverRender as serverRender
import orgo.engine.reactions as reactions
import orgo.models as models

def home(request, debug = "test"):
    #Home page.
    logout(request)
    outSmiles = reactions.smiles(reactions.mol)
    svg = serverRender.render(outSmiles)
    return render(request, 'index.html', {'molecule': svg, 'signUpForm': forms.UserCreationForm,
            'logInForm': forms.AuthenticationForm(), 'debug':debug},
            context_instance=RequestContext(request))

def signUp(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return loggedInHome(request)
        else:
            return home(request, debug = "Bad account info, please try again.")
            
def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Do log in check stuff
        user = authenticate(username = username, password = password)
        if user != None:
            return loggedInHome(request)
    return home(request, debug = "Invalid login, sorry.")
            
def loggedInHome(request):
    #Home page.
    outSmiles = reactions.smiles(reactions.CTmol)
    svg = serverRender.render(outSmiles)
    return render(request, 'index.html', {'molecule': svg})