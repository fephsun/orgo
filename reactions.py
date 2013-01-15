from helperFunctions import *








def removeDuplicates(moleculeList):
    return moleculeList





def react(molecules, findPlace, reactAtPlace):
    if not isinstance(molecules, list):
        return react([molecules], findPlace, reactAtPlace)
    while True:
        places = [(molecule, findPlace(molecule)) for molecule in molecules]
        if not (False in [item[1]==None for item in places]):
            break
        for molecule, place in places:
            if place != None:
                molecules.remove(molecule)
                x = reactAtPlace(molecule, place)
                if not isinstance(x, list):
                    x = [x]
                molecules += x
    return removeDuplicates(molecules)
#TO DO: put something here to decrease the size of molecules if things are identical
#TO DO: make react deepcopy its input molecules?





"""Hydrogenation
Candidate reactants: alkenes, alkynes
H2 cat Pd|C in EtOH
Syn addition of an H to each atom in the alkene or alkyne. Go all the way to single bond."""
def hydrogenate(molecules):
    def reactAtPlace(molecule, place):
        if place[0].neighbors[place[1]] == 2:
            #Alkene
            return synAdd(molecule, place[0], place[1], None, None)
        else:
            #Alkyne
            return allTripleAdd(molecule, place[0], place[1], None, None)

    return react(molecules, findAlkeneAndAlkyne, reactAtPlace)



    


"""Hydrohalogenation
HX in CH2Cl2
Candidate reactants: alkenes, alkynes
Adds the X to the Markovnikov-most carbon, and the H to the other carbon. ***Neither syn nor anti*** (because carbocation intermediate).
**UNLESS the alkene is next to a carbonyl (i.e. Michael acceptor). In this case, the halogen is added anti-Markovnikov. We might want to allow users to use this 
reaction, but not allow it to be used when we generate random synthesis problems.
If reacting an alkyne:
if 1eqv specified --> add once
if 2eqv or if excess specified --> add twice
if no quantity specified --> don't let it be a valid reaction? Some sort of feedback to make user specify _how much_ when reacting with alkynes (which is a good habit 
to have) would be nice."""
#halogen is a string
def hydrohalogenate(molecules, halogen):
    def reactAtPlace(molecule, place): #returns a list of molecules post-reaction at place
        newMolecules = []
        atomicHalogen = Atom(halogen)
        mkvCarbons = markovnikov(place[0], place[1])
        for pairing in mkvCarbons:
            if place[0].neighbors[place[1]] == 2:
                #Double bond
                newMolecules += allAdd(molecule, pairing[0], pairing[1], Atom(halogen), None)
            else:
                #Triple bond
                newMolecules += allTripleAdd(molecule, pairing[0], pairing[1], Atom(halogen), None)
        #Sometimes, Mkv's rule results in two identical products.  Return only one of them.
        if moleculeCompare(newMolecules[0], newMolecules[1]):
            return newMolecules[0]
        else:
            return newMolecules
    return react(molecules, findAlkeneAndAlkyne, reactAtPlace)



"""Halogenation
Candidate reactants: alkenes, alkynes
X2 in CH2Cl2, dark
Anti addition of an X to each atom in the alkene.
if 1eqv specified --> add once
if 2eqv or if excess specified --> add twice
if no quantity specified --> don't let it be a valid reaction? Some sort of feedback to make user specify _how much_ when reacting with alkynes (which is a good habit to have) would be nice."""


#halogen is a string
def halogenate(molecules, halogen):
    def reactAtPlace(molecule, place):
        atomicHalogen = Atom(halogen)
        atomicHalogen2 = Atom(halogen)
        if place[0].neighbors[place[1]] == 2:
            #Double bond.
            return antiAdd(molecule, place[0], place[1], atomicHalogen, atomicHalogen2)
        else:
            return allTripleAdd(molecule, place[0], place[1], atomicHalogen, atomicHalogen2)
    return react(molecules, findAlkeneAndAlkyne, reactAtPlace)

