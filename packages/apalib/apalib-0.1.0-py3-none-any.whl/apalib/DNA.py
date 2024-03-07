from apalib.Data import data as data
from apalib.Residue import Residue


class DNA(Residue):

    def __init__(self, seqNum=None, atoms=None, resName=None, set_name=True, chainID=None):
        super().__init__(seqNum, atoms, chainID)
        self.SetResName(resName)

    # def DeepCopy(self):
    #     return DNA(seqNum=self.seqNum,
    #                atoms=self.atoms,
    #                resName=self.resName,
    #                set_name=True)

    def CalculateCentroid(self):
        super()._CalculateCentroid("DNA Nucleotides")

    def GetBaseAtom(self):
        if self.atoms is None:
            return None
        for atom in self.atoms:
            if 'C1' in atom.GetName():
                return atom
        return None

    def _GetType(self):
        return "DNA"

    def InsertAtom(self, atom):
        if self.atoms is None:
            self.atoms = list()
        self.atoms.append(atom)

    def SetResName(self, name):
        if data.ValidateDNA(name):
            self.resName = data.SetDNAName(name)
        return

    def GetResName(self):
        return self.resName

    def _BaseObject(self):
        return DNA()
