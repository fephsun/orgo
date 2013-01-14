from helperFunctions import *
import random

def randomStart():
    lastAtom = Atom("C")
    frontAtom = lastAtom
    mol = Molecule(lastAtom)
    while random.random() < 0.9 or len(mol.atoms) < 5:
        switcher = random.random()
        if switcher < 1:
            newMol, thisAtom, nextAtom = randC()
##        elif switcher < 0.75:
##            newMol, thisAtom, nextAtom = randRing(5)
##        else:
##            newMol, thisAtom, nextAtom = randRing(6)

        switcher = random.random()
        if switcher < 0.5 and len(thisAtom.neighbors) == 0\
           and lastAtom.totalBondOrder() == 1:
            #Make a triple bond.
            mol.addMolecule(newMol, thisAtom, lastAtom, 3)
        elif switcher < 0.4 and len(thisAtom.neighbors) <= 1\
             and lastAtom.totalBondOrder() <= 2\
             and lastAtom.findAlkeneBond() == None:
            #Make a double bond.  Watch out for cis/trans.
            #Each double bond must have a cis/trans specification.
            mol.addMolecule(newMol, thisAtom, lastAtom, 2)
            otherNeighbors = []
            for neighbor in lastAtom.neighbors:
                if neighbor != thisAtom:
                    otherNeighbors.append(neighbor)
            if len(otherNeighbors) == 1:
                lastAtom.newCTCenter(thisAtom, otherNeighbors[0],
                                     None)
            else:
                lastAtom.newCTCenter(thisAtom, otherNeighbors[0],
                                     otherNeighbors[1])
            #Will make other half of cis/trans later
        else:
            #Make single bond
            mol.addMolecule(newMol, thisAtom, lastAtom, 1)
        fixStereo(mol, thisAtom, lastAtom)
        lastAtom = thisAtom
        thisAtom = nextAtom
    #Not quite done yet.  We need to fix stereochemistry on the last atom.
    fixStereo(mol, None, lastAtom) #May be a slight problem with chirality?
    return mol, frontAtom, None

def randC():
    #Makes a random carbon atom with some substituents
    c = Atom("C")
    mol = Molecule(c)
    #Add up to 2 substituents
    for i in xrange(2):
        switcher = random.random()
        if switcher < 0.2:
            newS = Atom("Cl")
            mol.addAtom(newS, c, 1)
        elif switcher < 0.4:
            newS = Atom("Br")
            mol.addAtom(newS, c, 1)            
        elif switcher < 0.3:
            print "Branching"
            newS, frontAtom, notused = randomStart()
            mol.addMolecule(newS, frontAtom, c, 1)
    return mol, c, c

def randRing(noCs):
    pass

def fixStereo(mol, thisAtom, lastAtom):
    #Look to see if the *last* piece we added requires stereochem
    otherC = lastAtom.findAlkeneBond()
    if otherC != None:
        #Find the last neighbor of lastAtom (other than thisAtom
        #and otherC).  None means Hydrogen.
        otherN = None
        for neighbor in lastAtom.neighbors:
            if neighbor != otherC and neighbor != thisAtom:
                otherN = neighbor
        #Do a coin flip to determine cis or trans.
        if random.random() < 0.5:
            lastAtom.newCTCenter(otherC, otherN, thisAtom)
        else:
            lastAtom.newCTCenter(otherC, thisAtom, otherN)
    if probablyChiral(lastAtom):
        tempN = []
        for neighbor in lastAtom.neighbors:
            if neighbor != thisAtom:
                tempN.append(neighbor)
        if len(tempN) == 2:
            tempN.append(None)
        #Do a coin flip to determine chirality.
        if random.random() < 0.5:
            lastAtom.newChiralCenter(thisAtom, (tempN[0],
                        tempN[1], tempN[2]))
        else:
            lastAtom.newChiralCenter(thisAtom, (tempN[0],
                        tempN[2], tempN[1]))
        
        
            

def probablyChiral(atom):
    #A rather bootleg heruistic for determining whether an atom
    #may need a chiral center.
    if len(atom.neighbors) <= 2:
        return False
    carbonCount = 0
    elementList = []
    for neighbor in atom.neighbors:
        if neighbor.element == 'C':
            carbonCount += 1
        if neighbor.element not in elementList:
            elementList.append(neighbor.element)
    if carbonCount >= 2 or len(elementList) >= 3:
        return True
    else:
        return False


    


