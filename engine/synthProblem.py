from reactions import *
import randomGenerator
import random
import orgoStructure
import reactions as reactionsModule
import string

#Synthesis problem class
    #List of starting materials
    #List of molecules in target
    #List of reactionSteps
    #List of reagents the user has entered into sidebar
    #A synthesisSolution

    
    #Checks, when a new molecule or reagent is added to a reaction step, whether it matches any known reactions
        #If so, creates a new molecule to represent the reacted product.
        #Updates its knowledge of whether the problem is solved or not.

    #Can delete individual molecule-boxes or individual reaction-steps.

    #Can add: reagents to reaction-steps, reagents to molecule-boxes, reaction-steps to molecule-boxes, molecule-boxes to reaction-steps.
class SynthesisProblem:
    def __init__(self, startingMaterials, finalProduct, solution):
        self.
        self.startingMaterials = startingMaterials
        self.finalProduct = finalProduct
        self.steps = [] #to be a list of reactionSteps
        self.reagentsMade = [] #for the sidebar
        self.solution = solution



#SynthesisSolution class
    #List of reactionSteps
class SynthesisSolution:
    def __init__(self, steps):
        self.steps = [] #to be a list of reactionSteps



#ReactionStep class
    #Molecule box to point from
    #Molecule box to point to
    #List of added reagents
    #List of added molecules other than molecule box
class ReactionStep:
    def __init__(self, parentMoleculeBox):
        self.reactantBox = parentMoleculeBox
        self.otherMoleculeBoxes = []
        self.otherMolecules = []
        self.productBox = None
        
        #hasReagents is a dict that maps numbers (of reagents) to true/false
        self.hasReagents = parseReagentsString("")
    
    #Add more reagents.
    def addReagent(self, reagentBox): #reagentList is a list of reagent boxes
        for reagent in list(REAGENTS):
            if reagentBox.hasReagents[reagent]:
                self.hasReagents[reagent] = True
        return self.react()
          
    def addMolecule(self, moleculeBox):
        self.otherMoleculeBoxes += [moleculeBox]
        self.otherMolecules += moleculeBox.molecules
        
        
    #Returns True or False depending on whether or not a reaction occurred.
    #If True, it updates self.product to be a new MoleculeBox containing 
    def react(self, mode="generate"):
        #mode can be "generate" or "check".  Generate returns true iff the reaction makes
        #*new* products; check returns true iff the reaction specified is a valid combination
        #of reagents.
        
        #a helper function
        def hasReagent(acceptableReagents):
            return True in [self.hasReagents[x] for x in acceptableReagents]
            
        for reaction in REACTIONS:
        #This loops through all of the reagents, checking if they are satisfied.
            if (True in [not hasReagent(acceptableReagents) for acceptableReagents in reaction[0]]): #returns False if the list comprehension [hasReagent...] is either empty or all full of Trues
                continue
            else:
                #react!
                products = reaction[1](self.reactantBox.molecules)(self.otherMolecules) #a function of two variables
                if mode == "check":
                    #check if the output list is non-empty
                    #if so, reaction is successful
                    if products != []:
                        self.productBox = MoleculeBox(products)
                        return True
                    #if not, the old set of molecules remain intact
                    else:
                        self.productBox = MoleculeBox(self.reactantBox.molecules + self.otherMolecules)
                        return True
                elif mode == "generate":
                    #Return true if some new molecule was made during the course of the reaction
                    for product in products:
                        if sum([moleculeCompare(product, reactant) for reactant in self.reactantBox.molecules])==0:
                            self.productBox = MoleculeBox(products)
                            return True
                    return False
                else:
                    print "Invalid mode in react."
                    raise StandardError
                        
                
        return False
        
        #Check if reagent requirements are satisfied
        #Check if anything is produced by the reaction function
        
        
        
    #Returns a list of the reagents contained in this reaction step as HTML-printable strings.
    def stringList(self):
        return [REAGENTS[reagent][0] for reagent in list(self.hasReagents) if self.hasReagents[reagent]] 


