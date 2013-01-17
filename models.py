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
SynthesisProblemModel
Contains: pickled list of molecule-models by unique ID
Contains: pickled list of reagent-models by unique ID
Contains: pickled list of reaction-step-models by unique ID
Contains: pickled synthesis problem solution
"""
class SynthesisProblemModel(models.Model):
    moleculeModels = PickledObjectField()
    reagentModels = PickledObjectField()

    

"""
MoleculeBoxModel
Contains: foreignkey to a SynthesisProblemModel
Contains: pickled moleculebox
Contains: SVG representation
"""


"""
ReagentModel
Contains: foreignkey to a SynthesisProblemModel
Contains: pickled reagentbox
Contains: its own HTML representation
"""


"""
ReactionStepModel
Contains: foreignkey to a SynthesisProblemModel
Contains: pickled reactionstep
Contains: HTML representation
"""
#class ReactionStepModel(models.Model):
    

        
        
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
    
    
    
    
