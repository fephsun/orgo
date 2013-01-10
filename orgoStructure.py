#Testing - replace "H" with "Br" to visualize all hydrogens
hydrogen = "H"

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

    def addHydrogens(self):
        #Adds a full complement of hydrogens to every atom.
        #As a side-effect, also checks for over-valence.
        for atom in self.atoms:
            if atom.element == 'C':
                maxval = 4
            elif atom.element == 'N':
                maxval = 3
            elif atom.element == 'O':
                maxval = 2
            else:
                continue
            val = 0
            for neighbor in atom.neighbors:
                val += atom.neighbors[neighbor]
            if val > maxval:
                print str(atom) + " has too many bonds!"
                raise StandardError
            for i in xrange(maxval-val):
                H = Atom(hydrogen)
                self.addAtom(H, atom, 1)

    def countElement(self, element):
        out = 0
        for atom in self.atoms:
            if atom.element == element:
                out += 1
        return out


class Atom:

    def __str__(self):
        return self.element
    
    def __init__(self, element):
        self.element = element
        self.neighbors = dict()

        #Temporary values which should only be meaningful within smiles() and subsmiles().
        #for traversing
        self.flag = 0
        #for ring-finding
        self.rflag = 0 #0 if not part of a ring bond, <0 if otherwise
        self.rAtom = 0 #0 if not part of a ring bond, the other-atom the bond is made with if otherwise
        self.nRead = 0 #neighbors already read
        self.parentAtom = 0 #atom right before this one
        self.nonHNeighbors = []



    def newChiralCenter(self, reference, clockwiseList):
        #Set up this atom as a chiral center.
        #reference is an Atom; clockwiseList is a list of 3 Atoms
        self.chiralA = reference
        self.chiralB, self.chiralC, self.chiralD = clockwiseList

    def chiralCWlist(self, reference):
        #Returns a list of the other 3 Atoms bonded to this Atom,
        #in clockwise order when looking down reference.
        if reference == self.chiralA:
            return [self.chiralB, self.chiralC, self.chiralD]
        elif reference == self.chiralB:
            return [self.chiralA, self.chiralD, self.chiralC]
        elif reference == self.chiralC:
            return [self.chiralA, self.chiralB, self.chiralD]
        elif reference == self.chiralD:
            return [self.chiralA, self.chiralC, self.chiralB]
        
    def newCTCenter(self, otherC, a, b):
        #CTCenters (cis-trans centers) must come in pairs.  Both of the
        #carbons across the double bond must have a CTCenter.  Atom a is
        #directly clockwise from otherC.  Atom b is directly counterclockwise.
        self.CTotherC = otherC
        self.CTa = a
        self.CTb = b

    def eliminateCT(self):
        del(self.CTotherC)
        del(self.CTa)
        del(self.CTb)


def smiles(molecule):
    if len(molecule.atoms)==0: return ""
    
    ringsfound = 0
    curAtom = molecule.atoms[0]
    homeAtom = molecule.atoms[0]

    #Create the dictionary nonHNeighbors for each atom.
    for atom in molecule.atoms:
        atom.nonHNeighbors = dict((a, b) for (a, b)in atom.neighbors.items() if a.element.lower() != "h")
    

    #Traverse the molecule once, to hunt down and flag rings.
    #Each iteration: (...while we aren't back to the home atom, or if we are,
                    #while the home atom still has neighbors to read)
    while ((curAtom != homeAtom) or (homeAtom.nRead < len(homeAtom.nonHNeighbors))):
    
        #flag current atom as "read" (flag = 1)
        curAtom.flag = 1
        
        #if there are neighbors left to read from this atom:
        if (curAtom.nRead < len(curAtom.nonHNeighbors)):
            
            #if the next atom is the parent atom:
            if list(curAtom.nonHNeighbors)[curAtom.nRead] == curAtom.parentAtom:
                #don't do anything but incrementing nRead
                curAtom.nRead += 1
                
            #else,
            else:
                if list(curAtom.nonHNeighbors)[curAtom.nRead].nRead == 0:
                #if the next atom has not been traversed yet:
                    curAtom.nRead += 1
                    list(curAtom.nonHNeighbors)[curAtom.nRead - 1].parentAtom = curAtom
                    curAtom = list(curAtom.nonHNeighbors)[curAtom.nRead - 1]
                    #increment current atom's nRead counter
                    #make the next atom the current atom:
                    #make the old atom the next atom's parent

                else:
                #if the next atom has been traversed yet:
                    #it's a ring!
                    ringsfound += 1
                    curAtom.rflag = ringsfound
                    list(curAtom.nonHNeighbors)[curAtom.nRead].rflag = ringsfound
                    curAtom.nRead += 1
                    curAtom.rAtom = list(curAtom.nonHNeighbors)[curAtom.nRead - 1]
                    list(curAtom.nonHNeighbors)[curAtom.nRead - 1].rAtom = curAtom
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