#MoleculeBox class
#Represents a draggable box containing molecules (svg).
    #List of molecules contained in it
class MoleculeBox:
    def __init__(self, moleculesList):
        self.molecules = moleculesList

    #Returns a list of smiles of the molecules contained in this box.
    def stringList(self):
        return [smiles(mol) for mol in self.molecules]
        
        
#ReagentBox class
#Represents a draggable box containing some quantity of different reagents
    #List of reagents (as strings) contained in it
class ReagentBox:
    def __init__(self, reagentsString):
        self.reagentsString = reagentsString #a string of raw user input
        self.hasReagents = parseReagentsString(reagentsString) #a dictionary
        
    #Returns a list of the reagents contained in this reaction step as HTML-printable strings.
    def stringList(self):
        return [REAGENTS[reagent][0] for reagent in list(self.hasReagents) if self.hasReagents[reagent]] 
 
      
#Enter a string, such as "H2 cat Pd|C"
#Returns a dictionary, such as {"H2":True, "PDC":True, "ETOH":False, ...}
def parseReagentsString(inpstring):
    string = inpstring.lower()
    outp = {}
    
    if (inpstring == ""):
        for reagent in list(REAGENTS):
            outp[reagent] = False
        return outp
        
    for reagent in list(REAGENTS):
        outp[reagent] = False
        for spelling in REAGENTS[reagent][1]:
            if spelling.lower() in string:
                outp[reagent] = True

    #hacky
    #Make sure you don't count substrings if you're counting things they're part of.
    if outp[CH2CL2]:
        if (inpstring.count("h2") - inpstring.count("ch2cl2")) == 0:
            outp[H2] = False
        if (inpstring.count("cl2") - inpstring.count("ch2cl2")) == 0:
            outp[CL2] = False
    if outp[NANH2]:
        if (inpstring.count("na") - inpstring.count("nanh2")) == 0:
            outp[NA] = False
    if outp[NAOH]:
        if (inpstring.count("na") - inpstring.count("naoh")) == 0:
            outp[NA] = False
    
    return outp
            
def randomSynthesisProblemMake(mode = "Everything", steps = 10):
    #Mode controls the reagents that are legal, as well as the distribution of starting materials.
    reactions = [] #List of reactions that we want to keep
    if mode == "AlkeneAlkyne":
        molBoxes = []
        for i in xrange(2):
        #MoleculeBox([randomGenerator.randomStart(alkyneProb=0.3,
        #    BrProb=0.05, ClProb=0.05, OHProb=0.05,forceTerminalAlkyne = True)[0]])
            molBoxes.append(MoleculeBox([reactionsModule.propyne]))
        legalRxns = ALKENEALKYNE
    elif mode == "Everything":
        molBoxes = []
        for i in xrange(2):
            molBoxes.append(MoleculeBox([randomGenerator.randomStart()[0]]))
        legalRxns = REACTIONS
    else:
        print "Invalid mode in randomSynthesisProblemMake"
    legalAddRxns = [reaction for reaction in ADDREACTIONS if (reaction in legalRxns)]
    #Add other modes here.
    if debug:
        print "Initial mol: "+str(smiles(molBoxes[0].molecules)) + ' , ' + str(smiles(molBoxes[1].molecules))
    
    goodSteps = 0    #Number of successful steps taken.
    for attemptNo in xrange(steps):
        newMolBoxes = []
        for molBox in molBoxes:
            reagents, rxnFunction, ignore = legalRxns[random.randint(0, len(legalRxns)-1)]
            if debug:
                print "Trying step: " + str(reagents)
            currentRxn = ReactionStep(molBox)
            for reagent in reagents:
                currentRxn.hasReagents[reagent[0]] = True
            if currentRxn.react() and len(currentRxn.productBox.molecules)+len(molBox.molecules)<5:
                #A good reaction.
                newMolBoxes.append(currentRxn.productBox)
                reactions.append(currentRxn)
                goodSteps += 1
                if debug:
                    print "Result: " +str(smiles(currentRxn.productBox.molecules))
                    print "I think there are: " +str(len(molBox.molecules))
            else:
                newMolBoxes.append(molBox)
        #Now, try to fuse molecules?
        reagents, rxnFunction, ignore = legalAddRxns[random.randint(0, len(legalAddRxns)-1)]
        if debug:
            print "Trying fusion: "+str(reagents)
        molBoxes = []
        if len(newMolBoxes) == 1:
            #No point in trying to fuse molecules if you only have one.
            molBoxes = newMolBoxes
            continue
        for i in xrange(len(newMolBoxes)):
            for j in xrange(i+1,len(newMolBoxes)):
                #Loop through all pairs of molecules.
                molBox1 = newMolBoxes[i]
                molBox2 = newMolBoxes[j]
                cc1 = molBox1.molecules[0].countElement('C')
                cc2 = molBox2.molecules[0].countElement('C')
                currentRxn = ReactionStep(molBox1)
                currentRxn.addMolecule(molBox2)
                for reagent in reagents:
                    currentRxn.hasReagents[reagent[0]] = True
                if currentRxn.react():
                    #OK, we have a reaction.  But, did we get fusion?
                    if sum([product.countElement('C') == cc1 + cc2 for product in currentRxn.productBox.molecules]) > 0:
                        #Success!
                        reactions.append(currentRxn)
                        newMolBoxes.remove(molBox1)
                        newMolBoxes.remove(molBox2)
                        molBoxes = newMolBoxes + [currentRxn.productBox]
                        if debug:
                            print "Result: " +str(smiles(currentRxn.productBox.molecules))
        if len(molBoxes) == 0:
            #Didn't fuse any molecules.  Oh well.
            molBoxes = newMolBoxes
    return reactions
                            







