class Molecule:
    def __init__(self, firstAtom):
        self.atoms = [firstAtom]
        self.bonds = []
    def addAtom(self, newAtom, targetAtom, bondOrder):
        self.atoms.append(newAtom)
        self.bonds.append(Bond(newAtom, targetAtom, bondOrder))
    def addBond(self, atom1, atom2, bondOrder):
        self.bonds.append(Bond(atom1, atom2, bondOrder))
    def removeAtom(self, atom):
        for bond in self.bonds:
            if bond.end1 == atom or bond.end2 == atom:
                self.bonds.remove(bond)
        self.atoms.remove(atom)
    
    
class Atom:
    def __init__(self, element):
        self.element = element

class Bond:
    def __init__(self, end1, end2, order):
        self.end1 = end1
        self.end2 = end2
        self.order = order
