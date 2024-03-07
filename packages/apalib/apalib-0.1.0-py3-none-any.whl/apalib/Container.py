from apalib.AminoAcid import AminoAcid
from apalib.Atom import Atom
from apalib.DNA import DNA
from apalib.RNA import RNA
from apalib.HETATM import HETATM
from apalib.ResidueCollection import ResidueCollection
from apalib.Biomolecule import Biomolecule
import sys
from apalib.Data import data as data

class Container:
    def __init__(self):
        self.current_fetch = None
        self.Chains = {}
        self.PeptideChains = None
        self.DNAChains = None
        self.RNAChains = None
        self.HETATMChains = None
        self.Populated = False
        self.Symmetry = {}

    def ClearAll(self, initialize = True):
        self.__init__()
        if initialize:
            self.Chains = {}
            self.HETATMChains = {}
            self.PeptideChains = {}
            self.DNAChains = {}
            self.RNAChains = {}

    def AddChain(self, key):
        self.Chains[key] = ResidueCollection()
        self.HETATMChains[key] = {}
        self.PeptideChains[key] = {}
        self.DNAChains[key] = {}
        self.RNAChains[key] = {}

    def PopulateResidueGroups(self, force_populate = False):
        if self.Populated and force_populate == False:
            return
        self.HETATMChains = {}
        self.PeptideChains = {}
        self.DNAChains = {}
        self.RNAChains = {}
        for key in self.Chains:
            self.HETATMChains[key] = {}
            self.PeptideChains[key] = {}
            self.DNAChains[key] = {}
            self.RNAChains[key] = {}
            for index in self.Chains[key].keys():
                if isinstance(self.Chains[key][index], AminoAcid):
                    self.PeptideChains[key][index] = self.Chains[key][index]
                elif isinstance(self.Chains[key][index], HETATM):
                    self.HETATMChains[key][index] = self.Chains[key][index]
                elif isinstance(self.Chains[key][index], RNA):
                    self.RNAChains[key][index] = self.Chains[key][index]
                elif isinstance(self.Chains[key][index], DNA):
                    self.DNAChains[key][index] = self.Chains[key][index]
        self.Populated = True

    #Create a new residue if missing. Otherwise return the designated residue
    def AddResidue(self, resType, index, resName, chainID):
        if chainID not in self.Chains.keys():
            self.AddChain(chainID)
        index = int(index.strip())
        if index in self.Chains[chainID].keys():
            return self.Chains[chainID][index]

        if resType == "HETATM":
            residue = HETATM(seqNum=index, resName=resName, chainID=chainID)
        elif resType == "RNA":
            residue = RNA(seqNum=index, resName=resName, chainID=chainID)
        elif resType == "DNA":
            residue = DNA(seqNum=index, resName=resName, chainID=chainID)
        elif resType == "AA":
            residue = AminoAcid(seqNum=index, resName=resName, chainID=chainID)
        else: #This should raise an exception
            sys.stderr.write("Something went wrong in adding a residue")
            return
        self.Chains[chainID][index] = residue
        return residue

    def GetChain(self, chain):
        return self.Chains[chain]

    def SetFetch(self, fetch):
        self.current_fetch = fetch

    def GetFetch(self):
        return self.current_fetch

    def ClearFetch(self):
        self.current_fetch = None

    def SetProteinChains(self, pchain):
        self.PeptideChains = pchain

    def GetPeptideChains(self):
        return self.PeptideChains

    def ClearPeptideChains(self):
        self.PeptideChains = None

    def SetDNAChains(self,dchain):
        self.DNAChains = dchain

    def GetDNAChains(self):
        return self.DNAChains

    def ClearDNAChains(self):
        self.DNAChains = None

    def GetRNAChains(self):
        return self.RNAChains

    def SetRNAChains(self, rchain):
        self.RNAChains = rchain

    def ClearRNAChains(self):
        self.RNAChains = None

    def GetHETATMChains(self):
        return self.HETATMChains

    def SetHETATMChains(self, hchain):
        self.HETATMChains = hchain

    def ClearHEETATMChains(self):
        self.HETATMChains = None

    def _AddSymmetry(self, symmetry_groups):
        for sg in symmetry_groups:
            symmetry = Biomolecule(sg['chains'])
            for key in sg.keys():
                if key == 'chains':
                    continue
                symmetry.AddSymmetry(sg[key], key)
            self.Symmetry[len(self.Symmetry.keys())] = symmetry
        print("stop")

    def GetSymmetry(self, key=None):
        if key is None:
            return self.Symmetry
        return self.Symmetry[key]


            #Perform calculations, etc. to be done after a full parse
    def _PostParseEvaluations(self):
        #Fill in variables
        for chain in self.Chains.keys():
            for res in self.Chains[chain].values():
                res.CalculateCentroid()
                coords = res.GetCentroid()
                # if res.centroid is not None:
                #     res.SetCentroidAtom(Atom(resSeq=res.seqNum, resName=res.resName, serial=" ", element="CENT", name="CENT", x=coords[0], y=coords[1], z=coords[2]))
        # for chain in self.PeptideChains.keys():
        #     for res in self.PeptideChains[chain].values():
        #         res.CalculateCentroid()
        # for chain in self.DNAChains.keys():
        #     for res in self.DNAChains[chain].values():
        #         res.CalculateCentroid()
        # for chain in self.RNAChains.keys():
        #     for res in self.RNAChains[chain].values():
        #         res.CalculateCentroid()

    def DumpResidues(self):
        flat_list = [res for reslist in [list(self.Chains[chain].values()) for chain in self.Chains] for res in reslist]
        return flat_list
        # return [list(self.Chains[chain].values()) for chain in self.Chains][0]

    def DumpAtoms(self):
        return [atom for group in [residue.GetAtoms() for residue in [list(self.Chains[chain].values()) for chain in self.Chains][0]] for atom in group]


