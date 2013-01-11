from orgoStructure import *
import os
import copy
import itertools

randThing = 0

def hydrogenate(molecule):
    #H2/PdC catalyst reaction for double bonds only, for now.  Syn addition.
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
    #Insert flags onto atoms, so we can find them after deepcopy.
    target1.targetFlag = 1
    target2.targetFlag = 2
    if addtarget1 != None:
        addtarget1.atFlag = 1
    if addtarget2 != None:
        addtarget2.atFlag = 2

    #deepcopy to make 2 cases: top addition or bottom addition
    Xmolecule = copy.deepcopy(molecule)
    for atom in Xmolecule.atoms:
        if hasattr(atom, "targetFlag"):
            if atom.targetFlag == 1:
                Xtarget1 = atom
            elif atom.targetFlag == 2:
                Xtarget2 = atom
    Xadd1 = copy.deepcopy(add1)
    Xadd2 = copy.deepcopy(add2)
    if addtarget1 != None:
        for atom in Xadd1.atoms:
            if hasattr(atom, "atFlag"):
                Xaddtarget1 = atom
    else:
        Xaddtarget1 = None
    if addtarget2 != None:
        for atom in Xadd2.atoms:
            if hasattr(atom, "atFlag"):
                Xaddtarget2 = atom
    else:
        Xaddtarget2 = None

    #Add the add's to both targets, following chirality.  Sorry for the copy-paste.
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

    for thisAdd, thisTarget, thisAddTarget, otherTarget, ct1, ct2\
            in ((Xadd1, Xtarget1, Xaddtarget1, Xtarget2, Xtarget1.CTb, Xtarget1.CTa),
                (Xadd2, Xtarget2, Xaddtarget2, Xtarget1, Xtarget2.CTa, Xtarget2.CTb)):
        if isinstance(thisAdd, Atom):
            Xmolecule.addAtom(thisAdd, thisTarget, 1)
            if ct1 != None or ct2 != None:
                thisTarget.newChiralCenter(otherTarget,
                        (thisAdd, ct2, ct1))
        elif isinstance(thisAdd, Molecule):
            #Untested.
            Xmolecule.addMolecule(thisAdd, thisAddTarget, thisTarget, 1)
            if ct1 != None or ct2 != None:
                thisTarget.newChiralCenter(otherTarget,
                        (thisAddTarget, ct2, ct1))
        else:
            #Hydrogens.
            if ct1 != None and ct2 != None:
                thisTarget.newChiralCenter(otherTarget,
                        (None, ct2, ct1))
        thisTarget.eliminateCT()

    #If molecule and Xmolecule are the same, we only need to return one product.
    if moleculeCompare(molecule, Xmolecule):
        return molecule
    else:
        return [molecule, Xmolecule]

def moleculeCompare(a, b, compareDict = None, expanded = []):
    #Determines whether two molecules are isomorphic.  In the worst case
    #(two molecules with the same atoms), this procedure does not run in
    #polynomial time, so be careful.
    for ele in ['C','N','O']:
        if a.countElement(ele) != b.countElement(ele):
            return False
    #sa = smiles(a)
    #sb = smiles(b)

    #compareDict maps atoms in a to their hypothesized counterparts in b.

    if len(expanded) == len(a.atoms):
        #We've reached every atom.  Call it equal.
        return True
        pass

    if compareDict == None:
        for atom in b.atoms:
            if atom.element == a.atoms[randThing].element:
                newCompareDicts = neighborCompare(a.atoms[randThing], atom, dict())
                if newCompareDicts == None:
                    continue
                for newCompareDict in newCompareDicts:
                    if moleculeCompare(a, b, newCompareDict, [a.atoms[randThing]]):
                        return True
        return False

    for aAtom in compareDict:
        if aAtom in expanded:
            #Already expanded this atom.  Don't do it again.
            continue
        newDictSectors = neighborCompare(aAtom, compareDict[aAtom], compareDict)
        if newDictSectors == None:
            return False
        for newDictSector in newDictSectors:
            if moleculeCompare(a, b, dict(compareDict.items() + newDictSector.items()),
                               expanded + [aAtom]):
                return True
        return False
            
def neighborCompare(a,b, compareDict):
    #Helper function.  Given 2 atoms, returns all pairings of neighbors of a
    #with neighbors of b such that each pair has the same element.
    aN = []
    bN = []
    for aNeighbor in a.neighbors:
        aN.append(aNeighbor.element)
    for bNeighbor in b.neighbors:
        bN.append(bNeighbor.element)
    #If the elements don't match, obviously there are no pairings.
    if sorted(aN) != sorted(bN):
        return None
    if hasattr(a, "chiralA") != hasattr(b, "chiralA"):
        #One atom has chirality, where the other doesn't.  Obviously no pairings.
        return None
    if hasattr(a, "chiralA"):
        chiralFlag = True
    else:
        chiralFlag = False
    #Generate all n! pairings, and prune as we go.
    out = []
    for aNeighborSet in itertools.permutations(a.neighbors):
        temp = dict()
        OKFlag = True
        for i in xrange(len(aNeighborSet)):
            if aNeighborSet[i].element != b.neighbors.keys()[i].element:
                #Oops, the elements don't actually match.  Skip.
                OKFlag = False
                break
            if a.neighbors[aNeighborSet[i]] != b.neighbors[b.neighbors.keys()[i]]:
                #Oops, the bond orders are different.  Skip.
                OKFlag = False
                break
            if aNeighborSet[i] in compareDict and \
               b.neighbors.keys()[i] != compareDict[aNeighborSet[i]]:
                #This pairing goes against what's already in compareDict.  Skip.
                OKFlag = False
                break
            temp[aNeighborSet[i]] = b.neighbors.keys()[i]
        if chiralFlag and OKFlag:
            aCW = []
            bCW = []
            for neighbor in a.chiralCWlist(aNeighborSet[randThing]):
                if neighbor == None:
                    #Hydrogen.
                    aCW.append("H")
                else:
                    aCW.append(neighbor.element)
            for neighbor in b.chiralCWlist(b.neighbors.keys()[randThing]):
                if neighbor == None:
                    #Hydrogen.
                    bCW.append("H")
                else:
                    bCW.append(neighbor.element)
            OKFlag = False
            for i in xrange(3):
                if aCW == shift(bCW, i):
                    OKFlag = True
                    for j in xrange(3):
                        if a.chiralCWlist(aNeighborSet[randThing])[j] == None:
                            continue
                        if temp[a.chiralCWlist(aNeighborSet[randThing])[j]] ==\
                            b.chiralCWlist(b.neighbors.keys()[randThing])[(j+i)%3]:
                            pass
                        else:
                            OKFlag = False

        if (temp not in out) and OKFlag:
            out.append(temp)
    return out

def shift(l, n):
    return l[n:] + l[:n]

def noOfAtoms(string):
    #Helper function.  Given a SMILES string, return the number of atoms.
    out = 0
    for char in string:
        if char.isupper():
            out += 1
    return out

#Finds candidate alkenes within a molecule.
#(define "alkenes" as "alkenes that are not Michael alpha-beta alkenes next to carbonyls, and are not in an aromatic ring")
def findAlkenes(molecule):



print smiles(mol)
print "================"
print smiles(CTmol)
print "----------------"
mol2 = hydrogenate(CTmol)
print smiles(mol2)
mol2 = copy.deepcopy(mol)
c3.newChiralCenter(n1, (None, c4, c5))
