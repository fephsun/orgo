# Create your views here.
from django.shortcuts import render
import orgo.engine.serverRender as serverRender
import orgo.engine.reactions as reactions

def home(request):
    #Home page.
    outSmiles = reactions.smiles(reactions.mol)
    svg = serverRender.render(outSmiles)
    return render(request, 'index.html', {'molecule': svg})