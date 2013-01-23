# standard import to get access to models.Model
from django.db import models
import orgo.engine.orgoStructure as orgoStructure
from orgo.engine.synthProblem import *
import cPickle
import django.forms as forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

class PickledObjectField(models.Field):
    description = "An object."
    __metaclass__ = models.SubfieldBase
    
    def __init__ (self, *args, **kwargs):
        super(PickledObjectField, self).__init__(*args, **kwargs)
    
    #Loads a saved molecule pickle-thing to Python
    def to_python(self, value):
        if isinstance(value, unicode):
            if len(value) == 0:
                return None
            return cPickle.loads(str(value))
        return value

    
    #Pickles a molecule in preparation for database storage
    def get_prep_value(self, value):
        return cPickle.dumps(value)
    
    def db_type(self, connection):
        #No unlimited-length fields?
        return 'text'


"""
MoleculeBoxModel
Contains: foreignkey to a SynthesisProblemModel
Contains: pickled moleculebox
Contains: SVG representation
"""
class MoleculeBoxModel(models.Model):
    problemModel = models.ForeignKey('SynthesisProblemModel', null=True, on_delete=models.SET_NULL)
    moleculeBox = PickledObjectField(null=True)
    svg = models.TextField(null=True)
    equalsTarget = models.BooleanField()
    
    #Call MoleculeBoxModel.create(moleculeBoxObject) to create a MoleculeBoxModel representing moleculeBoxObject
    #moleculeBoxObject is an instance of MoleculeBox
    #parentSynthesisProblemModel is an instance of SynthesisProblemModel
    @classmethod
    def create(cls, moleculeBoxObject):
        x = cls(moleculeBox = moleculeBoxObject, svg = moleculeBoxObject.stringList(), equalsTarget = False)
        return x

    #target is an instance of MoleculeBoxModel
    #returns True or False, updates its own equalsTarget field with same
    def checkIfEqualsTarget(self, target):
        self.equalsTarget = boxEqualityChecker(self.moleculeBox, target.moleculeBox)
        return self.equalsTarget
        
        
#something to store arrows --> many to many field, ArrowModel{molecule box, molecule box, string}
class ArrowModel(models.Model):
    pointFrom = models.ForeignKey(MoleculeBoxModel, null=True, on_delete=models.SET_NULL, related_name="arrowPointsFrom")
    pointTo = models.ForeignKey(MoleculeBoxModel, null=True, on_delete=models.SET_NULL, related_name="arrowPointsTo")
    reagentsHtml = models.TextField(null=True)
    
    @classmethod
    #newPointFrom and newPointTo are MoleculeBoxModels
    #newReagentsHtml is a string
    def create(cls, newPointFrom, newPointTo, newReagentsHtml):
        x = cls(pointFrom = newPointFrom, pointTo = newPointTo, reagentsHtml = newReagentsHtml)
        x.save()
        return x        
    
        
"""
SynthesisProblemModel
Contains: pickled list of molecule-models by unique ID
Contains: pickled list of reaction-step-models by unique ID
Contains: pickled synthesis problem solution
Contains: ForeignKey to the final product the synthesis should produce
"""
    
    

class SolutionModel(models.Model):
    #something to store moleculeboxes --> many to many field, molecule box
    #something to store arrows --> many to many field, ArrowModel{molecule box, molecule box, string}
    molecules = models.ManyToManyField(MoleculeBoxModel, related_name="solutionMolecules")
    arrows = models.ManyToManyField(ArrowModel, related_name="solutionArrows")
    
    @classmethod
    def create(cls, reactionSteps):
        x = cls()
        x.save()
        
        (arrowmodels, moleculeboxmodels) = getArrowAndMoleculeModels(reactionSteps)  #helper method defined below
        
        for arrowmodel in arrowmodels: 
            x.arrows.add(arrowmodel)
            
        for moleculeboxmodel in moleculeboxmodels:
            assert moleculeboxmodel != None
            try:
                x.molecules.add(moleculeboxmodel)
            except:
                raise Exception("04")
        
        return x
    
    

    
