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
from orgo.engine.synthProblem import *

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

    

##What is still needed for this to be working?
    ##Need to have proper fields in problemInterface.html to replace
    ##Need to convert lists of molecules + reactionsteps to html
    ##Need to fix addReagent method so as to get rid of reagentBoxes altogether
    ##Eventually: also pass in synthesis solutions, somehow
    ##Eventually: how does the frontend know which synthesis problem it's working on?
def renderProblem(request):
    #Makes C#C
    c67 = Atom("C")
    c68 = Atom("C")
    ethylene = Molecule(c67)
    ethylene.addAtom(c68, c67, 3)

    #Makes C-C-Br
    c69 = Atom("C")
    br70 = Atom("Br")
    c71 = Atom("C")
    bromoethane = Molecule(c69)
    bromoethane.addAtom(c71, c69, 1)
    bromoethane.addAtom(br70, c69, 1)
    
    ##Replace this temporary code with a randomly generated synthesis problem, eventually
    start = MoleculeBox([ethylene])
    target = MoleculeBox([bromoethane])
    #reactionStep = ReactionStep(start)
    #reactionStep.addReagent(parseReagentString("H2 cat Lindlar"))
    #reactionSteps = [reactionStep]
    #problemSolution = SynthesisSolution([reactionStep, ReactionStep(reactionStep.productBox).addReagent(parseReagentString("HBr in CH2Cl2"))])
    
    
    return render(request, 'problemInterface.html', {"TargetMolecule":moleculeBoxHtml(target), "StartMolecule":moleculeBoxHtml(start)})
    
    
def renderNameReagent(request):
    problem = generateNameReagentProblem()
    profile = request.user.profile
    step = models.ReactionStepModel.create(problem)
    step.save()
    profile.currentNameReagentProblem = step
    profile.save()
    return render(request, 'problemInterface.html', {})
    
    
    
    
def checkSingleStepReaction(request):
    #Should figure out what the current starting material and final material are of the user's current single-step problem.
    #Should return a JSON object containing: whether or not the problem is right; the SVG of the molecule produced by the reaction.
    #The data in request will include a "reagents" field containing a string of reagents the user entered and dragged onto the starting material.
    return 
 
    
##Make this have a shiny flowchart layout once that becomes possible.
def moleculesAndReactionsHtml(startingMaterials, reactionSteps):
    html = ""
    startingMaterialsCopy = copy.deepcopy(startingMaterials)
    for startingMaterial in startingMaterialsCopy:
        keepgoing = True
        moleculeToCheck = startingMaterial
        while keepgoing:
            html += moleculeBoxHtml(moleculeToCheck)
            stepList = [reactionStep for reactionStep in reactionSteps if reactionStep.reactantBox == moleculeToCheck]
            if len(stepList) == 1:
                html += reactionStepHtml(stepList[0])
            elif len(stepList) == 0:
                keepgoing = False
                html += "<br/>"
            else:
                html += reactionStepHtml(stepList[0])
                
    
    return html
    
def moleculeBoxHtml(moleculeBox):
    html = "<div class = \"molecule\" class=\"ui-widget-content\"  >"
    html += serverRender.render(moleculeBox.stringList())
    html += "</div>"
    return html
    
def reactionStepHtml(reactionStep):
    html = ""
    for reagent in list(REAGENTS):
        if reactionStep.hasReagents[reagent]:
            html += REAGENTS[reagent][0] + ", "
            
    return "<div class = \"reaction\" class = \"ui-widget-content\">"+(html[:-2])+"<img src=\"http://felixsun.scripts.mit.edu/orgo/static/arrow.png\"/></div>"
    
