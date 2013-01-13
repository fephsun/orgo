from orgoStructure import *
import copy
import itertools

randThing = 0



#Returns a list of molecules.
def antiAdd(molecule, target1, target2, add1, add2,
            addtarget1 = None, addtarget2 = None):
    #Just a wrapper function, to make antiAdd less confusing.
    return synAdd(molecule, target1, target2, add1, add2,
                  addtarget1, addtarget2, True)

def duplicateInputs(molecule, target1, target2, add1, add2, addtarget1,
                    addtarget2):
    #Helper function for adds.  Returns a deep-copied version of all the inputs.
    target1Pos = molecule.atoms.index(target1)
    target2Pos = molecule.atoms.index(target2)
    if addtarget1 != None:
        addtarget1Pos = add1.atoms.index(addtarget1)
    if addtarget2 != None:
        addtarget2Pos = add2.atoms.index(addtarget2)

    Xmolecule = copy.deepcopy(molecule)
    #Remake pointers to targets
    Xtarget1 = Xmolecule.atoms[target1Pos]
    Xtarget2 = Xmolecule.atoms[target2Pos]
    Xadd1 = copy.deepcopy(add1)
    Xadd2 = copy.deepcopy(add2)
    if addtarget1 != None:
        Xaddtarget1 = Xadd1.atoms[addtarget1Pos]
    else:
        Xaddtarget1 = None
    if addtarget2 != None:
        Xaddtarget2 = Xadd2.atoms[addtarget2Pos]
    else:
        Xaddtarget2 = None
    return (Xmolecule, Xtarget1, Xtarget2, Xadd1, Xadd2, Xaddtarget1, Xaddtarget2)


#Returns a list of molecules.
def synAdd(molecule, target1, target2, add1, add2,
           addtarget1 = None, addtarget2 = None, antiAdd = False):
    #Destroys the double bond and CTstereochemistry between target1 and target2.
    #Adds add1 and add2 to target1 and target2.  If add1 and/or add2 are molecules,
    #addtargets are needed to specify where the bond should originate from add.

    #Also does anti-addition, if antiAdd is set to true.
    (molecule, target1, target2, add1, add2, addtarget1, addtarget2) =\
               duplicateInputs(molecule, target1, target2, add1, add2, addtarget1,
                               addtarget2)
    (Xmolecule, Xtarget1, Xtarget2, Xadd1, Xadd2, Xaddtarget1, Xaddtarget2) =\
               duplicateInputs(molecule, target1, target2, add1, add2, addtarget1,
                               addtarget2)

    #Set bond orders to single.
    target1.neighbors[target2] = 1
    target2.neighbors[target1] = 1
    Xtarget1.neighbors[Xtarget2] = 1
    Xtarget2.neighbors[Xtarget1] = 1

    if antiAdd:
        bigListOfStuff =\
        ((molecule, add1, target1, addtarget1, target2, target1.CTa, target1.CTb),
        (molecule, add2, target2, addtarget2, target1, target2.CTa, target2.CTb),
        (Xmolecule, Xadd1, Xtarget1, Xaddtarget1, Xtarget2, Xtarget1.CTb, Xtarget1.CTa),
        (Xmolecule, Xadd2, Xtarget2, Xaddtarget2, Xtarget1, Xtarget2.CTb, Xtarget2.CTa))
    else:
        bigListOfStuff =\
        ((molecule, add1, target1, addtarget1, target2, target1.CTb, target1.CTa),
        (molecule, add2, target2, addtarget2, target1, target2.CTa, target2.CTb),
        (Xmolecule, Xadd1, Xtarget1, Xaddtarget1, Xtarget2, Xtarget1.CTa, Xtarget1.CTb),
        (Xmolecule, Xadd2, Xtarget2, Xaddtarget2, Xtarget1, Xtarget2.CTb, Xtarget2.CTa))

    for thismolecule, thisAdd, thisTarget, thisAddTarget, otherTarget, ct1, ct2\
            in bigListOfStuff:
        if isinstance(thisAdd, Atom):
            thismolecule.addAtom(thisAdd, thisTarget, 1)
            if ct1 != None or ct2 != None:
                thisTarget.newChiralCenter(otherTarget,
                        (thisAdd, ct1, ct2))
        elif isinstance(thisAdd, Molecule):
            #Untested.
            thismolecule.addMolecule(thisAdd, thisAddTarget, thisTarget, 1)
            if ct1 != None or ct2 != None:
                thisTarget.newChiralCenter(otherTarget,
                        (thisAddTarget, ct1, ct2))
        else:
            #Hydrogens.
            if ct1 != None and ct2 != None:
                thisTarget.newChiralCenter(otherTarget,
                        (None, ct1, ct2))
        thisTarget.eliminateCT()
    if moleculeCompare(molecule, Xmolecule):
        return [molecule]
    else:
        return [molecule, Xmolecule]

