from orgoStructure import *

def hydrogenate(molecule):
    for carbon in molecule.atoms:
        if carbon.element != 'C':
            continue
        for neighbor in carbon.neighbors:
            if neighbor.element == 'C' and carbon.neighbors[neighbor] == 2:
                #Set bond orders
                carbon.neighbors[neighbor] = 1
                neighbor.neighbors[carbon] = 1
                if carbon.CTb != None and carbon.CTa != None:
                    carbon.newChiralCenter(neighbor, (None, carbon.CTb, carbon.CTa))
                if neighbor.CTb != None and neighbor.CTa != None:
                    neighbor.newChiralCenter(carbon, (None, neighbor.CTa, neighbor.CTb))
                carbon.eliminateCT()
                neighbor.eliminateCT()
    return molecule

mol2 = hydrogenate(mol)
print smiles(mol2)