def halogenate1eq(molecules, halogen):
    #Reacts one equivalent of X2 with a molecule containing one alkyne and no alkenes.  Will
    #not do anything (e.g. will return the input molecules) if there are multiple alkynes or any
    #alkenes.
    #Creates a trans alkene.
    def findPlace(molecule):
        if findAlkene(molecule) != None:
            return None
        if len(findAlkynes(molecule)) != 1:
            return None
        return findAlkyne(molecule)  
    def reactAtPlace(molecule, place):
        return tripleAdd(molecule, place[0], place[1], Atom(halogen), Atom(halogen), 'trans')
    return react(molecules, findPlace, reactAtPlace)

"""Free-radical hydrohalogenation
Candidate reactants: alkenes
HBr cat ROOR, hv or heat
Adds the X to the anti-Markovnikov-most carbon in the alkene, and the H to the other one. Neither syn nor anti."""

#halogen is a string
def radicalhydrohalogenate(molecules, halogen):
    def findPlace(molecule): #returns one place at which the molecule can react -- e.g. a tuple of atoms, for alkenes/alkynes
        return findAlkene(molecule)
    def reactAtPlace(molecule, place): #returns a list of molecules post-reaction at place
        newMolecules = []
        mkvCarbons = markovnikov(place[0], place[1])
        for pairing in mkvCarbons:
                newMolecules += allAdd(molecule, pairing[0], pairing[1], None, Atom(halogen))
        return newMolecules
    return react(molecules, findPlace, reactAtPlace)



"""
Epoxidation
Candidate reactants: alkenes
mCPBA or PhCO3H or RCO3H, in CH2Cl2
Converts alkene bond to an epoxide. Two possible stereochemical outcomes (up-epoxide or down-epoxide)
"""
def epoxidate(molecules):
    def epoxAdd(molecule, target1, target2, add1, add2):
        addtarget1 = None
        addtarget2 = None
        antiAdd = False
        #Also does anti-addition, if antiAdd is set to true.
        (molecule, target1, target2, add1, add2, addtarget1, addtarget2) =\
                   duplicateInputs(molecule, target1, target2, add1, add2, addtarget1,
                                   addtarget2)
        (Xmolecule, Xtarget1, Xtarget2, Xadd1, Xadd2, Xaddtarget1, Xaddtarget2) =\
                   duplicateInputs(molecule, target1, target2, add1, add2, addtarget1,
                                   addtarget2)
        add1 = add2
        Xadd1 = Xadd2

        #Set bond orders to single.
        target1.neighbors[target2] = 1
        target2.neighbors[target1] = 1
        Xtarget1.neighbors[Xtarget2] = 1
        Xtarget2.neighbors[Xtarget1] = 1

        bigListOfStuff =\
        ((molecule, add1, target1, addtarget1, target2, target1.CTb, target1.CTa),
        (molecule, add2, target2, addtarget2, target1, target2.CTa, target2.CTb),
        (Xmolecule, Xadd1, Xtarget1, Xaddtarget1, Xtarget2, Xtarget1.CTa, Xtarget1.CTb),
        (Xmolecule, Xadd2, Xtarget2, Xaddtarget2, Xtarget1, Xtarget2.CTb, Xtarget2.CTa))

        for thismolecule, thisAdd, thisTarget, thisAddTarget, otherTarget, ct1, ct2\
                in bigListOfStuff:
            try:
                thismolecule.addAtom(thisAdd, thisTarget, 1)
            except:
                thismolecule.addBond(thisAdd, thisTarget, 1)
            if ct1 != None or ct2 != None:
                thisTarget.newChiralCenter(otherTarget,
                        (thisAdd, ct1, ct2))
            thisTarget.eliminateCT()
        if moleculeCompare(molecule, Xmolecule):
            return [molecule]
        else:
            return [molecule, Xmolecule]
    def findPlace(molecule): #returns one place at which the molecule can react -- e.g. a tuple of atoms, for alkenes/alkynes
        return findAlkene(molecule)
    def reactAtPlace(molecule, place): #returns a list of molecules post-reaction at place
        oxygen = Atom("O")
        return epoxAdd(molecule, place[0], place[1], oxygen, oxygen)
    return react(molecules, findPlace, reactAtPlace)


