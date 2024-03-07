from apalib.Data import Data
import apalib.config
import apalib.apalibExceptions
from apalib.Container import Container
from apalib.AminoAcid import AminoAcid
# from apalib.Atom import Atom
from apalib.DNA import DNA
from apalib.RNA import RNA
from apalib.HETATM import HETATM
from apalib.pdb import PDB
from apalib.RandomProtein import RandomProtein
from apalib.ProteinStats import ProteinStats
import math
import sys

global j_data
j_data = Data()


def GetData():
    global j_data
    return j_data


global _verbose
_verbose = False


def Verbose():
    global _verbose
    _verbose = True


# noinspection PyPep8Naming
def Silence():
    global _verbose
    _verbose = False


# TODO work on error messages
# try:
#     requests.get(r"http://www.google.com", timeout=5)
# except :
#     sys.stderr.write(apalib.apalibExceptions.BadInternet())


# TODO Move **ALL HARDCODED DATA** into a json
# TODO Make error messages a full string (functional with stderr.write())
# Parsing DNA/RNA should be essentially the same as an amino acid atom-group, with some intricacies. 1pyi is a good example
# TODO Ensure functionality with symmetry pairs
# TODO Make set_name a thing everywhere

#  Naive approach to calculating isoelectric point at a specific pH

def getIEP(pHofInterest):
    global CONTAINER
    curr_protein_chains = CONTAINER.PeptideChains

    # initialize dict of counts
    total_counts = {'NTERM': 0, 'CTERM': 0, 'CYS': 0, 'ASP': 0, 'GLU': 0, 'HIS': 0, 'LYS': 0, 'ARG': 0, 'TYR': 0}
    for key, value in curr_protein_chains.items():
        current_chain = value
        # TODO Add check for termini (in case section of a protein is checked instead of a full protein)
        # TODO Are there pKas for nucleic acids?

        total_counts['NTERM'] += 1
        total_counts['CTERM'] += 1

        for key, value in current_chain.items():
            if value.name == "CYS":
                total_counts['CYS'] += 1
            elif value.name == "ASP":
                total_counts['ASP'] += 1
            elif value.name == "GLU":
                total_counts['GLU'] += 1
            elif value.name == "HIS":
                total_counts['HIS'] += 1
            elif value.name == "LYS":
                total_counts['LYS'] += 1
            elif value.name == "ARG":
                total_counts['ARG'] += 1
            elif value.name == "TYR":
                total_counts['TYR'] += 1
    print(total_counts)

    # TODO Add pKa values to JSON file
    # using "EMBOSS" pKa's

    sum_charges = 0

    if pHofInterest < 8.6:
        sum_charges += total_counts['NTERM']
    if pHofInterest > 3.6:
        sum_charges -= total_counts['CTERM']
    if pHofInterest > 8.5:
        sum_charges -= total_counts['CYS']
    if pHofInterest > 3.9:
        sum_charges -= total_counts['ASP']
    if pHofInterest > 4.1:
        sum_charges -= total_counts['GLU']
    if pHofInterest < 6.5:
        sum_charges += total_counts['HIS']
    if pHofInterest < 10.8:
        sum_charges += total_counts['LYS']
    if pHofInterest < 12.5:
        sum_charges += total_counts['ARG']
    if pHofInterest > 10.1:
        sum_charges -= total_counts['TYR']

    return sum_charges


# TODO in all GETTERS in each class, add a check to see if variable exists
# TODO Complete the below functions before pushing version 1.0.0

# def SurfaceArea(**kwargs):
#     if 'domain' not in kwargs:
#         sys.stderr.write("No domain provided. Specify using SurfaceArea(domain=val)\n")
#     if 'num_dots' not in kwargs:
#         sys.stderr.write("Number of dots not provided. Specify using SurfaceArea(num_dots=val)\n")
#     if 'solvent_radius' not in kwargs:
#         sys.stderr.write("Solvent radius not provided. Specify using SurfaceArea(solvent_radius=val)\n")
#     print("stub")
#

"""
A. Shrake, J.A. Rupley, Environment and exposure to solvent of protein atoms. Lysozyme and insulin,
Journal of Molecular Biology, Volume 79, Issue 2, 1973,
Pages 351-371, ISSN 0022-2836, https://doi.org/10.1016/0022-2836(73)90011-9.
(https://www.sciencedirect.com/science/article/pii/0022283673900119)
"""


def ShrakeRupleySASA(domain=None, context=None, n_dots=200, sol_radius=1.4, include_hydrogen=False):
    if context is None:
        context = domain
    pass


# From http://extremelearning.com.au/how-to-evenly-distribute-points-on-a-sphere-more-effectively-than-the-canonical-fibonacci-lattice/
def _GetCloseAtoms(atom, solv_rad, context):
    close = []
    for a in context:
        if atom.GetDistance(a) <= atom.GetRadius() + solv_rad:
            close.append(a)
    return close


