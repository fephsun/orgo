#Jump through a bunch of hoops to import openbabel, which is in another folder.
import sys, os
openbabelDir = "/afs/athena.mit.edu/user/f/e/felixsun/openbabel/install/lib"
homeDir = os.getcwd()
os.chdir(openbabelDir)
sys.path.append(openbabelDir)
import openbabel, pybel
os.chdir(homeDir) 
import re

#Set up input and output formats
obConversion = openbabel.OBConversion()
obConversion.SetInAndOutFormats("smi", "svg")

def render(smiles):
    outMol = openbabel.OBMol()
    obConversion.ReadString(outMol, smiles)
    ans = obConversion.WriteString(outMol)
    
    #Make the svg background transparent
    #replace fill="rgb(255,255,255)" with fill-opacity="0"
    
    ans = re.sub("fill=\"white\"", "fill-opacity=\"0\"", ans)
    
    return ans