"""
Hydration
Candidate reactants: alkenes
H2SO4 (or other acid) in ROH, where R can also be H
If alkene: Adds an OR to the Markovnikov carbon of the alkene, and an H to the anti-Markovnikov carbon. Neither syn nor anti, since carbocation.
If alkyne and H2O: Form a ketone or aldehyde, placing the O at the Markovnikov carbon.
If alkyne and ROH: form an enolate-ether, I think...     or form two ethers.

For alkynes to react, usually also mention "HgSO4 accels."
"""

#When there is an other-molecule:
    #If any incoming molecules can react with themselves, use that as the product.
    #Only if none of the molecules can react with themselves, react them against each other in all possible ways.
        #Afterwards, check the resulting molecule for self-reactivity.

def acidhydrate(molecules, others):

    def findPlaces1(molecule):
        return findAlkenesAndAlkynes(molecule)
    def findPlaces2(molecule):
        return findHydroxyls(molecule)

    #Place 1 is an alkene or an alkyne (tuple of atoms)
    #Place 2 is an oxygen connected to 1 or 0 neighbors
    def reactAtPlaces(molecule1, molecule2, place1, place2):
        
        #Use addMolecule(self, molecule, foreignTarget, selfTarget, bo)
        if place1[0].neighbors[place1[1]] == 2: #if is alkene:
            newMolecules = []
            mkvCarbons = markovnikov(place1[0], place1[1])
            for pairing in mkvCarbons:
                newMolecules += allAdd(molecule1, pairing[0], pairing[1], molecule2, None, place2, None)
            return newMolecules

        elif place1[0].neighbors[place1[1]] == 3: #if is alkyne:
            
            if len(list(place2.neighbors)) == 0: #if adding water:
                #Going to need to write a custom function here, borrowed from allTripleAdd.
                #Make the alkyne bond a single bond
                #Add a double-bond-O to the Markovnikov carbon
                #If each carbon is equally Markovnikov, do some duplication-hacks and add to both
                #Make a double bond between each Markovnikov carbon and the O of place2
                def carbonylAdd(molecule, target1, target2):
                    #Adds two copies of add1 and two copies of add2 to target1 and target2, respectively.
                    #Breaks a triple bond.  Introduces no new stereochemistry.
                    #MODIFICATION: Adds same copy of add1 to target1, instead producing a double bond.
                    #add1 is an oxygen atom:
                    add1 = Atom("O")
                    add2 = None
                    addtarget1 = None
                    addtarget2 = None

                    #Protect the inputs from modification:
                    (molecule, target1, target2, add1, add2, addtarget1, addtarget2)=\
                               duplicateInputs(molecule, target1, target2, add1, add2, addtarget1, addtarget2)
                    #We need an extra copy of add1 and add2, along with corresponding addtargets.
                    (notused, notused2, notused3, add1b, add2b, addtarget1b, addtarget2b)=\
                               duplicateInputs(molecule, target1, target2, add1, add2, addtarget1, addtarget2)
                    #Change to single bond
                    molecule.changeBond(target1, target2, 1)
                    #Add new stuff
                    molecule.addAtom(add1, target1, 2)
                    
                    return [molecule]
                
                newMolecules = []
                mkvCarbons = markovnikov(place1[0], place1[1])
                for pairing in mkvCarbons:
                    newMolecules += carbonylAdd(molecule1, pairing[0], pairing[1])
                return newMolecules

                
            elif len(list(place2.neighbors)) == 1: #if is alcohol:
                #Use allTripleAdd(molecule, target1, target2, add1, add2, addtarget1 = None, addtarget2 = None)

                #form an enol ether?
                #Make the alkyne bond a double bond
                #Add a single-bond connecting the Markovnikov carbon to the alcohol
                
                newMolecules = []
                mkvCarbons = markovnikov(place1[0], place1[1])
                for pairing in mkvCarbons:
                    print (pairing[0] in molecule1.atoms)
                    newMolecules += allTripleAdd(molecule1, pairing[0], pairing[1], molecule2, None, place2, None, )
                return newMolecules
        else:
            print "Error: findAlkenes, findAlkynes returning non-alkene and/or non-alkyne"
            raise StandardError

        
        
        
    return twoReact(copy.deepcopy(molecules), copy.deepcopy(others), findPlaces1, findPlaces2, reactAtPlaces)


