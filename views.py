# Create your views here.
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
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
    return render(request, 'index.html', {'molecule': svg,
                                          'signUpForm': models.mySignUpForm,
                                          'logInForm': forms.AuthenticationForm(),
                                          'debug':debug , 
                                          'resetPWForm': PasswordResetForm()})

def signUp(request):
    if request.method == 'POST':
        form = models.mySignUpForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']):
                #Non-unique email - not allowed!
                return home(request, debug="Someone else has already registered with this email!")
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

def resetPW(request):
    if request.method == 'POST':
        #Use built-in Django magic to reset a user's password and send him an email.
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except:
            return home(request, debug = "The email you entered does not correspond to any user.")
        password = User.objects.make_random_password()
        user.set_password(password)
        subject = "Orgo - your new password"
        body = 'Hello '+user.username+''',
Here is your new password: ''' + password + '''
Because this password was sent over email, it is not secure as a permanent password.  Please log in and change it immediately.
Thank you,
Your friendly admins'''
        newMessage = EmailMessage(subject, body, to=[email])
        newMessage.send()
        return render(request, 'successfulReset.html')
    return home(request, debug = "Unknown error in password reset")
    
    
def changePW(request):
    #Change the user's password.
    if request.method == 'POST':
        if authenticate(username=request.user.username, password=request.POST['old_password']) == None:
            return loggedInHome(request, debug="Your old password is incorrect.")
        if request.POST['new_password1'] != request.POST['new_password2']:
            return loggedInHome(request, debug="Your two new passwords don't match.")
        request.user.set_password(request.POST['new_password1'])
        return loggedInHome(request, debug="Password changed successfully.")
        #old_password, new_password1, new_password2


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
def loggedInHome(request, debug = ""):
    #Home page for those who have logged in.
    profile = request.user.profile
    #Set up the ChooseReagentsForm with the last choices the user made.
    initialValuesDict = dict()
    graphList = []
    for name, reactions in typeToReaction.items():
        try:
            profile.savedReagentTypes.get(name=name)
        except:
            initialValuesDict[name] = False
        else:
            initialValuesDict[name] = True
        #Load up the graph data
        try:
            accuracyObj = profile.accuracies.get(catagory=name)
        except:
            pass
        else:
            graphList.append([1.0*accuracyObj.correct/accuracyObj.total, name, accuracyObj.correct, accuracyObj.total])
    graphList.sort(key=lambda item: item[1])

    return render(request, 'loggedin.html', {'name': request.user.username, 
                                             'ChooseReagentsForm':models.ChooseReagentsForm(initial=initialValuesDict), 
                                             'debug': debug,
                                             'graphData': graphList,
                                             'changePW': PasswordChangeForm(request.user)})
    
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
    profile = request.user.profile
    #Sometimes, the user doesn't even have a previous problem, so deleting doesn't always work.
    try:
        temp1 = profile.currentNameReagentProblem.productBox
        temp2 = profile.currentNameReagentProblem.reactantBox
        profile.currentNameReagentProblem.delete()
        temp1.delete()
        temp2.delete()
    except:
        pass
        
       
    modes = checkboxUpdate(request)
    if modes == []:
        #Error - at least one mode must be selected!
        return loggedInHome(request, debug = "You must pick at least one reaction type!")
        
    problem = generateNameReagentProblem(modes)
    step = models.ReactionStepModel.create(problem)
    step.save()
    profile.currentNameReagentProblem = step
    profile.save()
    return render(request, 'problemInterface.html', {"ReactantMolecule": step.reactantBox.svg, "TargetMolecule": step.productBox.svg, "Name": request.user.username})
        
        
def checkboxUpdate(request): 
    profile = request.user.profile       
    modes = []
    if request.method == 'POST':
        #User filled out the checkboxes
        #First, clear the user's savedReagentTypes
        profile.savedReagentTypes.clear()
        #Parse and save which reaction types were checked.
        checkboxes = models.ChooseReagentsForm(request.POST)
        if checkboxes.is_valid():
            for name, reactions in typeToReaction.items():
                if checkboxes.cleaned_data[name]:
                    modes.append(name)
                    try:
                        reagentType = models.ReagentType.objects.get(name = name)
                    except:
                        #Make a new reagentType.  (We only need to do this once after we update our reagent types.)
                        reagentType = models.ReagentType.create(name = name)
                        reagentType.save()
                    profile.savedReagentTypes.add(reagentType)
    else:
        #User clicked on "new problem"
        #Load up the user's reagent preferences.
        for reagentTypeInstance in profile.savedReagentTypes.all():
            modes.append(reagentTypeInstance.name)
    return modes


    
