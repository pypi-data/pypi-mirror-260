import sys
from apalib import Container
import apalib.config
import copy
from apalib.Data import data as data
global FLAGS
FLAGS = {}


class Atom:
    def __init__(self, serial = None, name = None, altLoc = None, resName = None, chainID = None, resSeq = None,
                 iCode = None, x = None, y = None, z = None, occupancy = None, tempFactor = None, element = None,
                 charge = None, extract_missing_element_from_name = True, skip_initialization=False):
        if skip_initialization == True:
            return
        self.SetSerial(serial)
        self.SetName(name, extract_missing_element_from_name)
        self.SetAltLoc(altLoc)
        self.SetResName(resName)
        self.SetChainID(chainID)
        self.SetResSeq(resSeq)
        self.SetICode(iCode)
        self.SetXYZ(x,y,z)
        self.SetOccupancy(occupancy)
        self.SetTempFactor(tempFactor)
        if element is not None and element != '':
            self.SetElement(element)
        self.SetCharge(charge)
        for key in self.__dict__:
            if self.__dict__[key] == '':
                self.__dict__[key] = None

    def Copy(self):
        return copy.deepcopy(self)
        # newAtom = Atom(skip_initialization=True)
        # for var in self.__dict__:
        #     newAtom.__dict__[var] = self.__dict__[var]
        # if 'x' in self.__dict__: # Decouple the coordinate list in the new atom
        #     newAtom.SetXYZ(self.x, self.y, self.z)
        # return newAtom

    def AddAttribute(self, attr, var):
        self.__dict__[attr] = var

    def SetSerial(self, serial):
        self.serial = serial

    def GetSerial(self):
        return self.serial

    def SetName(self, name, extract):
        self.name = name
        if extract and name is not None:
            self.__ExtractElement(name)

    def GetName(self):
        return self.name

    def SetAltLoc(self, altLoc):
        self.altLoc = altLoc

    def GetAltLoc(self):
        return self.altLoc

    def SetResName(self, resName):
        self.resName = resName

    def GetResName(self):
        return self.resName

    def SetChainID(self, chainID):
        self.chainID = chainID

    def GetChainID(self):
        return self.chainID

    def SetResSeq(self, resSeq):
        self.resSeq = resSeq

    def GetResSeq(self):
        return self.resSeq

    def SetICode(self, iCode):
        self.iCode = iCode

    def GetICode(self):
        return self.iCode

    def SetXYZ(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.SetCoordinates([self.x, self.y, self.z])

    def GetXYZ(self):
        return [self.x, self.y, self.z]

    def SetCoordinates(self, coordinates):
        self.coordinates = [coordinates[0], coordinates[1], coordinates[2]]
        if isinstance(coordinates, list) and len(coordinates) == 3:
            self.coordinates = [float(x) for x in self.coordinates]

    def GetCoordinates(self):
        return self.coordinates

    def SetOccupancy(self, occupancy):
        self.occupancy = occupancy

    def GetOccupancy(self):
        return self.occupancy

    def SetTempFactor(self, tempFactor):
        self.tempFactor = tempFactor

    def GetTempFactor(self):
        return self.tempFactor

    def SetElement(self, element):
        self.element = element

    def GetElement(self):
        return self.element

    def SetCharge(self, charge):
        self.charge = charge

    def GetCharge(self):
        return self.charge

    #In case the element informatin is missing
    def __ExtractElement(self, id):
        if 'CU' in id:
            self.SetElement('CU')
        elif 'SE' in id:
            self.SetElement('SE')
        elif 'O' in id:
            self.SetElement('O')
        elif 'ZN' in id:
            self.SetElement('ZN')
        elif 'P' in id:
            self.SetElement('P')
        elif 'N' in id:
            self.SetElement('N')
        elif 'C' in id:
            self.SetElement('C')
        elif 'S' in id:
            self.SetElement('S')
        elif 'MG' in id:
            self.SetElement('MG')
        elif 'H' in id:
            self.SetElement('H')
        elif "FE" in id.upper():
            self.SetElement('FE')
        else:
            self.SetElement(''.join([x for x in id if x.isalpha()]))
            # sys.exit("SOMETHING WENT WRONG! CHECK WHAT HAPPENED! THIS ERROR SHOULD NOT OCCUR")

    def GetRadius(self, ver = "Van der Waals"):
        name = data.Map('Elements', self.element)
        return data.GetJson()['Atoms'][name]['Radius'][ver]

    def GetDistance(self, other):
        return ((self.coordinates[0] - other.coordinates[0])**2 + (self.coordinates[1] - other.coordinates[1])**2 + (self.coordinates[2] - other.coordinates[2])**2)**.5

    def GetConfiguration(self, extended=False):
        name = data.Map('Elements', self.element)
        if not extended:
            return data.GetJson()['Atoms'][name]["Ground Configuration"]
        else:
            return data._BuildConfiguration(name)

    def WritePDB(self, intro="ATOM  "):
        retstr = intro
        retstr += apalib.config.ToStringLen(self.serial, 5, left_justify=False)
        retstr += "  "
        retstr += apalib.config.ToStringLen(self.name, 3, left_justify=True)
        retstr += apalib.config.ToStringLen(self.altLoc, 1, left_justify=False)
        retstr += apalib.config.ToStringLen(self.resName, 3, left_justify=False)
        retstr += " "
        retstr += apalib.config.ToStringLen(self.chainID, 1, left_justify=False)
        retstr += apalib.config.ToStringLen(self.resSeq, 4, left_justify=False)
        retstr += " "  # TODO Verify this. What is AChar?
        retstr += "   "
        retstr += apalib.config.ToStringLen(round(self.x, 3), 8, left_justify=False)
        retstr += apalib.config.ToStringLen(round(self.y, 3), 8, left_justify=False)
        retstr += apalib.config.ToStringLen(round(self.z, 3), 8, left_justify=False)
        retstr += apalib.config.ToStringLen(self.occupancy, 6, left_justify=False)
        retstr += apalib.config.ToStringLen(self.tempFactor, 6, left_justify=False)
        retstr += apalib.config.ToStringLen("", 8, left_justify=True)
        retstr += apalib.config.ToStringLen(self.element, 4, left_justify=False)
        retstr += apalib.config.ToStringLen(self.charge, 2, left_justify=True)
        retstr += "\n"
        return retstr

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

    #TODO Make this not crash if an element is missing. Probably iterate through self.__dict__()
    def __repr__(self):
        retStr = f"Atom: {self.resName} {self.resSeq} : {self.name} {self.serial}"
        return retStr

    def __str__(self):
        retStr = f"Atom: {self.resName} {self.resSeq} : {self.name} {self.serial}"
        return retStr