#NOTE: findPlaces methods passed into this method MUST return lists
def twoReact(molecules, others, findPlaces1, findPlaces2, reactAtPlaces):
    if not isinstance(molecules, list):
        return twoReact([molecules], others, findPlaces1, findPlaces2, reactAtPlaces)
    if not isinstance(others, list):
        return twoReact(molecules, [others], findPlaces1, findPlaces2, reactAtPlaces)
    output = []
    molecules1 = [] #molecules which are capable of playing role 1
    molecules2 = [] #molecules which are capable of playing role 2
    for molecule in molecules+others:
        candidates1 = [x for x in findPlaces1(molecule) if x != None] #places in molecule which can react as role 1
        candidates2 = [x for x in findPlaces2(molecule) if x != None] #places in molecule which can react as role 2
        if len(candidates1) != 0:
            if len(candidates2) != 0:
                #self-react and add to list
                output += [item for sublist in [
                    reactAtPlaces(molecule, molecule, locus1, locus2)
                        for locus1 in findPlaces1(molecule)
                        for locus2 in findPlaces2(molecule)
                    ]
                    for item in sublist]

        if len(candidates1) != 0:
            molecules1 += [molecule]

        if len(candidates2) != 0:
            molecules2 += [molecule]

    #If this is true, then no molecule reacted with itself. You may proceed to reacting the molecules in molecules1 and molecules2 with each other.
    if len(output) == 0:
        output = [item for sublist in [reactAtPlaces(molecule1, molecule2, locus1, locus2) for molecule1 in molecules1 for molecule2 in molecules2 for locus1 in findPlaces1(molecule1) for locus2 in findPlaces2(molecule2)] for item in sublist]

    return removeDuplicates(output)


        
'''def react(molecules, findPlace, reactAtPlace):
    if not isinstance(molecules, list):
        return react([molecules], findPlace, reactAtPlace)
    while True:
        places = [(molecule, findPlace(molecule)) for molecule in molecules]
        if not (False in [item[1]==None for item in places]):
            break
        for molecule, place in places:
            if place != None:
                molecules.remove(molecule)
                x = reactAtPlace(molecule, place)
                if not isinstance(x, list):
                    x = [x]
                molecules += x
    return molecules'''


"""
Halohydration
Candidate reactants: alkenes
X2 in ROH, where R can also be H
Adds an OR to the Markovnikov carbon of the alkene, and an X to the anti-Markovnikov carbon. Anti.
"""



"""
Hydroboration
Candidate reactants: alkenes, alkynes
BH3 in THF, then NaOH and H2O2
If alkene: Adds an OH to the anti-Markovnikov carbon, then adds an H to the other one. Syn addition.
If alkyne: Form a ketone or aldehyde, placing the O at the anti-Markovnikov carbon.
"""
#TO DO: Implement with alkynes
def hydroborate(molecules):
    def findPlace(molecule): #returns one place at which the molecule can react -- e.g. a tuple of atoms, for alkenes/alkynes
        return findAlkene(molecule)
    def reactAtPlace(molecule, place): #returns a list of molecules post-reaction at place
        newMolecules = []
        mkvCarbons = markovnikov(place[0], place[1])
        for pairing in mkvCarbons:
            oxy = Atom("O")
            newMolecules += synAdd(molecule, pairing[0], pairing[1], None, oxy)
        return newMolecules
    return react(molecules, findPlace, reactAtPlace)



