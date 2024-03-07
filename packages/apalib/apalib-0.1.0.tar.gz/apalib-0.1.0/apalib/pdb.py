from apalib.apalibExceptions import BadNameException
from apalib.Atom import Atom
from apalib.HETATM import *
from apalib.AminoAcid import *
import sys
from apalib import *
from apalib.Data import data as data

class PDB:
    def __init__(self):
        self.container = Container()
        # print(apalib.j_data.GetJson())

    def Contents(self):
        return self.container

    def FetchFASTA(self, prot):
        import urllib.request
        url = r"https://www.rcsb.org/fasta/entry/" + prot.strip().upper() + r"/display"
        try:
            with urllib.request.urlopen(url) as f:
                return f.read().decode('utf-8')
        except urllib.error.URLError:
            sys.stderr.write("The requested pdb code could not be retrieved or does not exist\n")
            return False

    # def FetchAsFile(self, prot):
    #     import urllib.request
    #     url = r'https://files.rcsb.org/download/' + prot.strip() + '.pdb'
    #     try:
    #         with urllib.request.urlopen(url) as f:

    #Enabling bad behavior
    def fetch(self, prot, crash=True, hold_pdb=False):
        return self.Fetch(prot, crash, hold_pdb)
    def Fetch(self, prot, crash = True, hold_pdb=False):
        # print("Fetching ", prot)
        import urllib.request
        url = r'https://files.rcsb.org/download/' + prot.strip() + '.pdb'
        try:
            with urllib.request.urlopen(url) as f:
                self.container.SetFetch(f.read().decode('utf-8'))
                self._Parse(hold_pdb)
                return True
        except urllib.error.URLError:
            sys.stderr.write("The requested pdb code could not be retrieved or does not exist\n")
            if crash:
                exit()
            return False

    def Read(self, path, hold_pdb=False):
        with open(path, 'r') as fp:
            self.container.SetFetch(fp.read())
            self._Parse(hold_pdb)

    # Wrapper for the ParsePDB file to allow functionality with a fetched protein
    def _Parse(self, hold_pdb=False):
        try:
            if self.container.GetFetch() is None:
                raise apaExcept.NoFetchError
            return self._ParsePDB(self.container.GetFetch(), hold_pdb)
            # return self._ParsePDB(self.container.GetFetch().splitlines())
        except apaExcept.NoFetchError as e:
            sys.stderr.write(e.message)


    #PDB standard described here: https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html
    def _ParsePDB(self, raw_pdb, hold_pdb=False):
        self.container.ClearAll()
        remark350 = ""
        if hold_pdb:
            self.container.SetFetch(raw_pdb)
        for line in raw_pdb.splitlines():
            # print(line)
            if line[0:6] == 'ATOM  ' or line[0:6] == 'HETATM':
                self._ExtractAtomAndResidue(line)
            if line.find("REMARK 350") != -1:
                remark350 += line + "\n"

        symmetry_groups = self._ParseRemark350(remark350)
        self.container._AddSymmetry(symmetry_groups)
        self.container._PostParseEvaluations()
    def _ParseRemark350(self, remark350):
        lines = remark350.splitlines()
        lines.append("END")
        symFlag = False
        biomolecules = []
        for line in lines:
            if 'REMARK 350 APPLY' in line and ":" in line and symFlag is False:
                symFlag = True
                symLines = []
                chains = line[line.find(":")+1:].replace(",", " ").split()
            elif 'REMARK 350 APPLY' in line and ":" in line and symFlag is True:
                chains += line[line.find(":")+1:].replace(",", " ").split() #This feels dangerous
            elif 'AND CHAINS:' in line and symFlag is True:
                chains += line[line.find(":") + 1:].replace(",", " ").split() #This also feels dangerous
            elif 'BIOMT' in line and symFlag:
                BIOMT = line[13:19].strip()
                id = line[19:23].strip()
                x = line[23:33].strip()
                y = line[33:43].strip()
                z = line[43:53].strip()
                m = line[53:].strip()
                symLines.append([BIOMT, int(id), float(x), float(y), float(z) ,float(m)])
            elif symFlag:
                symFlag = False
                biomolecule = {}
                biomolecule['chains'] = chains
                for sl in symLines:
                    if sl[1] not in biomolecule.keys():
                        biomolecule[sl[1]] = []
                    biomolecule[sl[1]].append([sl[0]] + sl[2:])
                biomolecules.append(biomolecule)
            #I hate PDB file format
        for i in range(len(biomolecules)):
            biomolecule = biomolecules[i]
            for key in biomolecule.keys():
                biomolecule[key].sort(key=lambda x:x[0])
                for i in range(len(biomolecule[key])):
                    if key == "chains":
                        continue
                    biomolecule[key][i].pop(0)
        return biomolecules

    def _ExtractAtomAndResidue(self, line):
        serial = line[6:11].strip()
        name = line[12:16].strip()
        altLoc = line[16].strip()
        resName = line[17:20].strip()
        chainID = line[21].strip()
        resSeq = line[22:26].strip()
        iCode = line[26].strip()
        x = line[30:38].strip()
        y = line[38:46].strip()
        z = line[46:54].strip()
        occupancy = line[54:60].strip()
        tempFactor = line[60:66].strip()
        element = line[76:78].strip()
        charge = line[78:80].strip()
        atom = Atom.Atom(serial=serial, name=name, altLoc=altLoc, resName=resName, chainID=chainID, resSeq=resSeq,
                         iCode=iCode, x=float(x), y=float(y), z=float(z), occupancy=occupancy, tempFactor=tempFactor, element=element,
                         charge=charge)
        if "HETATM" in line:
            resType = "HETATM"
        else:
            resType = self.DetermineResType(resName)
        residue = self.container.AddResidue(resType, resSeq, resName, chainID)
        residue.InsertAtom(atom)

    def DetermineResType(self, resName):
        if data.ValidateRNA(resName):
            return 'RNA'
        elif data.ValidateDNA(resName):
            return 'DNA'
        elif data.ValidateAA(resName):
            return "AA"
        else:
            return "HETATM"

    #Remove all of the waters from the current fetch. Probably make this more general for any HETATM group. Make a wrapper?
    def RemoveWater(self):
        h_chains = self.container.GetHETATMChains()
        for chain in h_chains.keys():
            h_chains[chain] = {key: value for (key, value) in h_chains[chain].items() if value.GetResName().upper() != 'HOH'}

    # def Validate(self, **kwargs):
    #     for key in kwargs:
    #         if key != 'pdb' or (key == 'pdb' and not isinstance(kwargs['pdb'], str)):
    #             raise apalib.apalibExceptions.BadKwarg('pdb=<pdb_to_validate>')

    #Write contents to a PDB file

    def AddChain(self, collection, name=None):
        if name is None:
            chains = list(self.container.Chains.keys())
            for i in range(26):
                if chr(ord('z') - i) not in chains:
                    name = chr(ord('z') - i)
                    break
        else:
            if len(name) > 1 or not name.isalnum():
                raise BadNameException("A chain must be a single-character alphanumeric input")
        #Rechain all of the atoms and residues with new name
        for residue in collection:
            residue.SetChainID(name)
            for atom in residue.GetAtoms():
                atom.SetChainID(name)
        self.container.AddChain(name)
        self.container.Chains[name] = collection

    def WritePDB(self, fp):
        s = sorted(self.container.DumpResidues(), key=lambda x: x.seqNum)
        with open(fp, "w") as f:
            for res in s:
                f.write(res.WriteForPDB())

    #Write contents to FASTA
    def ToFASTA(self):
        ls = self.container.AsList(ordered=True)
        retStr = ""
        for r in ls:
            if data.ValidateAA(r.resName):
                name = data.Map("Amino Acids", r.resName)
                retStr += data.GetJson()["Amino Acids"][name]["1code"]
            elif r.resName.upper() != "HOH":
                retStr += "X"
        return retStr

