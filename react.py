from orgoStructure import *
import os

def hydrogenate(molecule):
    for carbon in molecule.atoms:
        if carbon.element != 'C':
            continue
        for neighbor in carbon.neighbors:
            if neighbor.element == 'C' and carbon.neighbors[neighbor] == 2:
                synAdd(molecule, carbon, neighbor, None, None)
    return molecule

def synAdd(molecule, target1, target2, add1, add2, addtarget1 = None, addtarget2 = None):
    #Destroys the double bond and CTstereochemistry between target1 and target2.
    #Adds add1 and add2 to target1 and target2.  If add1 and/or add2 are molecules,
    #addtargets are needed to specify where the bond should originate from add.

    #Set bond orders to single.
    target1.neighbors[target2] = 1
    target2.neighbors[target1] = 1

    for thisAdd, thisTarget, thisAddTarget, otherTarget, ct1, ct2\
            in ((add1, target1, addtarget1, target2, target1.CTb, target1.CTa),
                (add2, target2, addtarget2, target1, target2.CTa, target2.CTb)):
        if isinstance(thisAdd, Atom):
            molecule.addAtom(thisAdd, thisTarget, 1)
            if ct1 != None or ct2 != None:
                thisTarget.newChiralCenter(otherTarget,
                        (thisAdd, ct1, ct2))
        elif isinstance(thisAdd, Molecule):
            #Untested.
            molecule.addMolecule(thisAdd, thisAddTarget, thisTarget, 1)
            if ct1 != None or ct2 != None:
                thisTarget.newChiralCenter(otherTarget,
                        (thisAddTarget, ct1, ct2))
        else:
            #Hydrogens.
            if ct1 != None and ct2 != None:
                thisTarget.newChiralCenter(otherTarget,
                        (None, ct1, ct2))
        thisTarget.eliminateCT()

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
        
mol2 = hydrogenate(mol)
print smiles(mol2)
