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
        self.startingMaterials = startingMaterials
        self.finalProduct = finalProduct
        self.steps = [] #to be a list of reactionSteps
        self.reagentsMade = [] #for the sidebar
        self.solution = solution
        self.isSolved = False



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
        self.reactant = parentMoleculeBox
        self.otherMolecules = []
        self.product = None
        
        self.hasReagents = parseReagentsString("")
    
    def addReagent(reagentBox): #reagentList is a list of reagent boxes
        for reagent in list(REAGENTS):
            if reagentBox.hasReagents[reagent]:
                self.hasReagents[reagent] = True
        return react()
          
    def addMolecule(moleculeBox):
        self.otherMolecules += moleculeBox.molecules
		
		
    #Returns True or False depending on whether or not a reaction occurred.
    #If True, it updates self.product to be a new MoleculeBox containing 
    def react():
        #Check if reagent requirements are satisfied
        #Check if anything is produced by the reaction function
        
        


#MoleculeBox class
    #List of molecules contained in it
class MoleculeBox:
    def __init__(self, moleculesList):
        self.molecules = moleculesList

#ReagentBox class
    #List of reagents (as strings) contained in it
class ReagentBox:
    def __init__(self, reagentsString):
        self.reagentsString = reagentsString
        self.hasReagents = parseReagentsString(reagentsString)
        
 
      
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
    return outp
            
def randomSynthesisProblemMake():
    pass


#Returns a new MoleculeBox if the reaction step has the proper reagents to produce one of the standard reactions.
def getProduct(reactionStep):
    pass

#First item of each tuple in this list:
    #a set of necessary reagents. Things listed together have an "or" relationship.
            #E.g. (("O3",),("CH2CL2",),("ME2S", "ZN")) means ozone AND ch2cl2 AND (me2s OR zn)
#Second item of each tuple in this list:
    #a function of two variables, which takes in a list of molecules (x) and another list of molecules (o) and returns them reacted
#These are listed roughly by precedence: earlier-listed reactions which qualify take precedence over later-listed ones.
REACTIONS = (
(((H2,),(PDC,)), (lambda x: hydrogenate(x))),
(((HBR,),(CH2CL2,)), (lambda x: hydrohalogenate(x, "Br"))),
(((HF,),(CH2CL2,)), (lambda x: hydrohalogenate(x, "F"))),
(((HI,),(CH2CL2,)), (lambda x: hydrohalogenate(x, "I"))),
(((HCL,),(CH2CL2,)), (lambda x: hydrohalogenate(x, "Cl"))),
(((BR2,),(CH2CL2,),(EQV1,)), (lambda x: halogenate1eq(x, "Br"))),
(((F2,),(CH2CL2,),(EQV1,)), (lambda x: halogenate1eq(x, "F"))),
(((I2,),(CH2CL2,),(EQV1,)), (lambda x: halogenate1eq(x, "I"))),
(((CL2,),(CH2CL2,),(EQV1,)), (lambda x: halogenate1eq(x, "Cl"))),
(((BR2,),(CH2CL2,)), (lambda x: halogenate(x, "Br"))),
(((F2,),(CH2CL2,)), (lambda x: halogenate(x, "F"))),
(((I2,),(CH2CL2,)), (lambda x: halogenate(x, "I"))),
(((CL2,),(CH2CL2,)), (lambda x: halogenate(x, "Cl"))),
(((HBR,), (ROOR,), (HEAT, LIGHT)), (lambda x: radicalhydrohalogenate(x, "Br"))),
(((RCO3H,), (CH2CL2,)), (lambda x: epoxidate(x))),
(((H2SO4,), (H2O,)), (lambda x: acidhydrate(x, Molecule(Atom("O"))))),
(((H2SO4,), (ETOH,)), (lambda x: acidhydrate(x, ethanol))),
(((H2SO4,),), (lambda x: acidhydrate(x, o))),
(((H2SO4,), (H2O,), (HGSO4,)), (lambda x: acidhydrate(x, Molecule(Atom("O")), True))),
(((H2SO4,), (ETOH,), (HGSO4,)), (lambda x: acidhydrate(x, ethanol, True))),
(((H2SO4,), (HGSO4,)), (lambda x: acidhydrate(x, o, True))),
(((BR2,), (H2O,)), (lambda x: halohydrate(x, Molecule(Atom("O")), "Br")),
(((BR2,), (ETOH,)), (lambda x: halohydrate(x, ethanol, "Br")))),
(((BR2,),), (lambda x: halohydrate(x, o, "Br"))),
(((I2,), (H2O,)), (lambda x: halohydrate(x, Molecule(Atom("O")), "I")),
(((I2,), (ETOH,)), (lambda x: halohydrate(x, ethanol, "I")))),
(((I2,),), (lambda x: halohydrate(x, o, "I"))),
(((F2,), (H2O,)), (lambda x: halohydrate(x, Molecule(Atom("O")), "F")),
(((F2,), (ETOH,)), (lambda x: halohydrate(x, ethanol, "F")))),
(((F2,),), (lambda x: halohydrate(x, o, "F"))),
(((CL2,), (H2O,)), (lambda x: halohydrate(x, Molecule(Atom("O")), "Cl")),
(((CL2,), (ETOH,)), (lambda x: halohydrate(x, ethanol, "Cl")))),
(((CL2,),), (lambda x: halohydrate(x, o, "Cl"))),
(((BH3,), (THF,), (NAOH,), (H2O2,)), (lambda x: hydroborate(x))),
(((BH3,), (THF,)), (lambda x: hydroborate1(x))),
(((NAOH,), (H2O2,)), (lambda x: hydroborate2(x))),
(((OSO4,), (NMO,), (ACETONE, H2O)), (lambda x: dihydroxylate(x))),
(((O3,),(CH2CL2,),(ME2S,ZN)), (lambda x: ozonolyse(x))),
(((NA,), (NH3,)), (lambda x: sodiumAmmonia(x))),
(((NANH2,), (NH3,)), (lambda x: alkyneDeprotonate(x))),
((,), (lambda x: acetylideAdd(x, o))) )

    
    