#def ([arrowmodels], [moleculeboxmodels]) = getArrowAndMoleculeModels(reactionSteps)
#Helper method used by a constructor in models.
def getArrowAndMoleculeModels(reactionSteps):
    
    #Create dict of moleculeboxes : moleculeboxmodels 
    moleculedict = {}
    for reactionStep in reactionSteps:
        p = reactionStep.productBox
        r = reactionStep.reactantBox
        
        if not p in moleculedict.keys():
            newmodel = MoleculeBoxModel.create(p)
            newmodel.save()
            moleculedict[p] = newmodel
        if not r in moleculedict.keys():
            newmodel = MoleculeBoxModel.create(r)
            newmodel.save()
            moleculedict[r] = newmodel
    
    #Iterate through reactionsteps, creating a list of ArrowModels
    #ArrowModel.create(newPointFrom (a MoleculeBoxModel), newPointTo (a MoleculeBoxModel), newReagentsHtml (a html string)):
    arrowmodels = [ArrowModel.create(moleculedict[reactionStep.reactantBox],
                                    moleculedict[reactionStep.productBox],
                                    reactionStepHtml(reactionStep))
                   for reactionStep in reactionSteps]
    
    ##moleculeboxmodels = moleculedict.values()
    return (arrowmodels, moleculedict.values())
    
    
class SynthesisProblemModel(models.Model):
    #something to store solutions --> a SolutionModel
    #something to store moleculeboxes --> many to many field, molecule box
    #something to store arrows --> many to many field, ArrowModel{molecule box, molecule box, string}
    #target: a moleculeboxmodel foreignkey
    solution = models.ForeignKey(SolutionModel, null=True, on_delete=models.SET_NULL, related_name="spSolution")
    molecules = models.ManyToManyField(MoleculeBoxModel, related_name="spMolecules")
    arrows = models.ManyToManyField(ArrowModel, related_name="spArrows")
    target = models.ForeignKey(MoleculeBoxModel, null=True, on_delete=models.SET_NULL, related_name="spTarget")
    
    #reactionSteps is a list of reactionsteps; the final one contains the target molecule.
    @classmethod
    def create(cls, reactionSteps):
        
        assert len(reactionSteps) != 0
        
        #target molecule should be the final step's product
        t = MoleculeBoxModel.create(reactionSteps[-1].productBox)
        t.save()
        
        #solution should contain the other content of reactionSteps
        s = SolutionModel.create(reactionSteps)
        s.save()
        
        x = cls(target = t, solution = s)

        x.save()
        
        #arrows should be empty
        
        #molecules should contain the starting materials, which aren't the product of any reaction
        for moleculebox in getStartingMoleculeBoxes(reactionSteps): #helper method defined in synthProblem
            m = MoleculeBoxModel.create(moleculebox)
            m.checkIfEqualsTarget(t)
            m.save()
            try:
                x.molecules.add(m)
            except:
                raise Exception("05")
        
        return x
        
        
       
    #Return true if any item in molecules is equivalent to the target molecule
    #Most efficient way to do this: store a boolean field in every molecule box model created, for if it equals the target molecule
    #This requires calling checkIfEqualsTarget whenever a new molecule is added.
    def checkIfSolved(self):
        try:
            for moleculeBoxModel in self.molecules.all():
                if moleculeBoxModel.equalsTarget:
                    return True
            return False
        except:
            raise Exception("06")
        

            


"""
ReagentModel
Contains: foreignkey to a SynthesisProblemModel
Contains: pickled reagentbox
Contains: its own HTML representation
"""
#Unused
# class ReagentModel(models.Model):
    # problemModel = models.ForeignKey('SynthesisProblemModel')
    # reagentBox = PickledObjectField()
    # html = models.TextField()
    
    # Call ReagentModel.create(parentSynthesisProblemModel, reagentBoxObject) to create a ReagentModel representing reagentBoxObject
    # reagentBoxObject is an instance of ReagentBox
    # parentSynthesisProblemModel is an instance of SynthesisProblemModel
    # @classmethod
    # def create(cls, parentSynthesisProblemModel, reagentBoxObject):
        # x = cls(reagentBox = reagentBoxObject, problemModel = parentSynthesisProblemModel, html = reagentBoxObject.stringList())
        # return x


    
    
