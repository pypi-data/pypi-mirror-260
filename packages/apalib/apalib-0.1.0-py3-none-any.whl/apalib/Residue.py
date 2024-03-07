import copy
import sys
from abc import ABC, abstractmethod
from apalib.Atom import Atom
from apalib.apalibExceptions import BadKwarg
import random

from apalib.Data import data as data

class Residue(ABC):
    #TODO Defined/custom centroid domain
    #TODO Flags
    def __init__(self, seqNum=None, atoms=None, chainID=None):
        # self.SetResName(resName)
        self.SetSeqNum(seqNum)
        self.SetAtoms(atoms)
        self.SetChainID(chainID)
        self.FullName = None
        self.UseDefaultBase = True
        self.centroid_domain = None

    def Copy(self):
        return copy.deepcopy(self)
        # newResidue = self._BaseObject()
        # for var in self.__dict__:
        #     newResidue.__dict__[var] = self.__dict__[var]
        # #Decouple the atoms list in the copied residue
        # newAtoms = []
        # for atom in self.GetAtoms():
        #     newAtoms.append(atom.Copy())
        # newResidue.SetAtoms(newAtoms)
        # return newResidue

    def AddAttribute(self, attr, var):
        self.__dict__[attr] = var

    def SetSeqNum(self, num):
        self.seqNum = num

    def GetSeqNum(self):
        return self.seqNum

    def SetAtoms(self, atoms):
        self.atoms = atoms

    def InsertAtom(self, atom):
        if self.atoms is None:
            self.atoms = list()
        self.atoms.append(atom)

    def GetAtoms(self):
        return self.atoms

    def WriteForPDB(self):
        retstr = ""
        for atom in self.atoms:
            retstr += atom.WritePDB(intro="ATOM  ")
        return retstr

    def _CalculateCentroid(self, resType):
        self.centroid = None
        if 'atoms' not in self.__dict__:
            return
        residue = data.Map(resType, self.resName)

        if residue in data.GetJson()[resType].keys():
            # If residue is not specified
            x_coord = 0
            y_coord = 0
            z_coord = 0
            num_atoms = 0
            for atom in [atom for atom in self.atoms if
                         atom.name in data.GetJson()[resType][residue]['Centroid']]:
                if atom.element == 'H':
                    continue
                x_coord += atom.GetCoordinates()[0]
                y_coord += atom.GetCoordinates()[1]
                z_coord += atom.GetCoordinates()[2]
                num_atoms += 1
            self.centroid = list()
            try:
                self.centroid.append(x_coord / num_atoms)
                self.centroid.append(y_coord / num_atoms)
                self.centroid.append(z_coord / num_atoms)
            except ZeroDivisionError:
                self.centroid.clear()
                beta = [atom for atom in self.atoms if atom.name == 'CB']
                alpha = [atom for atom in self.atoms if atom.name == 'CA']
                if len(beta) != 0:
                    self.centroid.append(beta[0].coordinates[0])
                    self.centroid.append(beta[0].coordinates[1])
                    self.centroid.append(beta[0].coordinates[2])
                    # self.RaiseFlag('B_CENTROID')
                elif len(alpha) != 0:
                    self.centroid.append(alpha[0].coordinates[0])
                    self.centroid.append(alpha[0].coordinates[1])
                    self.centroid.append(alpha[0].coordinates[2])
                    # self.RaiseFlag('A_CENTROID')
                else:
                    self.centroid = None
                    self.vector = None
                    # self.RaiseFlag('BAD_CENTROID')
                    return
            # After all that, set the centroidal vector
            # print(self.GetBaseAtom())
            if self.GetBaseAtom() is not None:
                self.vector = [self.centroid[0] - self.GetBaseAtom().GetCoordinates()[0],
                               self.centroid[1] - self.GetBaseAtom().GetCoordinates()[1],
                               self.centroid[2] - self.GetBaseAtom().GetCoordinates()[2]]
            else:
                self.vector = None

        elif len(self.resName) == 4 and self.resName[1:] in data.GetJson()[resType][residue]['Centroid']:
            sys.stderr.write("ROTAMER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            sys.exit(f"An unknown residue was found: {self.resName}")

    # def SetCentroidAtom(self, atom):
    #     if atom is None:
    #         self.CentroidAtom = None
    #     self.CentroidAtom = atom

    def DefineCentroid(self, atoms):
        self.centroid_domain = atoms

    def GetCentroid(self):
        return self.centroid

    def GetCentroidAtom(self):
        return Atom(resSeq=self.seqNum, resName=self.resName, serial=" ", element="CENT", name="CENT", x=self.x, y=self.y, z=self.y)

    def GetVector(self):
        return self.vector

    def SetChainID(self, c):
        self.chainID = c

    def MapResidue(self, residue):
        return data.MapResidue(residue, self._GetType())

    def Get1Code(self, residue):
        return data.Get1Code(residue, self._GetType())

    def GetNeighborhood(self, potential_neighborhood, distance=30, compare="Centroid"):
        compare = compare.upper()
        neighborhood=[]
        try:
            for residue in potential_neighborhood:
                if compare == "BASE":
                    a1 = residue.GetBaseAtom()
                    a2 = self.GetBaseAtom()
                elif compare == "CENTROID":
                    a1 = residue.GetCentroid(as_atom=True)
                    a2 = self.GetCentroid(as_atom=True)
                elif compare == "RANDOM":
                    a1 = random.choice(residue.GetAtoms())
                    a2 = random.choice(self.GetAtoms())
                if a1.GetDistance(a2) < distance:
                    neighborhood.append(residue)
        except:
            #TODO Handle this
            print("No neighborhood found")
        return neighborhood
        #for residue in potential_neighborhood

    def __iter__(self):
        return iter(self.atoms)

    def __lt__(self, other):
        return self.seqNum < other.number

    def __repr__(self):
        # return f"RESIDUE: {data.MapResidue(self.resName)}, NUMBER: {self.seqNum}"
        return f"{self.resName} {self.seqNum}"

    def __str__(self):
        # return f"{data.MapResidue(self.resName)} {self.seqNum}"
        return f"{self.resName} {self.seqNum}"

    @abstractmethod
    def _GetType(self):
        pass

    @abstractmethod
    def GetBaseAtom(self):
        pass

    @abstractmethod
    def SetResName(self, name):
        pass

    @abstractmethod
    def CalculateCentroid(self):
        pass

    @abstractmethod
    def _BaseObject(self):
        pass