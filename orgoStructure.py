class Molecule:
    
    def __init__(self, firstAtom):
        self.atoms = [firstAtom]
        
    def addAtom(self, newAtom, targetAtom, bondOrder):
        if targetAtom not in self.atoms:
            print "Error in addAtom: target atom not already in molecule."
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

        #Temporary values which should only be meaningful within smiles.
        #for traversing
        self.flag = 0
        #for ring-finding
        self.rflag = 0 #0 if not part of a ring bond, <0 if otherwise
        self.rAtom = 0 #0 if not part of a ring bond, the other-atom the bond is made with if otherwise
        self.nRead = 0 #neighbors already read
        self.parentAtom = 0 #atom right before this one


def smiles(molecule):
    if len(molecule.atoms)==0: return ""
    
    ringsfound = 0
    curAtom = molecule.atoms[0]
    homeAtom = molecule.atoms[0]

    #Traverse the molecule once, to hunt down and flag rings.
    #Each iteration: (...while we aren't back to the home atom, or if we are,
                    #while the home atom still has neighbors to read)
    while ((curAtom != homeAtom) or (homeAtom.nRead < len(homeAtom.neighbors))):
    
        #flag current atom as "read" (flag = 1)
        curAtom.flag = 1
        
        #if there are neighbors left to read from this atom:
        if (curAtom.nRead < len(curAtom.neighbors)):
            
            #if the next atom is the parent atom:
            if list(curAtom.neighbors)[curAtom.nRead] == curAtom.parentAtom:
                #don't do anything but incrementing nRead
                curAtom.nRead += 1
                
            #else,
            else:
                if list(curAtom.neighbors)[curAtom.nRead].nRead == 0:
                #if the next atom has not been traversed yet:
                    curAtom.nRead += 1
                    list(curAtom.neighbors)[curAtom.nRead - 1].parentAtom = curAtom
                    curAtom = list(curAtom.neighbors)[curAtom.nRead - 1]
                    #increment current atom's nRead counter
                    #make the next atom the current atom:
                    #make the old atom the next atom's parent

                else:
                #if the next atom has been traversed yet:
                    #it's a ring!
                    ringsfound += 1
                    curAtom.rflag = ringsfound
                    list(curAtom.neighbors)[curAtom.nRead].rflag = ringsfound
                    curAtom.nRead += 1
                    curAtom.rAtom = list(curAtom.neighbors)[curAtom.nRead - 1]
                    list(curAtom.neighbors)[curAtom.nRead - 1].rAtom = curAtom
                    #increment ringsfound
                    #set rflag on both atoms to ringsfound
                    #increment current atom's nRead counter
                    #make sure the atoms know who each other is
                
        #if not:
            #go backwards to parent atom:
            #set curAtom to its parent atom
        else:
            curAtom = curAtom.parentAtom
            
            
    #Traverse twice to generate the SMILES.
    outp = subsmiles(molecule, molecule.atoms[0], 0)

    #Reset all old flags.    
    for atom in molecule.atoms:
        atom.flag = 0
        atom.rflag = 0
        atom.nRead = 0
        atom.parentAtom = 0
        atom.rAtom = 0

    return outp

bondSymbols = ['0', '-', '=', '#', '4', '5', '6', '7', '8', '9']
#Precondition: molecule has been flagged for ring positioning (some rflag values on atoms might != 0)
def subsmiles(molecule, startAtom, parentAtom):
    #Creates and returns a SMILES string for unflagged (!atom.flag==2) atoms within a molecule, starting with the given atom

    outp = startAtom.element

    #If the molecule has an rflag, find the neighbor it bonds with.
    #If that neighbor has already been traversed, add the rflag while specifying the bond.
    #If not, just add the rflag.
    if startAtom.rflag != 0:
        if startAtom.rAtom.flag == 1:
            outp += bondSymbols[startAtom.neighbors[rAtom]]
        outp += startAtom.rflag
    
    #Flag the current atom.
    startAtom.flag = 1

    #Add new groups for all neighbor atoms which are not the parent atom and not the rAtom.
    #Recursion is your friend.
    #Be sure to specify the base case (when zero non-parent non-ring atoms are available to bond to)
    toAdd = [atom for atom in list(startAtom.neighbors) if not (atom==startAtom.rAtom or atom==parentAtom)]

    #In the base case, this loop won't even be entered.
    for atom in toAdd:
        outp += "(" +bondSymbols[startAtom.neighbors[atom]] + subsmiles(molecule, atom, startAtom) + ")" 
    return outp
    


#Makes HO-C=C-N
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

print smiles(mol)