# noinspection SpellCheckingInspection
def _GenerateFibSphere(n, radius=1, offset=None, np=False):
    if offset is None:
        offset = [0, 0, 0]
    import math
    goldenRatio = (1 + 5 ** 0.5) / 2
    if np:
        from numpy import arange, pi, sin, cos, arccos
        ind = arange(0, n)
        theta = 2 * pi * ind / goldenRatio
        phi = arccos(1 - 2 * (ind + 0.5) / n)
        x = radius * cos(theta) * sin(phi) + offset[0]
        y = radius * sin(theta) * sin(phi) + offset[1]
        z = radius * cos(phi) + offset[2]
    else:
        ind = range(0, n)
        theta = [val * 2 * math.pi / goldenRatio for val in ind]
        phi = [math.acos(1 - 2 * (val + .5) / n) for val in ind]
        x = [radius * math.cos(theta[i]) * math.sin(phi[i]) + offset[0] for i in range(len(ind))]
        y = [radius * math.sin(theta[i]) * math.sin(phi[i]) + offset[1] for i in range(len(ind))]
        z = [radius * math.cos(phi[i]) + offset[2] for i in range(len(ind))]
    coords = []
    for i in range(len(x)):
        coords.append([x[i], y[i], z[i]])
    return coords


def GetUnfoldedSASA(lst, form="Gly-X-Gly ASA w"):
    working = lst
    accepted = ["Gly-X-Gly ASA w", "Gly-X-Gly ASA sc", "Ala-X-Ala ASA w", "Ala-X-Ala ASA sc"]
    if form not in accepted:
        sys.stderr.write("Bad type. Add more to this message")
    if type(lst) == type({}):
        working = list(lst.values())
    totalASA = 0
    for prot in working:
        totalASA += prot.GetASA(form)
    return totalASA


def VectorPair(AA1, AA2):
    # Slope of line made from CA --> CENTROID
    CA1 = AA1.GetBaseAtom()
    CA2 = AA2.GetBaseAtom()
    # XY orthogonal projection
    m1 = (AA1.GetCentroid()[1] - CA1.GetCoordinates()[1]) / (AA1.GetCentroid()[0] - CA1.GetCoordinates()[0])
    m2 = (AA2.GetCentroid()[1] - CA2.GetCoordinates()[1]) / (AA2.GetCentroid()[0] - CA2.GetCoordinates()[0])
    '''
     Intersection point
                   y_2 - y_1 + m_1x_1 - m_2x_2
       x_int =    ------------------------------
                           m_1 - m_2
    '''
    x_int = (AA2.GetCentroid()[1] - AA1.GetCentroid()[1] + m1 * AA1.GetCentroid()[0] - m2 * AA2.GetCentroid()[0])
    ''' 
    Cast back into 3D
            x - x_1
       z = --------- * c + z_1
               a
    '''
    y1 = (x_int - AA1.GetCentroid()[0]) / AA1.vector[0] * AA1.vector[1] + AA1.GetCentroid()[1]
    y2 = (x_int - AA2.GetCentroid()[0]) / AA2.vector[0] * AA2.vector[1] + AA2.centroid[1]
    z1 = (x_int - AA1.GetCentroid()[0]) / AA1.vector[0] * AA1.vector[2] + AA1.GetCentroid()[2]
    z2 = (x_int - AA2.GetCentroid()[0]) / AA2.vector[0] * AA2.vector[2] + AA2.GetCentroid()[2]
    return abs(z1 - z2), [x_int, y1, z1], [x_int, y2, z2]


def GetCentAngle(res1, res2, rad=True):
    # Get angle using res1_centroid --> res1_CA --> res2_CA
    CA1 = res1.GetBaseAtom().GetCoordinates()
    CA2 = res2.GetBaseAtom().GetCoordinates()
    cent = res1.GetCentroid()
    a = GetDist(cent, CA1)
    b = GetDist(CA1, CA2)
    c = GetDist(cent, CA2)
    theta = math.acos(-1 * (c ** 2 - a ** 2 - b ** 2) / (2 * a * b))
    if rad:
        return theta
    return math.degrees(theta)


# Checks that a residue-vector does not point backwards to extend towards a point
# TODO test this function a bit more
def CheckIsForward(res, pt):
    v1 = res.GetVector()
    v2 = [res.centroid[0] - pt[0],
          res.centroid[1] - pt[1],
          res.centroid[2] - pt[2]]
    # If any of the components switch direction then all v1_i * v2_i will be negative
    if v1[0] * v2[0] < 0 or v1[1] * v2[1] < 0 or v1[2] * v2[2] < 0:
        return False
    return True


def GetDist(a1, a2):
    return ((a1[0] - a2[0]) ** 2 + (a1[1] - a2[1]) ** 2 + (a1[2] - a2[2]) ** 2) ** (1 / 2)

#
# def CheckBridge(object1, object2):
#     print("stub")

# TODO Make sure ALL flags are properly cleared automatically