#Keeping these two functions commented and not deleted because I'm proud of my unreadable list comprehension
#___________________________________________________________________
    #Returns all residues from all children of CONTAINER as a list
    #Nasty list comprehension goes faster than a for-loop
    # def DumpResidues(self):
    #     return [val for sublist in (list(res.values()) for res in list(self.PeptideChains.values()) + list(self.HETATMChains.values()) + list(self.DNAChains.values()) + list(self.RNAChains.values())) for val in sublist]
        # lst =  list(self.PeptideChains.values()) + list(self.HETATMChains.values()) + list(self.DNAChains.values()) + list(self.RNAChains.values())
        # retlst = []
        # for d in lst:
        #     retlst += list(d.values())
        # return retlst

    #Return all atoms from all children of CONTAINER as a list
    #Virtually human-unreadable, but its efficient and pythonic
    # def DumpAtoms(self):
    #     return [atom for sublist in (group.GetAtoms() for group in (val for sublist in (list(res.values()) for res in list(self.PeptideChains.values()) + list(self.HETATMChains.values()) + list(self.DNAChains.values()) + list(self.RNAChains.values())) for val in sublist)) for atom in sublist]
        # return [atom for sublist in (group.GetAtoms() for group in self.DumpResidues()) for atom in sublist]
# ___________________________________________________________________

    #Return all residues from all chains as a single list
    # def AsList(self, ordered=True):
    #     fullLst = []
    #     retLst = []
    #     lst = [self.PeptideChains, self.DNAChains, self.RNAChains, self.HETATMChains]
    #     for val in lst:
    #         if val is not None and len(val.keys()) != 0:
    #             fullLst = fullLst + list(val.values())
    #     for val in fullLst:
    #         retLst = retLst + list(val.values())
    #     return sorted(retLst, key=lambda val : val.seqNum) if ordered else retLst