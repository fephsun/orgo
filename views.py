# Create your views here.
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import orgo.engine.serverRender as serverRender
import orgo.engine.reactions as reactions
import orgo.engine.randomGenerator as randomGenerator
import orgo.models as models

def home(request, debug = ""):
    #Home page.
    logout(request)
    outSmiles = reactions.smiles(randomGenerator.randomStart()[0])
    svg = serverRender.render(outSmiles)
    return render(request, 'index.html', {'molecule': svg, 'signUpForm': models.mySignUpForm,
            'logInForm': forms.AuthenticationForm(), 'debug':debug , 'outpSmilesForm': models.MoleculeForm})###Can delete "outpSmilesForm" term; this is me learning Django     

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

###Can delete; this is me learning Django
def outpSmiles(request):
    if request.method == 'POST':
        form = models.MoleculeForm(request.POST)
        if form.is_valid():
            molecule = models.MoleculeModel.create(request.POST['smiles'])
            molecule.save()
            return renderSmiles(request, molecule)
    
    
@csrf_exempt
def homeMoleculeChanger(request):
    #Returns new molecules for the AJAX tester (home molecule changer)
    outSmiles = reactions.smiles(randomGenerator.randomStart()[0])
    svg = serverRender.render(outSmiles)
    return HttpResponse(svg)
            
@login_required
def loggedInHome(request):
    #Home page for those who have logged in.
    name = request.user.username
    return render(request, 'loggedin.html', {'name': name})
    
###Can delete; this is me learning Django
def renderSmiles(request, molecule):
    return render(request, 'loggedin.html', {'item1': serverRender.render(str(molecule.smiles))})

    
    
def renderProblem(request):
    start = MoleculeBox([ethylene])
    target = MoleculeBox([bromoethane])
    reagentBox = ReagentBox("H2 cat Lindlar")
    reactionStep = ReactionStep(start)
    reactionStep.addReagent(reagentBox)
    reactionSteps = [reactionStep]
    sidebarReagents = [reagentBox]
    problemSolution = SynthesisSolution([reactionStep, ReactionStep(reactionStep.productBox).addReagent(ReagentBox("HBr in CH2Cl2"))])
    return render(request, 'problemInterface.html', {})