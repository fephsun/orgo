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
                carbon.newChiralCenter(neighbor, (None, carbon.CTb, carbon.CTa))
                neighbor.newChiralCenter(carbon, (None, neighbor.CTa, neighbor.CTb))
                carbon.eliminateCT()
                neighbor.eliminateCT()
    return molecule

