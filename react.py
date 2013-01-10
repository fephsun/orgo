from orgoStructure import *
import os

def hydrogenate(molecule):
    for carbon in molecule.atoms:
        if carbon.element != 'C':
            continue
        for neighbor in carbon.neighbors:
            if neighbor.element == 'C' and carbon.neighbors[neighbor] == 2:
                #Set bond orders
                carbon.neighbors[neighbor] = 1
                neighbor.neighbors[carbon] = 1
                if carbon.CTb != None and carbon.CTa != None:
                    carbon.newChiralCenter(neighbor, (None, carbon.CTb, carbon.CTa))
                if neighbor.CTb != None and neighbor.CTa != None:
                    neighbor.newChiralCenter(carbon, (None, neighbor.CTa, neighbor.CTb))
                carbon.eliminateCT()
                neighbor.eliminateCT()
    return molecule

def moleculeCompare(a, b):
    #Determines whether two molecules are isomorphic.  In the worst case
    #(two molecules with the same atoms), this procedure does not run in
    #polynomial time, so be careful.
    for ele in ['C','N','O']:
        if a.countElement(ele) != b.countElement(ele):
            return False
    sa = smiles(a)
    sb = smiles(b)
    #Call the SMSD program, which does molecular comparison
    os.system('java -Xms500M -Xmx512M -cp SMSD20120718.jar cmd.SMSDcmd -Q SMI -q "'
              +sa+'" -T SMI -t "'+sb+'" -O SMI -o temp.txt')
    similarSMI = open("temp.txt", "r")
    if noOfAtoms(sa) == noOfAtoms(similarSMI.read()) and noOfAtoms(sa) == noOfAtoms(sb):
        return True
    else:
        return False

def noOfAtoms(string):
    #Helper function.  Given a SMILES string, return the number of atoms.
    out = 0
    for char in string:
        if char.isupper():
            out += 1
    return out
        
mol2 = hydrogenate(CTmol)
print smiles(mol2)