#Some constants
H2=1 
PDC=2
ETOH=3
HF=4
HBR=5
HCL=6
HI=7
CH2CL2=8
F2=9
BR2=10
CL2=11
I2=12
ROOR=13
RCO3H=14
H2SO4=15
H2O=16
HGSO4=17
BH3=18
THF=19
NAOH=20
H2O2=21
OSO4=22
NMO=23
ACETONE=24
O3=25
ME2S=26
ZN=27
LINDLAR=28
NA=29
NH3=30
NANH2=31
EQV1=32
HEAT=33
LIGHT=34







#This gigantic terrible tuple is for determining which reaction should take place.

#First item of each tuple in this list:
    #a set of necessary reagents. Things listed together have an "or" relationship.
            #E.g. (("O3",),("CH2CL2",),("ME2S", "ZN")) means ozone AND ch2cl2 AND (me2s OR zn)
#Second item of each tuple in this list:
    #a function of two variables, which takes in a list of molecules (x) and another list of molecules (o) and returns them reacted
#These are listed roughly by precedence: earlier-listed reactions which qualify take precedence over later-listed ones.
ALKENEALKYNE = (
(((H2,),(PDC,)), (lambda x: lambda o: hydrogenate(x+o)), ()),
(((HBR,),(CH2CL2,)), (lambda x: lambda o: hydrohalogenate(x+o, "Br")), ()),
(((HF,),(CH2CL2,)), (lambda x: lambda o: hydrohalogenate(x+o, "F")), ()),
(((HI,),(CH2CL2,)), (lambda x: lambda o: hydrohalogenate(x+o, "I")), ()),
(((HCL,),(CH2CL2,)), (lambda x: lambda o: hydrohalogenate(x+o, "Cl")), ()),
(((BR2,),(CH2CL2,),(EQV1,)), (lambda x: lambda o: halogenate1eq(x+o, "Br")), ()),
(((F2,),(CH2CL2,),(EQV1,)), (lambda x: lambda o: halogenate1eq(x+o, "F")), ()),
(((I2,),(CH2CL2,),(EQV1,)), (lambda x: lambda o: halogenate1eq(x+o, "I")), ()),
(((CL2,),(CH2CL2,),(EQV1,)), (lambda x: lambda o: halogenate1eq(x+o, "Cl")), ()),
(((BR2,),(CH2CL2,)), (lambda x: lambda o: halogenate(x+o, "Br")), ()),
(((F2,),(CH2CL2,)), (lambda x: lambda o: halogenate(x+o, "F")), ()),
(((I2,),(CH2CL2,)), (lambda x: lambda o: halogenate(x+o, "I")), ()),
(((CL2,),(CH2CL2,)), (lambda x: lambda o: halogenate(x+o, "Cl")), ()),
(((HBR,), (ROOR,), (HEAT, LIGHT)), (lambda x: lambda o: radicalhydrohalogenate(x+o, "Br")), ()),
(((RCO3H,), (CH2CL2,)), (lambda x: lambda o: epoxidate(x+o)), ()),
(((H2SO4,), (H2O,)), (lambda x: lambda o: acidhydrate(x+o, Molecule(Atom("O")))), ()),
(((H2SO4,), (ETOH,)), (lambda x: lambda o: acidhydrate(x+o, ethanol)), ()),
(((H2SO4,),), (lambda x: lambda o: acidhydrate(x, o)), ()),
(((H2SO4,), (H2O,), (HGSO4,)), (lambda x: lambda o: acidhydrate(x+o, Molecule(Atom("O")), True)), ()),
(((H2SO4,), (ETOH,), (HGSO4,)), (lambda x: lambda o: acidhydrate(x+o, ethanol, True)), ()),
(((H2SO4,), (HGSO4,)), (lambda x: lambda o: acidhydrate(x, o, True)), ('add')),
(((BR2,), (H2O,)), (lambda x: lambda o: halohydrate(x+o, Molecule(Atom("O")), "Br")),()),
(((BR2,), (ETOH,)), (lambda x: lambda o: halohydrate(x+o, ethanol, "Br")), ()),
(((BR2,),), (lambda x: lambda o: halohydrate(x, o, "Br")), ()),
(((I2,), (H2O,)), (lambda x: lambda o: halohydrate(x+o, Molecule(Atom("O")), "I")),()),
(((I2,), (ETOH,)), (lambda x: lambda o: halohydrate(x+o, ethanol, "I")), ()),
(((I2,),), (lambda x: lambda o: halohydrate(x, o, "I")), ()),
(((F2,), (H2O,)), (lambda x: lambda o: halohydrate(x+o, Molecule(Atom("O")), "F")), ()),
(((F2,), (ETOH,)), (lambda x: lambda o: halohydrate(x+o, ethanol, "F")), ()),
(((F2,),), (lambda x: lambda o: halohydrate(x, o, "F")), ()),
(((CL2,), (H2O,)), (lambda x: lambda o: halohydrate(x+o, Molecule(Atom("O")), "Cl")),()),
(((CL2,), (ETOH,)), (lambda x: lambda o: halohydrate(x+o, ethanol, "Cl")), ()),
(((CL2,),), (lambda x: lambda o: halohydrate(x, o, "Cl")), ()),
(((BH3,), (THF,), (NAOH,), (H2O2,)), (lambda x: lambda o: hydroborate(x+o)), ()),
(((BH3,), (THF,)), (lambda x: lambda o: hydroborate1(x+o)), ()),
(((NAOH,), (H2O2,)), (lambda x: lambda o: hydroborate2(x+o)), ()),
(((OSO4,), (NMO,), (ACETONE, H2O)), (lambda x: lambda o: dihydroxylate(x+o)), ()),
(((O3,),(CH2CL2,),(ME2S,ZN)), (lambda x: lambda o: ozonolyse(x+o)), ()),
(((NA,), (NH3,)), (lambda x: lambda o: sodiumAmmonia(x+o)), ()),
(((LINDLAR,), (H2,)), (lambda x: lambda o: lindlar(x+o)), ()),
(((NANH2,), (NH3,)), (lambda x: lambda o: alkyneDeprotonate(x+o)), ()),
((), (lambda x: lambda o: acetylideAdd(x, o)),('add'))
)

