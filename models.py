# standard import to get access to models.Model
from django.db import models
import orgo.engine.orgoStructure as orgoStructure
import cPickle
import django.forms as forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class moleculeField(models.Field):
    description = "A molecule."
    __metaclass__ = models.SubfieldBase
    
    def __init__ (self, *args, **kwargs):
        super(moleculeField, self).__init__(*args, **kwargs)
    
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


class moleculeListModel(models.Model):
    molecule = PickledObjectField()


class synthesisProblemModel(models.Model):
    synthesisProblem = PickledObjectField()