"""
ReactionStepModel
Contains: foreignkey to a SynthesisProblemModel
Contains: pickled reactionstep
Contains: HTML representation
"""
#Used in NameReagent
class ReactionStepModel(models.Model):
    reactionStep = PickledObjectField()
    reactantBox = models.ForeignKey('MoleculeBoxModel', related_name='reactant', null=True, on_delete=models.SET_NULL)
    productBox = models.ForeignKey('MoleculeBoxModel', related_name='product', null=True, on_delete=models.SET_NULL)
    html = models.TextField(null=True)
    done = models.BooleanField()
    catagory = models.CharField(max_length=100, null=True)
    
    #Call ReactionStepModel.create(parentSynthesisProblemModel, reactionStepObject) to create a ReactionStepModel representing reactionStepObject
    #reactionStepObject is an instance of ReactionStep
    #parentSynthesisProblemModel is an instance of SynthesisProblemModel
    @classmethod
    
    def create(cls, reactionStepObject):
        reactantBox = MoleculeBoxModel.create(reactionStepObject.reactantBox)
        reactantBox.save()
        productBox = MoleculeBoxModel.create(reactionStepObject.productBox)
        productBox.save()
        if hasattr(reactionStepObject, 'catagory'):
            catagory = reactionStepObject.catagory
        else:
            catagory = None
        x = cls(reactionStep = reactionStepObject, html = reactionStepObject.stringList(),
            reactantBox = reactantBox, productBox = productBox, catagory = catagory, done = False)
        return x

    

    
        
class mySignUpForm(UserCreationForm):
    #Just like the default user registration form, except with an email blank.
    email = forms.EmailField(required = True)
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    
###Can delete; this is me learning Django
#class MoleculeForm(forms.Form):
#    smiles = forms.CharField(max_length = 100)
#class MoleculeModel(models.Model):
#    smiles = models.CharField(max_length=100)    
#    @classmethod
    # def create(cls, s):
        # x = cls(smiles = s)
        # return x
        
class HelpWaitingList(models.Model):
    #A container to manage waiting users who NEED help.
    #For now, we will only have one instance of this, but eventually,
    #each class will have one.
    #Eventually, we will need additional fields (class, etc.)
    users = models.ManyToManyField(User, null=True, through='WaitTimer')
    @classmethod
    def create(cls):
        return cls()
        
class WaitTimer(models.Model):
    helpWaitingList = models.ForeignKey(HelpWaitingList)
    user = models.ForeignKey(User)
    lastCheck = models.DateTimeField(auto_now=True)  #auto_now automatically changes this field to now whenever the object is saved.
    
class ChatPair(models.Model):
    #A chat between two people, with asymmetric naming.
    helpee = models.ForeignKey(User, related_name='helpee')
    helpeeLastCheck = models.DateTimeField(null=True)
    helper = models.ForeignKey(User, related_name='helper')
    helperLastCheck = models.DateTimeField(null=True)    #Can't do auto_now, because there are two users to track.
    initTime = models.DateTimeField()
    chatRecord = models.ManyToManyField("ChatLine")
    @classmethod
    def create(cls, helpee, helper):
        return cls(helpee=helpee, helper=helper, initTime=timezone.now(), helpeeLastCheck=timezone.now(), helperLastCheck=timezone.now())
    
class ChatLine(models.Model):
    originator = models.ForeignKey(User)
    content = models.TextField()
    helpeeSeen = models.BooleanField(default=False)
    helperSeen = models.BooleanField(default=False)
    @classmethod
    def create(cls, originator):
        return cls(originator=originator, content="")
        
class ReagentType(models.Model):
    #A little class that saves a string describing each reagent type.
    name = models.CharField(max_length=100)
    @classmethod
    def create(cls, name):
        x = cls(name = name)
        return x
        
class AccuracyModel(models.Model):
    #A little class that tracks the # attempted and correct of each reaction catagory
    #for each user.
    catagory = models.CharField(max_length=100)
    correct = models.SmallIntegerField()
    total = models.SmallIntegerField()
    @classmethod
    def create(cls, catagory):
        x = cls(catagory=catagory, correct=0, total=0)
        return x
    
class UserProfile(models.Model):
    #A user profile - saves all the important stuff about each user, including
    #reactions-in-progress, diagnostic stats, and default problem settings.
    #More to come.
    
    #Use user.profile to get this UserProfile.
    user = models.ForeignKey(User, unique=True)
    currentNameReagentProblem = models.ForeignKey(ReactionStepModel,   null=True, on_delete=models.SET_NULL)
    currentSynthesisProblem = models.ForeignKey(SynthesisProblemModel, null=True, on_delete=models.SET_NULL)
    savedReagentTypes = models.ManyToManyField(ReagentType)
    accuracies = models.ManyToManyField(AccuracyModel)
    #savedProblem = models.ForeignKey(SynthesisProblemModel)
    
#Auto-make a UserProfile for each user when needed
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class ChooseReagentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ChooseReagentsForm, self).__init__(*args, **kwargs)
        sortedNames = sorted(typeToReaction.items(), key=lambda thing: thing[0])
        for name, unused in sortedNames:
            self.fields[name] = forms.BooleanField(label=name, initial=True, required=False)
            


    
