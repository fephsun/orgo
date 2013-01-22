# standard import to get access to models.Model
from django.db import models
import orgo.engine.orgoStructure as orgoStructure
from orgo.engine.synthProblem import *
import cPickle
import django.forms as forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from south.modelsinspector import add_introspection_rules

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

#Allow Django South to introspect the PickledObject field.
add_introspection_rules([], ["^orgo\.models\.PickledObjectField"])
        
"""
MoleculeBoxModel
Contains: foreignkey to a SynthesisProblemModel
Contains: pickled moleculebox
Contains: SVG representation
"""
class MoleculeBoxModel(models.Model):
    problemModel = models.ForeignKey('SynthesisProblemModel', null=True, on_delete=models.SET_NULL)
    moleculeBox = PickledObjectField()
    svg = models.TextField()
    
    #Call MoleculeBoxModel.create(paXrentSynthesisProblemModel, moleculeBoxObject) to create a MoleculeBoxModel representing moleculeBoxObject
    #moleculeBoxObject is an instance of MoleculeBox
    #parentSynthesisProblemModel is an instance of SynthesisProblemModel
    @classmethod
    def create(cls, moleculeBoxObject, parentSynthesisProblemModel=None):
        x = cls(moleculeBox = moleculeBoxObject, problemModel = parentSynthesisProblemModel, svg = moleculeBoxObject.stringList())
        return x

    
        
"""
SynthesisProblemModel
Contains: pickled list of molecule-models by unique ID
Contains: pickled list of reaction-step-models by unique ID
Contains: pickled synthesis problem solution
Contains: ForeignKey to the final product the synthesis should produce
"""
#PUT STUFF HERE
class SynthesisProblemModel(models.Model):
#    moleculeModels = PickledObjectField()
#    reactionStepModels = PickledObjectField()
#    solution = PickledObjectField()
#    target = models.ForeignKey(MoleculeBoxModel)
    
    
    #Call SynthesisProblemModel.create(parentSynthesisProblem) to create a SynthesisProblemModel representing parentSynthesisProblem
    #parentSynthesisProblem is an instance of SynthesisProblem
    @classmethod
    def create(cls, parentSynthesisProblem):
        #Make models for each of the moleculeboxes and reactionsteps
        #Make lists of their ids
        #Pickle all the things
        
        
        #Attributes found in SynthesisProblem:
        #self.startingBoxes = []                 #a list of instances of MoleculeBox
        #self.finalProduct = None                #an instance of MoleculeBox
        #self.steps = []                         #a list of instances of ReactionStep, in any order
        #self.solution = solution                #an instance of SynthesisSolution
        pass



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
    html = models.TextField()
    
    #Call ReactionStepModel.create(parentSynthesisProblemModel, reactionStepObject) to create a ReactionStepModel representing reactionStepObject
    #reactionStepObject is an instance of ReactionStep
    #parentSynthesisProblemModel is an instance of SynthesisProblemModel
    @classmethod
    def create(cls, reactionStepObject):
        reactantBox = MoleculeBoxModel.create(reactionStepObject.reactantBox)
        reactantBox.save()
        productBox = MoleculeBoxModel.create(reactionStepObject.productBox)
        productBox.save()
        x = cls(reactionStep = reactionStepObject, html = reactionStepObject.stringList(),
            reactantBox = reactantBox, productBox = productBox)
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
        
class ReagentType(models.Model):
    #A little class that saves a string describing each reagent type.
    name = models.CharField(max_length=100)
    @classmethod
    def create(cls, name):
        x = cls(name = name)
        return x
    
class UserProfile(models.Model):
    #A user profile - saves all the important stuff about each user, including
    #reactions-in-progress, diagnostic stats, and default problem settings.
    #More to come.
    
    #Use user.profile to get this UserProfile.
    user = models.ForeignKey(User, unique=True)
    currentNameReagentProblem = models.ForeignKey(ReactionStepModel, null=True, on_delete=models.SET_NULL)
    savedReagentTypes = models.ManyToManyField(ReagentType)
    #savedProblem = models.ForeignKey(SynthesisProblemModel)
    
#Auto-make a UserProfile for each user when needed
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class ChooseReagentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ChooseReagentsForm, self).__init__(*args, **kwargs)
        sortedNames = sorted(typeToReaction.items(), key=lambda thing: thing[0])
        for name, unused in sortedNames:
            self.fields[name] = forms.BooleanField(label=name, initial=True, required=False)
            


    
