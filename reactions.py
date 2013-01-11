from helperFunctions import *

def hydrogenate(molecules):
    #H2/PdC catalyst reaction for double bonds only, for now.  Syn addition.
    for molecule in molecules:
        for carbon in molecule.atoms:
            if carbon.element != 'C':
                continue
            for neighbor in carbon.neighbors:
                if neighbor.element == 'C' and carbon.neighbors[neighbor] == 2:
                    molecules.remove(molecule)
                    molecules += synAdd(molecule, carbon, neighbor, None, None)
    return molecules

"""Hydrohalogenation
HX in CH2Cl2
Candidate reactants: alkenes, alkynes
Adds the X to the Markovnikov-most carbon, and the H to the other carbon. Neither syn nor anti (because carbocation intermediate).
**UNLESS the alkene is next to a carbonyl (i.e. Michael acceptor). In this case, the halogen is added anti-Markovnikov. We might want to allow users to use this 

reaction, but not allow it to be used when we generate random synthesis problems.
If reacting an alkyne:
if 1eqv specified --> add once
if 2eqv or if excess specified --> add twice
if no quantity specified --> don't let it be a valid reaction? Some sort of feedback to make user specify _how much_ when reacting with alkynes (which is a good habit 

to have) would be nice."""


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
#     C1/
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
c10.newCTCenter(c11, cl1, c12)
c11.newCTCenter(c10, cl2, None)

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

hydrogenate([mol])
