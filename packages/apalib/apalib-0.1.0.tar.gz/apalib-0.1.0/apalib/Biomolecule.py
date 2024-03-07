import numpy as np
import apalib.Atom
class Biomolecule():
    def __init__(self, chains = None):
        self._symmetries = {}
        self.chains = chains

    def AddSymmetry(self, symmetry, id=None):
        if id is None:
            id = len(self._symmetries)
            while id in self._symmetries.keys():
                id += 1
        self._symmetries[id] = np.array(symmetry)

    def GetSymmetryMatrix(self):
        return self._symmetries

    def GenerateSymmetricCollection(self, collection, matrix_numbers=None):
        if isinstance(matrix_numbers, int):
            matrix_numbers = list(matrix_numbers)
        elif matrix_numbers is None:
            matrix_numbers = self._symmetries.keys()

        symmetry_pairs = []
        for i in matrix_numbers:
            symmetric_collection = collection.Copy()
            for residue in symmetric_collection:
                for atom in residue:
                    xyz = np.array([atom.x, atom.y, atom.z, 1])
                    newCoord = np.matmul(self._symmetries[i], xyz)
                    atom.SetXYZ(newCoord[0], newCoord[1], newCoord[2])
                residue.CalculateCentroid()
            symmetry_pairs.append(symmetric_collection)
        return symmetry_pairs
