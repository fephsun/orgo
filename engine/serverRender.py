#Jump through a bunch of hoops to import openbabel, which is in another folder.
import sys, os
openbabelDir = "/afs/athena.mit.edu/user/f/e/felixsun/openbabel/install/lib"
homeDir = os.getcwd()
os.chdir(openbabelDir)
sys.path.append(openbabelDir)
import openbabel, pybel
os.chdir(homeDir) 

#Set up input and output formats
obConversion = openbabel.OBConversion()
obConversion.SetInAndOutFormats("smi", "svg")

def render(smiles):
    outMol = openbabel.OBMol()
    obConversion.ReadString(outMol, smiles)
    return obConversion.WriteString(outMol)