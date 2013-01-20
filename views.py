# Create your views here.
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import orgo.engine.serverRender as serverRender
import orgo.engine.reactions as reactions
import orgo.engine.randomGenerator as randomGenerator
import orgo.engine.orgoStructure as orgoStructure
import orgo.models as models
from orgo.engine.synthProblem import *

def home(request, debug = ""):
    #Home page.
    if request.user.is_authenticated():
        return loggedInHome(request)
    outSmiles = reactions.smiles(randomGenerator.randomStart()[0])
    svg = serverRender.render(outSmiles)
    return render(request, 'index.html', {'molecule': svg, 'signUpForm': models.mySignUpForm,
            'logInForm': forms.AuthenticationForm(), 'debug':debug , 'outpSmilesForm': models.MoleculeForm})###Can delete "outpSmilesForm" term; this is me learning Django     

def signUp(request):
    if request.method == 'POST':
        form = models.mySignUpForm(request.POST)
        if form.is_valid():
            form.save()
            newUser = authenticate(username = form.cleaned_data['username'], 
                password = form.cleaned_data['password1'])
            login(request, newUser)
            return loggedInHome(request)
        else:
            return home(request, debug = "<span style=\"color:FF0000\">Bad account info, please try again.</span>")
            
def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Do log in check stuff
        user = authenticate(username = username, password = password)
        if user != None:
            login(request, user)
            return loggedInHome(request)
    return home(request, debug = "<span style=\"color:FF0000\">Invalid login, sorry.</span>")
    


def logOut(request):
    logout(request)
    return home(request)






#@login_required
#def returnToLoggedInHome(request):
#    return loggedInHome(request)

    

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
##def renderProblem(request):
##    #Makes C#C
##    c67 = Atom("C")
##    c68 = Atom("C")
##    ethylene = Molecule(c67)
##    ethylene.addAtom(c68, c67, 3)
##
##    #Makes C-C-Br
##    c69 = Atom("C")
##    br70 = Atom("Br")
##    c71 = Atom("C")
##    bromoethane = Molecule(c69)
##    bromoethane.addAtom(c71, c69, 1)
##    bromoethane.addAtom(br70, c69, 1)
##    
##    ##Replace this temporary code with a randomly generated synthesis problem, eventually
##    start = MoleculeBox([ethylene])
##    target = MoleculeBox([bromoethane])
##    #reactionStep = ReactionStep(start)
##    #reactionStep.addReagent(parseReagentString("H2 cat Lindlar"))
##    #reactionSteps = [reactionStep]
##    #problemSolution = SynthesisSolution([reactionStep, ReactionStep(reactionStep.productBox).addReagent(parseReagentString("HBr in CH2Cl2"))])  
##    return render(request, 'problemInterface.html', {"TargetMolecule":moleculeBoxHtml(target), "StartMolecule":moleculeBoxHtml(start)})
    
    
@login_required    
def renderOldNameReagent(request):
    profile = request.user.profile
    step = profile.currentNameReagentProblem
    if step == None:
        return renderNameReagent(request)
    return render(request, 'problemInterface.html', {"ReactantMolecule": step.reactantBox.svg, "TargetMolecule": step.productBox.svg, "Name": request.user.username})
    
@login_required
def renderNameReagent(request):
    problem = generateNameReagentProblem(AlkeneAlkyneMode)
    profile = request.user.profile
    step = models.ReactionStepModel.create(problem)
    step.save()
    profile.currentNameReagentProblem = step
    profile.save()
    return render(request, 'problemInterface.html', {"ReactantMolecule": step.reactantBox.svg, "TargetMolecule": step.productBox.svg, "Name": request.user.username})
    #return render(request, 'problemInterface.html', {"ReactantMolecule": orgoStructure.smiles(problem.reactantBox.molecules), "TargetMolecule": orgoStructure.smiles(problem.productBox.molecules), "Name": request.user.username})

@csrf_exempt
def checkNameReagent(request):
    #Takes in a list of reagents that the user guessed.
    #Returns whether that list is correct, plus the actual product, if that list is incorrect.
    if request.method == 'POST':
        reagentsDict = parseReagentsString(request.POST['reagents'])
        reactant = request.user.profile.currentNameReagentProblem.reactantBox.moleculeBox
        target = request.user.profile.currentNameReagentProblem.productBox.moleculeBox
        testStep = ReactionStep(reactant)
        testStep.hasReagents = reagentsDict
        try:
            correct, products = testStep.checkStep(target)
        except:
            tb = traceback.format_exc()
            correct = True
            products = str(tb)
        responseData = dict()
        responseData["success"] = correct
        if isinstance(products, str):
            responseData["product"] = products
        else:
            responseData["product"] = products.stringList()
        #If we have the correct answer, free up some database space by deleting this stuff.
        if correct == True:
            request.user.profile.currentNameReagentProblem.reactantBox.delete()
            request.user.profile.currentNameReagentProblem.productBox.delete()
            request.user.profile.currentNameReagentProblem.delete()
            #Later: update analytics.
            
        return HttpResponse(json.dumps(responseData))

 
    
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

@csrf_exempt
def makeReagentHtml(request):
    try:
        reagentString = request.reagentString
        dict = parseReagentsString(reagentString)
        html = ""
        for reagent in list(dict):
            if dict[reagent]:
                html += REAGENTS[reagent][0] + ", "
        htmlOutput =  "<li class=\"reagent\" class = \"ui-state-default\" reagentString = \""+reagentString+"\">"+html[:-2]+"<img src=\"http://felixsun.scripts.mit.edu/orgo/static/arrow.png\"/></li>"
        return HttpResponse(htmlOutput)
    except:
        tb = traceback.format_exc()
        return HttpResponse(str(tb))
