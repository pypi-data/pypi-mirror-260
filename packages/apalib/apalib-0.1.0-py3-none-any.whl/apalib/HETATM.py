import apalib.config
from apalib.Data import data as data
from apalib.Residue import Residue

global FLAGS
FLAGS = {}

class HETATM(Residue):
    def __init__(self, seqNum=None, atoms=None, resName=None, chainID=None):
        self.SetResName(resName)
        self.SetSeqNum(seqNum)
        self.SetAtoms(atoms)
        self.SetChainID(chainID)

    # def DeepCopy(self):
    #     return HETATM(seqNum=self.seqNum,
    #                   atoms=self.atoms,
    #                   resName=self.resName)

    def AddAttribute(self, attr, var):
        self.__dict__[attr] = var

    def SetSeqNum(self, num):
        self.seqNum = num

    def GetAtoms(self):
        return self.atoms

    def SetAtoms(self, atoms):
        self.atoms = atoms
        # self.CalculateCentroid()

    def InsertAtom(self, atom):
        if self.atoms is None:
            self.atoms = list()
        self.atoms.append(atom)

    def SetResName(self, resName):
        self.resName = resName

    def GetResName(self):
        return self.resName

    def ClearFlags(self):
        self.flags.clear()

    def GetType(self):
        return "HETATM"

    def CalculateCentroid(self):
        if 'atoms' not in self.__dict__:
            self.centroid = None
            return
        n = 0
        x = 0
        y = 0
        z = 0
        for atom in self.atoms:
            n += 1
            x += atom.GetCoordinates()[0]
            y += atom.GetCoordinates()[1]
            z += atom.GetCoordinates()[2]
        self.centroid = [x/n, y/n, z/n]


    # def SetCentroidAtom(self, atom):
    #     self.CentroidAtom = atom
    #
    # def GetCentroid(self, as_atom=True):
    #     if as_atom:
    #         return
    #     return self.centroid

    # def GetCentroid(self):
    #     if 'centroid' in self.__dict__:
    #         return self.centroid
    #     return None

    def SetChainID(self, c):
        self.chainID = c

    def WriteForPDB(self):
        retstr = ""
        for atom in self.atoms:
            retstr += atom.WritePDB(intro="HETATM")
        return retstr

    def _GetType(self):
        return "HETATM"

    def SpecifyBaseAtom(self, ID):
        for atom in self.atoms:
            if atom.GetName() == ID:
                self.base = atom
                return
        raise apalib.apalibExceptions.AtomIDNotFound(f"An atom with the \"{ID}\" identifier was not found.")

    #Return the first atom provided if no base was specified
    def GetBaseAtom(self):
        if self.atoms is None:
            return None
        if "base" in self.__dict__:
            return self.base
        return self.atoms[0]

    def _BaseObject(self):
        return HETATM()

    @staticmethod
    def CheckFlag(f):
        global FLAGS
        if f in FLAGS:
            return FLAGS[f]
        return False

    @staticmethod
    def RaiseFlag(flag):
        global FLAGS
        FLAGS[flag] = True

    @staticmethod
    def ClearFlag(flag):
        global FLAGS
        FLAGS[flag] = False

    def __lt__(self, other):
        return self.seqNum < other.seqNum

    # def __repr__(self):
    #     return f"RESIDUE: {self.resName}, seqNum: {self.seqNum}"
    #
    # def __str__(self):
    #     return f"{self.resName} {self.seqNum}"
