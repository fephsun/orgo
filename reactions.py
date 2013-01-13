from helperFunctions import *


#abstract
def reactAtPlace(molecule, place):
    #react molecule using data provided by place
    #return a list of molecules
    pass

#abstract
def findPlace(molecule):
    #return some sort of data that can be used by its partner reactAtPlace method
    #if no such place exists, return None
    pass



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
                molecules += reactAtPlace(molecule, place)
    return molecules


'''def hydrogenate(molecules):
    #H2/PdC catalyst reaction for double bonds only, for now.  Syn addition.
    while True:
        alkenes = [findAlkenes(molecule) for molecule in molecules]
        #The line below flattens a nested list, I swear.  Just don't ask how
        #it works.  -FS
        flatAlkenes = [item for sublist in alkenes for item in sublist]
        if len(flatAlkenes) == 0:
            break
        alkenes = [(molecule,findAlkenes(molecule)) for molecule in molecules]
        for molecule, alkeneList in alkenes:
            molecules.remove(molecule)
            molecules += synAdd(molecule, alkeneList[0], alkeneList[1],
                                None, None)
    return molecules
'''


def hydrogenate(molecules):
    def findPlace(molecule):
        return findAlkenes(molecule)

    def reactAtPlace(molecule, place):
        return synAdd(molecule, place[0], place[1], None, None)

    return react(molecules, findPlace, reactAtPlace)


#abstract
def genericReaction(molecules, ):
    def findPlace(molecule): #returns one place at which the molecule can react -- e.g. a tuple of atoms, for alkenes/alkynes
        pass
    def reactAtPlace(molecule, place): #returns a list of molecules post-reaction at place
        pass
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

#halogen is a string
def hydrohalogenate(molecules, halogen):
    def findPlace(molecule): #returns one place at which the molecule can react -- e.g. a tuple of atoms, for alkenes/alkynes
        a = findAlkenes(molecule)
        if a == None:
            a = findAlkynes(molecule)

    def reactAtPlace(molecule, place): #returns a list of molecules post-reaction at place
        return bothAdd(molecule, place[0], place[1], Atom(halogen), None)
    
    return react(molecules, findPlace, reactAtPlace)


    
    '''newMolecules = []
    for molecule in molecules:
        for doublebond in findAlkenes(molecule):
            mkvCarbons = markovnikov(doublebond[0], doublebond[1])
            for pairing in mkvCarbons:
                newMolecules += bothAdd(molecule, pairing[0], pairing[1], Atom(halogen), None)
    return newMolecules'''



"""Halogenation
Candidate reactants: alkenes, alkynes
X2 in CH2Cl2, dark
Anti addition of an X to each atom in the alkene.
if 1eqv specified --> add once
if 2eqv or if excess specified --> add twice
if no quantity specified --> don't let it be a valid reaction? Some sort of feedback to make user specify _how much_ when reacting with alkynes (which is a good habit to have) would be nice."""

#halogen is a string
def halogenate(molecules, halogen):
    pass
'''
    newMolecules = []
    for molecule in molecules:
        for doublebond in findAlkenes(molecule):
            newMolecules += antiAdd(molecule, pairing[0], pairing[1], Atom(halogen), Atom(halogen))
        for triplebond in findAlkynes(molecule):

    return newMolecules
'''


"""Free-radical hydrohalogenation
Candidate reactants: alkenes
HBr cat ROOR, hv or heat
Adds the X to the anti-Markovnikov-most carbon in the alkene, and the H to the other one. Neither syn nor anti."""

#halogen is a string
def radicalhydrohalogenate(molecules, halogen):
    newMolecules = []

    
    def findPlace(molecule): #returns one place at which the molecule can react -- e.g. a tuple of atoms, for alkenes/alkynes
        a = findAlkenes(molecule)
        if a == None:
            a = findAlkynes(molecule)

    def reactAtPlace(molecule, place): #returns a list of molecules post-reaction at place
        print "Got here!"
        return bothAdd(molecule, place[0], place[1], None, Atom(halogen))
    
    return react(molecules, findPlace, reactAtPlace)

    '''
    for molecule in molecules:
        for doublebond in findAlkenes(molecule):
            mkvCarbons = markovnikov(doublebond[0], doublebond[1])
            for pairing in mkvCarbons:
                newMolecules += bothAdd(molecule, pairing[0], pairing[1], None, Atom(halogen))'''



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
#     C1/   \Br
c10 = Atom("C")
CTmol = Molecule(c10)
c11 = Atom("C")
CTmol.addAtom(c11, c10, 2)
c12 = Atom("C")
CTmol.addAtom(c12, c10, 1)
cl1 = Atom("Cl")
CTmol.addAtom(cl1, c10, 1)
cl2 = Atom("Cl")
CTmol.addAtom(cl2, c11, 1)
br10 = Atom("Br")
CTmol.addAtom(br10, c11, 1)
c10.newCTCenter(c11, cl1, c12)
c11.newCTCenter(c10, cl2, br10)

#Makes C\   /Cl
#        C=C
#     C1/   \Br
c15 = Atom("C")
CTmol2 = Molecule(c15)
c16 = Atom("C")
CTmol2.addAtom(c16, c15, 2)
c17 = Atom("C")
CTmol2.addAtom(c17, c15, 1)
cl5 = Atom("Cl")
CTmol2.addAtom(cl5, c15, 1)
cl6 = Atom("Cl")
CTmol2.addAtom(cl6, c16, 1)
br15 = Atom("Br")
CTmol2.addAtom(br15, c16, 1)
c15.newCTCenter(c16, cl6, c17)
c16.newCTCenter(c15, br15, cl5)

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




