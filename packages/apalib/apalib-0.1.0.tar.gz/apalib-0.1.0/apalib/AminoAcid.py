import sys
import apalib.config as config
import apalib.apalibExceptions as apaExcept
from apalib.Data import data as data
from apalib.Residue import Residue

global FLAGS
FLAGS = {}

class AminoAcid(Residue):
    def __init__(self, seqNum = None, atoms = None, resName = None, rotamer = None, vector = None, set_name = True,
                 heptad = None, centroid = None, chainID=None):
        self.rotamer = rotamer
        self.vector = vector
        self.heptad = heptad
        self.centroid = centroid
        self.SetResName(resName)
        super().__init__(seqNum, atoms, chainID)

    # def DeepCopy(self):
    #     return AminoAcid(number=self.seqNum,
    #                      atoms=self.atoms,
    #                      name=self.resName,
    #                      rotamer=self.rotamer,
    #                      vector=self.vector,
    #                      heptad=self.heptad,
    #                      centroid=self.centroid,
    #                      chainID=self.chainID,
    #                      set_name=True)

    def CalculateCentroid(self):
        super()._CalculateCentroid('Amino Acids')

    def GetRotamers(self, **kwargs):
        accepted = ['unique']
        for key in kwargs.keys():
            if key not in accepted:
                raise apalib.apalibExceptions.BadKwarg(accepted)

        if self.rotamer is not None:
            return self.rotamer

        if 'unique' in kwargs.keys() and isinstance(kwargs['unique'], (bool)):
            unique = kwargs['unique']
        else:
            unique = False

        retDict = {'Common':[]}
        if self.atoms is not None:
            for atom in self.atoms:
                if atom.rotation is None or atom.rotation == '':
                    retDict['Common'].append(atom)
                    continue
                if atom.rotation not in retDict.keys():
                    retDict[atom.rotation] = []
                retDict[atom.rotation].append(atom)
        if unique is False:
            for lst in [retDict[key] for key in retDict.keys() if key != 'Common']:
                lst += retDict['Common']
        return retDict

    def GetBaseAtom(self):
        if self.atoms is None:
            return None
        for atom in self.atoms:
            if atom.GetName() == 'CA':
                return atom
        for atom in self.atoms:
            if atom.GetName() == "C":
                return atom
        return self.atoms[0]

    #TODO This feels super messy. There is very likely a cleaner way to do this
    def SetResName(self, name):
        if name is None:
            self.resName = name
            return
        if len(name) == 3 and self.MapResidue(name) is not None:
            self.resName = name
        elif len(name) == 3 and self.MapResidue(name) is not None:
            self.resName = None
        elif len(name) == 1:
            self.resName = self.Get1Code(name)
        elif len(name) <= 4:
            if  self.MapResidue(name[-3:]) is not None:
                self.resName = name[-3:]
                self.rotamer = name[:-3]
            else:
                self.resName = None
        elif len(name) == 2:
            self.resName = None

    def SetHeptad(self, heptad):
        self.heptad = heptad

    def GetASA(self, form):
        d = config.data
        name = config.data.Map("Amino Acids", config.data.Standardize(self.resName))
        return config.data.GetJson()["Amino Acids"][name]["ASA"][form]

    def _GetType(self):
        return "AA"

    def _BaseObject(self):
        return AminoAcid()

    def Set_str(self, str):
        return
