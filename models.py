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

class synthesisProblem(models.Model):
    startingMol = moleculeField()
    
class UserForm(ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    #Hash the password.
    def save(self, commit=True):
        user = super(UserForm, self).save(commit = False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class LogInForm(ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']
    #Hash the password.
    def save(self, commit=True):
        user = super(UserForm, self).save(commit = False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user