#Precondition: molecule has been flagged for ring positioning (some rflag values on atoms might != 0). This is done by smiles().
def subsmiles(molecule, startAtom, parentAtom):
    #Creates and returns a SMILES string for unflagged (!atom.flag==2) atoms within a molecule, starting with the given atom

    outp = startAtom.element

	
    #Add charge if relevant.
    #UNIMPLEMENTED
	

	
    
    
   
	
    #Check if the atom is a chiral center. If so:
    if hasattr(startAtom, 'chiralA'):
        hasH = (True in [a.element.lower()=="h" for a in list(startAtom.neighbors)]) or (None in [startAtom.chiralA, startAtom.chiralB, startAtom.chiralC, startAtom.chiralD])
        hasP = (parentAtom != 0)
        #If the atom has a hydrogen:
        #Add [ and @@H] to the current output. (e.g. [C@@H]
        #If the atom does not have a hydrogen:
        #Add [ and @@] to the current output. (e.g. [C@@]
        #Then, add the remaining neighbors in the proper order.
        #Implement this by smart rearrangement of toAdd.
        #Be mindful of: whether or not there is a parent atom; whether or not there is a hydrogen.
        if hasH:
            outp = "[" + outp + "@@H]"
            if hasP:
                #toAdd should have two elements
                l = startAtom.chiralCWlist(parentAtom) #list of three atoms
                x = l.index(None) #index of hydrogen atom in list
                toAdd = [l[(x+1) %3], l[(x+2) %3]] #correct permutation
            else:
                #toAdd should have three elements
                toAdd = startAtom.chiralCWlist(None) #list of three atoms
        else:
            outp = "[" + outp + "@@]"
            if hasP:
                #toAdd should have three elements
                toAdd = startAtom.chiralCWlist(parentAtom)
            else:
                #toAdd should have four elements
                arbitraryRef = list(startAtom.neighbors)[0]
                l = startAtom.chiralCWlist(arbitraryRef)
                toAdd = [arbitraryRef] + l
                
    #Prepare to add new groups for all neighbor atoms which are not the parent atom and not the rAtom.
    else:
        toAdd = [atom for atom in list(startAtom.nonHNeighbors) if not (atom==startAtom.rAtom or atom==parentAtom or atom==None)]
		

	#Check if the atom is a cis-trans center.
	#UNIMPLEMENTED
		
    #If the molecule has an rflag, find the neighbor it bonds with.
    #If that neighbor has already been traversed, add the rflag while specifying the bond.
    #If not, just add the rflag.
	#Worry about cis-trans centers if the rflag relates to a double bond.
    if startAtom.rflag != 0:
        if startAtom.rAtom.flag == 1:
            outp += bondSymbols[startAtom.nonHNeighbors[startAtom.rAtom]]
        outp += str(startAtom.rflag)

    
    #Flag the current atom.
    startAtom.flag = 1

    
    #Recursion is your friend.
    #Be sure to specify the base case (when zero non-parent non-ring atoms are available to bond to)
    #In the base case, this loop won't even be entered.
    for atom in toAdd:
        outp += "(" +bondSymbols[startAtom.nonHNeighbors[atom]] + subsmiles(molecule, atom, startAtom) + ")" 
    return outp


def moleculeCompare(a, b):
    #Determines whether two molecules are isomorphic.  In the worst case
    #(two molecules with the same atoms), this procedure does not run in
    #polynomial time, so be careful.
    for ele in ['C','N','O']:
        if a.countElement(ele) != b.countElement(ele):
            return False
    for bAtom in b.atoms:
        if bAtom.element == a.atoms[0].element:
                
    


#Makes     C-C-C-C
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
print smiles(mol)






