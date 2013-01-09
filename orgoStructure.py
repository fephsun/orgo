class Molecule:
    
    def __init__(self, firstAtom):
        self.atoms = [firstAtom]
        
    def addAtom(self, newAtom, targetAtom, bondOrder):
        if targetAtom not in self.atoms:
            print "Error in addAtom: target atom not already in molecule."
            raise StandardError
        if newAtom in self.atoms:
            print "Error in addAtom: new atom already in molecule.  Use addBond instead."
            raise StandardError
        self.atoms.append(newAtom)
        self.addBond(newAtom, targetAtom, bondOrder)
        
    def addBond(self, atom1, atom2, bondOrder):
        atom1.neighbors[atom2] = bondOrder
        atom2.neighbors[atom1] = bondOrder
        
    def removeAtom(self, target):
        for atom in self.atoms:
            if target in atom.neighbors:
                del(atom.neighbors[target])
        self.atoms.remove(target)
        del(target)
        
    def changeBond(self, atom1, atom2, newBondOrder):
        #newBondOrder=0 breaks the bond.
        if newBondOrder == 0:
            del(atom1.neighbors[atom2])
            del(atom2.neighbors[atom1])
        else:
            atom1.neighbors[atom2] = newBondOrder
            atom2.neighbors[atom1] = newBondOrder


class Atom:
    
    def __init__(self, element):
        self.element = element
        self.neighbors = dict()


#Makes     C-C-C-C
#          |   |
#       HO-C=C-N
c1 = Atom("C")
mol = Molecule(c1)
c2 = Atom("C")
n1 = Atom("N")
mol.addAtom(c2, c1, 2)
mol.addAtom(n1, c2, 1)
o1 = Atom("O")
h1 = Atom("H")
mol.addAtom(o1, c1, 1)
mol.addAtom(h1, o1, 1)
c3 = Atom("C")
mol.addAtom(c3, n1, 1)
c4 = Atom("C")
c5 = Atom("C")
mol.addAtom(c4, c3, 1)
mol.addAtom(c5, c3, 1)
c6 = Atom("C")
mol.addAtom(c6, c5, 1)
mol.addBond(c6, c1, 1)
