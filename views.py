# Create your views here.
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
import orgo.engine.serverRender as serverRender
import orgo.engine.reactions as reactions
import orgo.models as models

def home(request, debug = ""):
    #Home page.
    logout(request)
    outSmiles = reactions.smiles(reactions.mol)
    svg = serverRender.render(outSmiles)
    return render(request, 'index.html', {'molecule': svg, 'signUpForm': models.mySignUpForm,
            'logInForm': forms.AuthenticationForm(), 'debug':debug})

def signUp(request):
    if request.method == 'POST':
        form = models.mySignUpForm(request.POST)
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
            login(request, user)
            return loggedInHome(request)
    return home(request, debug = "Invalid login, sorry.")
            
@login_required
def loggedInHome(request):
    #Home page for those who have logged in.
    name = request.user.username
    return render(request, 'loggedin.html', {'name': name})