"h2 PD C"

#List of synonyms of reagents.
#The first value in the tuple is how it should be printed (with proper subscripts).
#The second value in the tuple is what items should be recognizable as user input.
REAGENTS = {
H2: ("H<sub>2</sub>",["H2", "Hydrogen"]),
PDC: ("Pd|C", ["PdC", "Pd/C", "Pd|C", "Pd C", "palladium"]),
ETOH: ("EtOH", ["EtOH", "Ethanol", "Ethyl alcohol", "C2H5OH"]),
HF: ("HF", ["HF", "Hydrogen fluoride", "Hydrofluoric acid"]),
HBR: ("HBr", ["HBr", "Hydrogen bromide", "Hydrobromic acid"]),
HCL: ("HCl", ["HCl", "Hydrogen chloride", "Hydrochloric acid"]),
HI: ("HI", ["HI", "Hydrogen iodide", "Hydroiodic acid"]),
CH2CL2: ("CH<sub>2</sub>Cl<sub>2</sub>", ["CH2Cl2", "Dichloromethane"]),
F2: ("F<sub>2</sub>", ["Fluorine", "F2"]),
BR2: ("Br<sub>2</sub>", ["Bromine", "Br2"]),
CL2: ("Cl<sub>2</sub>", ["Chlorine", "Cl2"]),
I2: ("I<sub>2</sub>", ["Iodine", "I2"]),
ROOR: ("ROOR", ["ROOR", "tBuOOtBu", "Peroxide", "Tert-butyl peroxide", "Di-tert-butyl peroxide"]),
RCO3H: ("RCO3H",["mCPBA", "PhCO3H", "RCO3H"]),
H2SO4: ("H<sub>2</sub>SO<sub>4</sub>", ["H2SO4", "Sulfuric acid"]),
H2O: ("H<sub>2</sub>O", ["H2O", "Water", "Dihydrogen monoxide", "HOH"]),
HGSO4: ("HgSO<sub>4</sub> accels.", ["HgSO4", "Hg2+", "Mercury sulfate"]),
BH3: ("BH<sub>3</sub>", ["BH3", "Borane"]),
THF: ("THF", ["THF", "Tetrahydrofuran"]),
NAOH: ("NaOH", ["NaOH", "Sodium hydroxide", "Hydroxide"]),
H2O2: ("H<sub>2</sub>O<sub>2</sub>", ["H2O2", "Hydrogen peroxide"]),
OSO4: ("OsO<sub>4</sub>", ["oso4", "osmium tetroxide", "osmium oxide"]),
NMO: ("NMO", ["NMO", "NMMO", "N-Methylmorpholine N-oxide"]),
ACETONE: ("Acetone", ["Acetone", "Propanone", "(CH3)2CO"]),
O3: ["O<sub>3</sub>", ["Ozone", "O3"]],
ME2S: ["Me<sub>2</sub>S", ["Dimethyl sulfide", "Methylthiomethane", "Me2S"]],
ZN: ["Zn", ["Zn", "Zinc"]],
LINDLAR: ["cat. Lindlar", ["cat Lindlar", "cat. Lindlar", "Lindlar", "Lindlar catalyst"]],
NA: ["Na", ["Sodium", "Na"]],
NH3: ["NH<sub>3 (L)</sub>", ["NH3", "Ammonia", "Anhydrous ammonia"]],
NANH2: ["NaNH<sub>2</sub>", ["Sodium amide", "Sodamide", "NaNH2", "Amide"]] 
EQV1: ["1 equiv.", ["1 eq", "one eq"]]
HEAT: ["Heat", ["heat", "delta", "hot", "warm"]]
LIGHT: ["Light", ["hv", "light", "bright", "h nu", "hnu"]]
}


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

