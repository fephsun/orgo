# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate
import orgo.engine.serverRender as serverRender
import orgo.engine.reactions as reactions
import orgo.models as models

def home(request):
    #Home page.
    outSmiles = reactions.smiles(reactions.mol)
    svg = serverRender.render(outSmiles)
    return render(request, 'index.html', {'molecule': svg, 'signUpForm': models.UserForm(),
            'logInForm': models.LogInForm()})

def signUp(request):
    if request.method == 'POST':
        form = models.UserForm(request.POST)
        if form.is_valid():
            form.save()
            return loggedInHome(request)
        else:
            return home(request)
            
def logIn(request):
    if request.method == 'POST':
        form = models.LogInForm(request.POST)
        if form.is_valid():
            #Do log in check stuff
            user = authenticate(username = form.cleaned_data['username'],
                password = form.cleaned_data['password'])
            if user != None:
                return loggedInHome(request)
        
    return home(request)
            
def loggedInHome(request):
    #Home page.
    outSmiles = reactions.smiles(reactions.CTmol)
    svg = serverRender.render(outSmiles)
    return render(request, 'index.html', {'molecule': svg, 'form':models.UserForm()})