"""
Dihydroxylation (Upjohn dihydroxylation)
Candidate reactants: alkenes
cat. OsO4 in NMO and acetone or H2O
Syn addition of two OH groups to each carbon.
"""
def dihydroxylate(molecules):
    def findPlace(molecule):
        return findAlkene(molecule)
    def reactAtPlace(molecule, place):
        return synAdd(molecule, place[0], place[1], Atom("O"), Atom("O"))
    return react(molecules, findPlace, reactAtPlace)



"""
Ozonolysis
Candidate reactants: alkenes
O3 in CH2Cl2, with Me2S or Zn
Adds two oxygens, splitting alkene bond, producing carbonyls.
"""
def ozonolyse(molecules):
    def findPlace(molecule):
        return findAlkene(molecule)
    def reactAtPlace(molecule, place):
        #Break the double bond
        molecule.changeBond(place[0], place[1], 0)
        #Add two double bonds to two new oxygens
        molecule.addAtom(Atom("O"), place[0], 2)
        molecule.addAtom(Atom("O"), place[1], 2)
        #Destroy CT stereochemistry
        place[0].eliminateCT()
        place[1].eliminateCT()
        #Splice the molecule
        return splice(molecule)
    return react(copy.deepcopy(molecules), findPlace, reactAtPlace)




"""
Lindlar reduction
Candidate reactants: alkynes
H2, cat. Lindlar
Produces the cis alkene from an alkyne. Adds two Hs.
"""
def lindlar(molecules):
    def findPlace(molecule):
        return findAlkyne(molecule)
    def reactAtPlace(molecule, place):
        tripleAdd(molecule, place[0], place[1], None, None, 'cis')
    return react(molecules, findPlace, reactAtPlace)



"""
Sodium-ammonia reduction
Candidate reactants: alkynes
Na, in NH3 (L)
Produces the trans alkene from an alkyne. Adds two Hs.
"""
def sodiumAmmonia(molecules):
    def findPlace(molecule):
        return findAlkyne(molecule)
    def reactAtPlace(molecule, place):
        tripleAdd(molecule, place[0], place[1], None, None, 'trans')
    return react(molecules, findPlace, reactAtPlace)




"""
Alkyne deprotonation to acetylide
Candidate reactants: alkynes, in which one end is an H
NaNH2 in NH3
Produces an acetylide ion. Removes the H+, resulting in a negative charge.
"""

















#Makes     C-C-C<C
#          |   |
#        O-C=C-N

#Makes     C-C-C>C
#          |   |
#        O-C=C-N
c1 = Atom("C")
mol = Molecule(c1)
c2 = Atom("C")
n1 = Atom("N")
mol.addAtom(c2, c1, 2)
mol.addAtom(n1, c2, 1)
o1 = Atom("O")
mol.addAtom(o1, c1, 1)

c3 = Atom("C")
mol.addAtom(c3, n1, 1)
c4 = Atom("C")
c5 = Atom("C")
mol.addAtom(c4, c3, 1)
mol.addAtom(c5, c3, 1)
c6 = Atom("C")
mol.addAtom(c6, c5, 1)
mol.addBond(c6, c1, 1)
c3.newChiralCenter(n1, (c4, None, c5))
c1.newCTCenter(c2, o1, c6)
c2.newCTCenter(c1, n1, None)



#Makes C\   /Cl
#        C=C
#     Cl/   \Br
c10 = Atom("C")
CTmol = Molecule(c10)
c11 = Atom("C")
CTmol.addAtom(c11, c10, 2)
c12 = Atom("C")
CTmol.addAtom(c12, c10, 1)
cL1 = Atom("Cl")
CTmol.addAtom(cL1, c10, 1)
cL2 = Atom("Cl")
CTmol.addAtom(cL2, c11, 1)
br10 = Atom("Br")
CTmol.addAtom(br10, c11, 1)
c10.newCTCenter(c11, cL1, c12)
c11.newCTCenter(c10, cL2, br10)