REACTIONS = ALKENEALKYNE

ADDREACTIONS = [reaction for reaction in REACTIONS if ('add' in reaction[2])]


#This dictionary is for understanding what people type in.

#List of synonyms of reagents.
#The first value in the tuple is how it should be printed (with proper subscripts).
#The second value in the tuple is all of the items that should be recognizable as user input.

#When adding a new reagent, also be sure to update REACTIONS, to add a value for the constant,
#and to update the section flagged "hacky" in the methods above.
REAGENTS = {
H2: ("H<sub>2</sub>",("H2", "Hydrogen")),
PDC: ("Pd|C", ("PdC", "Pd/C", "Pd|C", "Pd C", "palladium")),
ETOH: ("EtOH", ("EtOH", "Ethanol", "Ethyl alcohol", "C2H5OH")),
HF: ("HF", ("HF", "Hydrogen fluoride", "Hydrofluoric acid")),
HBR: ("HBr", ("HBr", "Hydrogen bromide", "Hydrobromic acid")),
HCL: ("HCl", ("HCl", "Hydrogen chloride", "Hydrochloric acid")),
HI: ("HI", ("HI", "Hydrogen iodide", "Hydroiodic acid")),
CH2CL2: ("CH<sub>2</sub>Cl<sub>2</sub>", ("CH2Cl2", "Dichloromethane")),
F2: ("F<sub>2</sub>", ("Fluorine", "F2")),
BR2: ("Br<sub>2</sub>", ("Bromine", "Br2")),
CL2: ("Cl<sub>2</sub>", ("Chlorine", "Cl2")),
I2: ("I<sub>2</sub>", ("Iodine", "I2")),
ROOR: ("ROOR", ("ROOR", "tBuOOtBu", "Peroxide", "Tert-butyl peroxide", "Di-tert-butyl peroxide")),
RCO3H: ("RCO3H",("mCPBA", "PhCO3H", "RCO3H")),
H2SO4: ("H<sub>2</sub>SO<sub>4</sub>", ("H2SO4", "Sulfuric acid")),
H2O: ("H<sub>2</sub>O", ("H2O", "Water", "Dihydrogen monoxide", "HOH")),
HGSO4: ("HgSO<sub>4</sub> accels.", ("HgSO4", "Hg2+", "Mercury sulfate")),
BH3: ("BH<sub>3</sub>", ("BH3", "Borane")),
THF: ("THF", ("THF", "Tetrahydrofuran")),
NAOH: ("NaOH", ("NaOH", "Sodium hydroxide", "Hydroxide", "OH-")),
H2O2: ("H<sub>2</sub>O<sub>2</sub>", ("H2O2", "Hydrogen peroxide")),
OSO4: ("OsO<sub>4</sub>", ("oso4", "osmium tetroxide", "osmium oxide")),
NMO: ("NMO", ("NMO", "NMMO", "N-Methylmorpholine N-oxide")),
ACETONE: ("Acetone", ("Acetone", "Propanone", "(CH3)2CO")),
O3: ("O<sub>3</sub>", ("Ozone", "O3")),
ME2S: ("Me<sub>2</sub>S", ("Dimethyl sulfide", "Methylthiomethane", "Me2S")),
ZN: ("Zn", ("Zn", "Zinc")),
LINDLAR: ("cat. Lindlar", ("Lindlar",)),
NA: ("Na", ("Sodium", "Na")),
NH3: ("NH<sub>3 (L)</sub>", ("NH3", "Ammonia")),
NANH2: ("NaNH<sub>2</sub>", ("Sodium amide", "Sodamide", "NaNH2", "Amide")),
EQV1: ("1 equiv.", ("1", "eq", "one")),
HEAT: ("Heat", ("heat", "delta", "hot", "warm")),
LIGHT: ("Light", ("hv", "light", "bright", "nu", "v", "hnu"))
}


#Debugging
if __name__ == "__main__":
    print randomSynthesisProblemMake(mode="AlkeneAlkyne")

