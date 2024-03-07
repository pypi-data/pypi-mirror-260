# global FULL_NAME
# global ONE_LETTER
import sys
from apalib.Data import data as data
from apalib.Residue import Residue

global FLAGS
FLAGS = {}


class RNA(Residue):
    def __init__(self, seqNum=None, atoms=None, resName=None, set_name=True, chainID=None):
        super().__init__(seqNum, atoms, chainID)
        self.SetResName(resName)

    # def DeepCopy(self):
    #     return RNA(seqNum=self.seqNum,
    #                atoms=self.atoms,
    #                resName=self.resName,
    #                set_name=True)

    def CalculateCentroid(self):
        super()._CalculateCentroid("RNA Nucleotides")

    def SetResName(self, name):
        if data.ValidateRNA(name):
            self.resName = data.SetRNAName(name)
        return

    def GetResName(self):
        return self.resName

    def GetBaseAtom(self):
        if self.atoms is None:
            return None
        for atom in self.atoms:
            if 'C1' in atom.GetName():
                return atom
        return None

    def _BaseObject(self):
        return RNA()

    def _GetType(self):
        return "RNA"
