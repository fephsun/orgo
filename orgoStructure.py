class Molecule:
    def __init__(self, firstAtom):
        self.atoms = [firstAtom]
    def addAtom(self, newAtom, targetAtom, bondOrder):
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
    
    
class Atom:
    def __init__(self, element):
        self.element = element
        self.neighbors = dict()