def allAdd(molecule, target1, target2, add1, add2, addtarget1=None, addtarget2=None):
    #Adds add1 and add2 to target1 and target2, in both syn and anti fashions.
    #Does not introduce stereochemistry (this kind of addition never results in
    #stereochemistry).

    #Protect the inputs from modification:
    (molecule, target1, target2, add1, add2, addtarget1, addtarget2)=\
               duplicateInputs(molecule, target1, target2, add1, add2, addtarget1, addtarget2)
    #Reduce double bond
    molecule.changeBond(target1, target2, 1)
    target1.eliminateCT()
    target2.eliminateCT()
    #Add new stuff
    for thisTarget, thisAdd, thisAddtarget in (
        (target1, add1, addtarget1), (target2, add2, addtarget2)):
        if isinstance(thisAdd, Molecule):
            molecule.addMolecule(thisAdd, thisAddtarget, thisTarget, 1)
        elif isinstance(thisAdd, Atom):
            molecule.addAtom(thisAdd, thisTarget, 1)
        else:
            #Hydrogens.  Do nothing.
            pass
    return [molecule]
    

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
    if hasattr(a, "CTotherC") != hasattr(b, "CTotherC"):
        #One atom has a cis-trans center, where the other doesn't.  Obviously no pairings.
        return None
    if hasattr(a, "CTotherC"):
        CTFlag = True
    else:
        CTFlag = False
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
            #The following bit of code is still quite messy.  It tests whether the
            #hypothesized pairing follows the correct chirality.
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
        if CTFlag and OKFlag:
            #Makes sure that the hypothesized pairing follows the correct
            #cis-trans relationship
            if (a.CTa == None and b.CTa != None) or\
               (a.CTa != None and temp[a.CTa] != b.CTa) or\
               (a.CTb == None and b.CTb != None) or\
               (a.CTb != None and temp[a.CTb] != b.CTb):
                OKFlag = False

        if (temp not in out) and OKFlag:
            out.append(temp)
    return out

def shift(l, n):
    return l[n:] + l[:n]

def noOfAtoms(string):
    #Helper function.  Given a SMILES string, return the number of atoms.
    #Not used, as of Jan 11, 2013
    out = 0
    for char in string:
        if char.isupper():
            out += 1
    return out

def markovnikov(a, b):
    #a and b are two carbon atoms.  Function tuple of all possible markovnikov
    #orderings of carbons
    aTotal = 0
    bTotal = 0
    for atom in a.neighbors:
        if atom.element == "C":
            aTotal += 1
    for atom in b.neighbors:
        if atom.element == "C":
            bTotal += 1
    if aTotal == bTotal:
        return ((a,b),(b,a))
    elif aTotal > bTotal:
        return ((a, b))
    else:
        return ((b, a))


'''
#Finds candidate alkenes within a molecule.
#(define "alkenes" as "alkenes that are not in an aromatic ring")
#Returns a tuple of tuples of atoms. The lowest tuple is a pair of two atoms, which share a double bond.
#Make sure not to include duplicates.
def findAlkenes(molecule):
    #To track which bonds we've counted, we use the atom.flag property.
    #atom.flag starts at 0, and must be reset to 0 at the end.
    doubleBonds = []
    for atom in molecule.atoms:
        if not(atom.element == 'C'):
            continue
        for neighbor in atom.neighbors:
            if neighbor.element == 'C' and atom.neighbors[neighbor] == 2:
                if atom.flag != 0 and neighbor.flag != 0 and atom in neighbor.flag\
                   and neighbor in atom.flag:
                    #We've already counted this bond.  Move on.
                    continue
                if atom.flag == 0:
                    atom.flag = [neighbor]
                else:
                    atom.flag.append(neighbor)
                if neighbor.flag == 0:
                    neighbor.flag = [atom]
                else:
                    neighbor.flag.append(atom)
                doubleBonds.append((atom, neighbor))
    #Reset the flags - other functions like to use them, as well.
    for atom in molecule.atoms:
        atom.flag = 0
    return doubleBonds
'''


#Returns a tuple of atoms.
def findAlkenes(molecule):
    for atom in molecule.atoms:
        if not (atom.element == 'C'):
            continue
        for neighbor in atom.neighbors:
            if neighbor.element == 'C' and atom.neighbors[neighbor] == 2:
                return (atom, neighbor)
    return None

#Returns a tuple of atoms.
def findAlkynes(molecule):
    for atom in molecule.atoms:
        if not (atom.element == 'C'):
            continue
        for neighbor in atom.neighbors:
            if neighbor.element == 'C' and atom.neighbors[neighbor] == 3:
                return (atom, neighbor)
    return None






