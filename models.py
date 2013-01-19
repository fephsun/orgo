# standard import to get access to models.Model
from django.db import models
import orgo.engine.orgoStructure as orgoStructure
import cPickle
import django.forms as forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PickledObjectField(models.Field):
    description = "An object."
    __metaclass__ = models.SubfieldBase
    
    def __init__ (self, *args, **kwargs):
        super(PickledObjectField, self).__init__(*args, **kwargs)
    
    #Loads a saved molecule pickle-thing to Python
    def to_python(self, value):
        if isinstance(value, orgoStructure.Molecule):
            return value
        return cPickle.loads(value)
    
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
    problemModel = models.ForeignKey('SynthesisProblemModel')
    moleculeBox = PickledObjectField()
    svg = models.TextField()
    
    #Call MoleculeBoxModel.create(parentSynthesisProblemModel, moleculeBoxObject) to create a MoleculeBoxModel representing moleculeBoxObject
    #moleculeBoxObject is an instance of MoleculeBox
    #parentSynthesisProblemModel is an instance of SynthesisProblemModel
    @classmethod
    def create(cls, parentSynthesisProblemModel, moleculeBoxObject):
        x = cls(MoleculeBox = moleculeBoxObject, problemModel = parentSynthesisProblemModel, svg = moleculeBoxObject.stringList())
        return x
        
"""
SynthesisProblemModel
Contains: pickled list of molecule-models by unique ID
Contains: pickled list of reagent-models by unique ID
Contains: pickled list of reaction-step-models by unique ID
Contains: pickled synthesis problem solution
"""
class SynthesisProblemModel(models.Model):
    moleculeModels = PickledObjectField()
    reagentModels = PickledObjectField()
    reactionStepModels = PickledObjectField()
    solution = PickledObjectField()
    target = models.ForeignKey(MoleculeBoxModel)
    
    
    #Call SynthesisProblemModel.create(parentSynthesisProblem) to create a SynthesisProblemModel representing parentSynthesisProblem
    #parentSynthesisProblem is an instance of SynthesisProblem
    @classmethod
    def create(cls, parentSynthesisProblem):
        #Make models for each of the moleculeboxes, reagentboxes, and reactionsteps
        #Make lists of their ids
        #Pickle all the things
        
        
        #Attributes found in SynthesisProblem:
        #self.startingBoxes = []                 #a list of instances of MoleculeBox
        #self.finalProduct = None                #an instance of MoleculeBox
        #self.steps = []                         #a list of instances of ReactionStep, in any order
        #self.reagentsMade = []                  #a list of instances of ReagentBox, for the sidebar
        #self.solution = solution                #an instance of SynthesisSolution
        pass
    



"""
ReagentModel
Contains: foreignkey to a SynthesisProblemModel
Contains: pickled reagentbox
Contains: its own HTML representation
"""
class ReagentModel(models.Model):
    problemModel = models.ForeignKey('SynthesisProblemModel')
    reagentBox = PickledObjectField()
    html = models.TextField()
    
    #Call ReagentModel.create(parentSynthesisProblemModel, reagentBoxObject) to create a ReagentModel representing reagentBoxObject
    #reagentBoxObject is an instance of ReagentBox
    #parentSynthesisProblemModel is an instance of SynthesisProblemModel
    @classmethod
    def create(cls, parentSynthesisProblemModel, reagentBoxObject):
        x = cls(reagentBox = reagentBoxObject, problemModel = parentSynthesisProblemModel, html = reagentBoxObject.stringList())
        return x
    
    
"""
ReactionStepModel
Contains: foreignkey to a SynthesisProblemModel
Contains: pickled reactionstep
Contains: HTML representation
"""
class ReactionStepModel(models.Model):    
    problemModel = models.ForeignKey('SynthesisProblemModel')
    reactionStep = PickledObjectField()
    reactantBox = models.ForeignKey('MoleculeBoxModel')
    productBox = models.ForeignKey('MoleculeBoxModel')
    html = models.TextField()
    
    #Call ReactionStepModel.create(parentSynthesisProblemModel, reactionStepObject) to create a ReactionStepModel representing reactionStepObject
    #reactionStepObject is an instance of ReactionStep
    #parentSynthesisProblemModel is an instance of SynthesisProblemModel
    @classmethod
    def create(cls, parentSynthesisProblemModel, reactionStepObject):
        x = cls(reactionStep = reactionStepObject, problemModel = parentSynthesisProblemModel, html = reactionStepObject.stringList())
        return x

    

    
        
class mySignUpForm(UserCreationForm):
    #Just like the default user registration form, except with an email blank.
    #Hey look, one line of code!
    email = forms.EmailField()

    
###Can delete; this is me learning Django
class MoleculeForm(forms.Form):
    smiles = forms.CharField(max_length = 100)
class MoleculeModel(models.Model):
    smiles = models.CharField(max_length=100)    
    @classmethod
    def create(cls, s):
        x = cls(smiles = s)
        return x
        
    
    
class UserProfile(models.Model):
    #A user profile - saves all the important stuff about each user, including
    #reactions-in-progress, diagnostic stats, and default problem settings.
    #More to come.
    user = models.ForeignKey(User, unique=True)
    #savedProblem = models.ForeignKey(SynthesisProblemModel)

#Auto-make a UserProfile for each user when needed
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
    
    
    
    
