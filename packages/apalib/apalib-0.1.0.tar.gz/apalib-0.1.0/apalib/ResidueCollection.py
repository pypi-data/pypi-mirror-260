import copy

from apalib.Residue import Residue

class ResidueCollection():
    def __init__(self, collection=None):
        if collection is None:
            collection = {}
        self._collection = collection
        self.AllowClash = False

    def Copy(self):
        return copy.deepcopy(self)
        # newCollection = ResidueCollection()
        # for var in self.__dict__:
        #     newCollection.__dict__[var] = self.__dict__[var]
        # #Decouple the dictionary
        # newCollection._collection = {}
        # for key in self.keys():
        #     newCollection[key] = self[key].Copy()
        # return newCollection

    def SetClashAllowance(self, allow):
        self.AllowClash = allow

    def keys(self, asList=False):
        if asList:
            return list(self._collection.keys())
        return self._collection.keys()

    def values(self, asList=False):
        if asList:
            return list(self._collection.values())
        return self._collection.values()

    def GetCollection(self):
        return self._collection

    def AddResidue(self, residue, index):
        self._collection[index] = residue

    def __iter__(self):
        return self._collection.values().__iter__()

    def __getitem__(self, key):
        return self._collection[key]

    def __setitem__(self, key, value):
        self._collection[key] = value

    def __delitem__(self, key):
        del self._collection[key]

    def __add__(self, other):
        if isinstance(other, ResidueCollection):
            newCollection = ResidueCollection()
            for k, v in  self._collection.items():
                newCollection[f"{k}_1"] = v
            for k, v in other.GetCollection().items():
                newCollection[f"{k}_2"] = v
            return newCollection
        #TODO this needs to be tested
        elif isinstance(other, Residue):
            if self.AllowClash:
                self._collection[other.GetSeqNum()] = other
            elif str(other.GetSeqNum()) not in self._collection.keys():
                self._collection[other.GetSeqNum()] = other
