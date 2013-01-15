#Synthesis problem class
    #List of starting materials
    #List of molecules in final outcome
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
    def __init__(self, parentMoleculeBox, reagentList):
        self.reactant = parentMoleculeBox
        self.reagentList = reagentList
        self.otherMolecules = []
        self.product = None

    def addReagents(reagentList):
        self.reagentList += reagentList

    def 


#MoleculeBox class
    #List of molecules contained in it
class MoleculeBox:
    def __init__(self, moleculesList):
        self.molecules = moleculesList

#ReagentBox class
    #List of reagents (as strings) contained in it
class ReagentBox:
    def __init__(self, reagentsList):
        self.reagents = reagentsList

def randomSynthesisProblemMake():



#Returns a new MoleculeBox if the reaction step has the proper reagents to produce one of the standard reactions.
def getProduct(reactionStep):
    



H2 = ("H<sub>2</sub>",["h2", "hydrogen"])
PDC = ("Pd|C", ["pdc", "pd/c", "pd|c", "palladium and carbon", "palladium on carbon", "palladium carbon", "carbon and palladium", "carbon on palladium", "carbon palladium"])
ETOH = ("EtOH", ["etoh", "ethanol", "ethyl alcohol", "c2h5oh"])
HF = ("HF", ["hf", "hydrogen fluoride", "hydrofluoric acid"])
HBR = ("HBr", ["hbr", "hydrogen bromide", "hydrobromic acid"])
HCL = ("HCl", ["hcl", "hydrogen chloride", "hydrochloric acid"])
HI = ("HI", ["hi", "hydrogen iodide", "hydroiodic acid"])
CH2CL2 = ("CH<sub>2</sub>Cl<sub>2</sub>", ["ch2cl2", "dichloromethane"])
F2 = ("F<sub>2</sub>", ["fluorine", "f2"])
BR2 = ("Br<sub>2</sub>", ["bromine", "br2"])
CL2 = ("Cl<sub>2</sub>", ["chlorine", "cl2"])
I2 = ("I<sub>2</sub>", ["iodine", "i2"])
ROOR = ("ROOR", ["roor", "hooh", "rooh", "tbuootbu", "peroxide", "tert-butyl peroxide", "di-tert-butyl peroxide"])
RCO3H = ("RCO3H",["mCPBA", "PhCO3H", "RCO3H"])
H2SO4
