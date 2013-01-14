from helperFunctions import *





#abstract
def genericReaction(molecules):
    def findPlace(molecule): #returns one place at which the molecule can react -- e.g. a tuple of atoms, for alkenes/alkynes
        return None
    def reactAtPlace(molecule, place): #returns a list of molecules post-reaction at place
        return None
    return react(molecules, findPlace, reactAtPlace)






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
    return molecules
#TO DO: put something here to decrease the size of molecules if things are identical
#TO DO: make react deepcopy its input molecules?






"""Hydrogenation
Candidate reactants: alkenes, alkynes
H2 cat Pd|C in EtOH
Syn addition of an H to each atom in the alkene or alkyne. Go all the way to single bond."""

#TO DO: implement alkynes

def hydrogenate(molecules):
    def findPlace(molecule):
        x = findAlkenes(molecule)
        if x == None:
            return findAlkynes(molecule)
        else:
            return x

    def reactAtPlace(molecule, place):
        if place[0].neighbors[place[1]] == 2:
            #Alkene
            return synAdd(molecule, place[0], place[1], None, None)
        else:
            #Alkyne
            return 

    return react(molecules, findPlace, reactAtPlace)



    


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

#TO DO: implement alkynes

#halogen is a string
def hydrohalogenate(molecules, halogen):
    def findPlace(molecule): #returns one place at which the molecule can react -- e.g. a tuple of atoms, for alkenes/alkynes
        a = findAlkenes(molecule)
        return a
    def reactAtPlace(molecule, place): #returns a list of molecules post-reaction at place
        newMolecules = []
        mkvCarbons = markovnikov(place[0], place[1])
        for pairing in mkvCarbons:
                newMolecules += allAdd(molecule, pairing[0], pairing[1], Atom(halogen), None)
        return newMolecules
    return react(molecules, findPlace, reactAtPlace)




"""Halogenation
Candidate reactants: alkenes, alkynes
X2 in CH2Cl2, dark
Anti addition of an X to each atom in the alkene.
if 1eqv specified --> add once
if 2eqv or if excess specified --> add twice
if no quantity specified --> don't let it be a valid reaction? Some sort of feedback to make user specify _how much_ when reacting with alkynes (which is a good habit to have) would be nice."""

#TO DO: implement alkynes

#halogen is a string
def halogenate(molecules, halogen):
    def findPlace(molecule):
        return findAlkenes(molecule)
    def reactAtPlace(molecule, place):
        atomicHalogen = Atom(halogen)
        atomicHalogen2 = Atom(halogen)
        return antiAdd(molecule, place[0], place[1], atomicHalogen, atomicHalogen2)
    return react(molecules, findPlace, reactAtPlace)





"""Free-radical hydrohalogenation
Candidate reactants: alkenes
HBr cat ROOR, hv or heat
Adds the X to the anti-Markovnikov-most carbon in the alkene, and the H to the other one. Neither syn nor anti."""

#halogen is a string
def radicalhydrohalogenate(molecules, halogen):
    def findPlace(molecule): #returns one place at which the molecule can react -- e.g. a tuple of atoms, for alkenes/alkynes
        return findAlkenes(molecule)
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
        return findAlkenes(molecule)
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
If alkyne and ROH: I'm not sure. Forms some strange enolate-ester? Possibly best to leave this out?
"""
#TO DO: add alkyne functionality

#When there is an other-molecule:
    #Check both the current molecule and the other-molecule for alkenes and hydroxyls.
    #If the molecule can react with itself, make that the product.
    #If the other can react with itself, add that as another product.
    #Only if none of the above can occur, react them against each other.
        #Afterwards, check the resulting molecule for self-reactivity.

def acidhydrate(molecules, other):
    
    def findPlace(molecule): #returns one place at which the molecule can react -- e.g. a tuple of atoms, for alkenes/alkynes
        return findAlkenes(molecule)
    def reactAtPlace(molecule, place): #returns a list of molecules post-reaction at place
        newMolecules = []
        mkvCarbons = markovnikov(place[0], place[1])
        for pairing in mkvCarbons:
                newMolecules += allAdd(molecule, pairing[0], pairing[1], )
        return newMolecules
    return react(molecules, findPlace, reactAtPlace)

def twoReact



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
        return findAlkenes(molecule)
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
        return findAlkenes(molecule)
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
        return findAlkenes(molecule)
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
        return findAlkynes(molecule)
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
        return findAlkynes(molecule)
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