@csrf_exempt
def checkNameReagent(request):
    #Takes in a list of reagents that the user guessed.
    #Returns whether that list is correct, plus the actual product, if that list is incorrect.
    if request.method == 'POST':
      try:
        reagentsDict = parseReagentsString(request.POST['reagents'])
        profile = request.user.profile
        reactant = profile.currentNameReagentProblem.reactantBox.moleculeBox
        target = profile.currentNameReagentProblem.productBox.moleculeBox
        testStep = ReactionStep(reactant)
        #If the problem is done, do nothing - don't let them get more points.
        if profile.currentNameReagentProblem.done:
            return HttpResponse("")
        testStep.hasReagents = reagentsDict
        correct, products = testStep.checkStep(target)
        responseData = dict()
        responseData["success"] = correct
        if isinstance(products, str):
            responseData["product"] = products
        else:
            responseData["product"] = products.stringList()
        #If we have the correct answer, free up some database space by deleting this stuff.
        thisCatagory = profile.currentNameReagentProblem.catagory
        try:
            accModel = profile.accuracies.get(catagory=thisCatagory)
        except:
            accModel = models.AccuracyModel.create(catagory=thisCatagory)
            accModel.save()
            profile.accuracies.add(accModel)
        if correct == True:
            accModel.correct += 1
            accModel.total += 1
            accModel.save()
            profile.currentNameReagentProblem.done = True
            profile.currentNameReagentProblem.save()
        else:
            accModel.total += 1
            accModel.save()
      except StandardError as e:
        responseData = dict()
        responseData["product"] = str(e)
        responseData["success"] = False
        
      return HttpResponse(json.dumps(responseData))
      
@csrf_exempt
def showNRAnswer(request):
    out = request.user.profile.currentNameReagentProblem.html
    htmlOutput =  "<li class=\"reagent\" class = \"ui-state-default\" >"+out+"<img src=\"http://felixsun.scripts.mit.edu/orgo/static/arrow.png\"/></li>"
    #Mark this problem as done.
    request.user.profile.currentNameReagentProblem.done = True
    request.user.profile.currentNameReagentProblem.save()
    return HttpResponse(htmlOutput)
 
    
##Make this have a shiny flowchart layout once that becomes possible.
##Obsolete? Not convinced this is actually used anywhere.
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
    
@csrf_exempt
def makeReagentHtml(request):
    try:
        reagentString = request.POST['reagentString']
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
        
        
        
        
###Some methods for displaying and operating with giant synthesis problems.
@login_required
def renderOldSynthesis(request):
    profile = request.user.profile
    synthesis = profile.currentSynthesisProblem
    if synthesis == None:
        return renderSynthesis(request)
    return render(request, 'synthesisProblemInterface.html', {"TargetMolecule": synthesis.target.svg, "Name": request.user.username})



@login_required
def renderSynthesis(request):
    profile = request.user.profile
    #Sometimes, the user doesn't even have a previous problem, so deleting doesn't always work.
    try:
        profile.currentSynthesisProblem.target.delete()
        profile.currentSynthesisProblem.delete()
    except:
        pass
    
    modes = checkboxUpdate(request)
    if modes == []:
        #Error - at least one mode must be selected!
        return loggedInHome(request, debug = "You must pick at least one reaction type!")
        
    reactionsteps = randomSynthesisProblemMake(modes)
    synthesis = models.SynthesisProblemModel.create(reactionsteps)
    synthesis.save()
    profile.currentSynthesisProblem = synthesis
    profile.save()
    
    return render(request, 'synthesisProblemInterface.html', {"TargetMolecule": synthesis.target.svg, "Name": request.user.username})

    
#Other to-do:
    #addMoleculeToMolecule in views
    #addReagentToMolecule in views
    #add buttons in loggedin page to link to api/renderSynthesis and api/renderSynthesis/resume
    #MoleculeBoxModelinstance.checkIfEqualsTarget()

    

def getSynthesisData(request):
    #Should return a JSON string with the following attributes contained:
    #molecules is an array of arrays: [ [idnumber, "<svg>...</svg>"], ... ]
    #arrows is an array of arrays: [ [idnumber1, idnumber2, "reagentText"], ...]
    #success   -- a boolean (true/false)
    
    synthesis = profile.currentSynthesisProblem
    
    
    #Iterate over all molecules for a specific synthesis
    moleculesOutput = [ (moleculeBoxModel.id, moleculeBoxModel.svg) 
                        for moleculeBoxModel in synthesis.molecules.all()]
    
    #Iterate over all arrows for a specific synthesis
    arrowsOutput = [ (arrowModel.pointFrom.id, arrowModel.pointTo.id, arrowModel.reagentsHtml)
                     for arrowModel in synthesis.arrows.all()]
    
    responseData = dict()
    
    responseData["success"] = synthesis.checkIfSolved()
    responseData["molecules"] = moleculesOutput
    responseData["arrows"] = arrowsOutput

    return HttpResponse(json.dumps(responseData))
    

@csrf_exempt
#data: {'molecule1': ui.draggable.attr("id"), 'molecule2': this.attr("id")}
def addMoleculeToMolecule(request):
    #Create a new moleculebox, combining the two inputs into one box, appending it to synthesis.molecules
    #Make sure to check whether they react with each other
    #Create two new arrows, with empty reagents, correctly attached
    
    return getSynthesisData(request)

    
    
@csrf_exempt
#data: {'reagents': ui.draggable.attr("reagentString"), 'moleculeOn': this.attr("id")}
def addReagentToMolecule(request):
    #Do this via creating a reactionstep
    #Create a new moleculebox, representing the reaction's products
    #Create a new arrow, containing html of reagents, from reactants to products

    return getSynthesisData(request)