#Makes C\   /Br
#        C=C
#     C1/   \Cl
c15 = Atom("C")
CTmol2 = Molecule(c15)
c16 = Atom("C")
CTmol2.addAtom(c16, c15, 2)
c17 = Atom("C")
CTmol2.addAtom(c17, c15, 1)
cL5 = Atom("Cl")
CTmol2.addAtom(cL5, c15, 1)
cL6 = Atom("Cl")
CTmol2.addAtom(cL6, c16, 1)
br15 = Atom("Br")
CTmol2.addAtom(br15, c16, 1)
c15.newCTCenter(c16, cL5, c17)
c16.newCTCenter(c15, br15, cL6)

#Makes  C\ /C-C
#         C
#      Br/ \H
c20 = Atom("C")
chiralMol1 = Molecule(c20)
c23 = Atom("C")
chiralMol1.addAtom(c23, c20, 1)
br20 = Atom("Br")
chiralMol1.addAtom(br20, c20, 1)
c21 = Atom("C")
chiralMol1.addAtom(c21, c20, 1)
c22 = Atom("C")
chiralMol1.addAtom(c22, c21, 1)
c20.newChiralCenter(c21, (None, br20, c23))

c30 = Atom("C")
chiralMol2 = Molecule(c30)
c33 = Atom("C")
chiralMol2.addAtom(c33, c30, 1)
br30 = Atom("Br")
chiralMol2.addAtom(br30, c30, 1)
c31 = Atom("C")
chiralMol2.addAtom(c31, c30, 1)
c32 = Atom("C")
chiralMol2.addAtom(c32, c31, 1)
c30.newChiralCenter(c31, (None, c33, br30))

#Makes C/C=C/C
c40 = Atom("C")
c41 = Atom("C")
mol4 = Molecule(c40)
mol4.addAtom(c41, c40, 2)
c42 = Atom("C")
c43 = Atom("C")
mol4.addAtom(c42, c40, 1)
mol4.addAtom(c43, c41, 1)
c40.newCTCenter(c41, c42, None)
c41.newCTCenter(c40, c43, None)

#Makes C\C=C\C
c45 = Atom("C")
c46 = Atom("C")
mol4alt = Molecule(c45)
mol4alt.addAtom(c46, c45, 2)
c47 = Atom("C")
c48 = Atom("C")
mol4alt.addAtom(c47, c45, 1)
mol4alt.addAtom(c48, c46, 1)
c45.newCTCenter(c46, None, c47)
c46.newCTCenter(c45, None, c48)

#        c50
#Makes C-C<Cl
#     /   \
#   C<C   C>Br c51
#      \C/
c50 = Atom("C")
c51 = Atom("C")
c52 = Atom("C")
c53 = Atom("C")
c54 = Atom("C")
cycPentMol = Molecule(c50)
cycPentMol.addAtom(c51, c50, 1)
cycPentMol.addAtom(c52, c51, 1)
cycPentMol.addAtom(c53, c52, 1)
cycPentMol.addAtom(c54, c53, 1)
cycPentMol.addBond(c54, c50, 1)
cl50 = Atom("Cl")
cycPentMol.addAtom(cl50, c50, 1)
c50.newChiralCenter(c54, (cl50, c51, None))
br50 = Atom("Br")
cycPentMol.addAtom(br50, c51, 1)
c51.newChiralCenter(c50, (c52, br50, None))
c55 = Atom("C")
cycPentMol.addAtom(c55, c53, 1)
c53.newChiralCenter(c52, (c55, None, c54))

#Makes C-C#C-C
c60 = Atom("C")
c61 = Atom("C")
c62 = Atom("C")
c63 = Atom("C")
propyne = Molecule(c60)
propyne.addAtom(c61, c60, 3)
propyne.addAtom(c62, c61, 1)
propyne.addAtom(c63, c60, 1)

#Makes C-C-OH, ethanol
c64 = Atom("C")
c65 = Atom("C")
o66 = Atom("O")
ethanol = Molecule(c64)
ethanol.addAtom(c65, c64, 1)
ethanol.addAtom(o66, c64, 1)






