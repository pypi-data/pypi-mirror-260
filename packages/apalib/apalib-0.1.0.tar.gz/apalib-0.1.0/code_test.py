import apalib
data = apalib.GetData()
print(data.GetAtomMass("u"))

# import json
# json_d = apalib.j_data.GetJson()
# for atom in json_d['Atoms'].keys():
#     avg = 0
#     for num in json_d['Atoms'][atom]['Stable'].keys():
#         avg += json_d['Atoms'][atom]['Stable'][num]["Mass"] * json_d['Atoms'][atom]['Stable'][num]["Abundance"]
#     print(avg)
#     json_d['Atoms'][atom]["Molar Mass"] = round(avg, 5)
#
# with open("chemistry_new.json", "w") as fp:
#     json.dump(json_d, fp, indent=3)
# print("stop")
#
#
# num_to_generate = 1000 #@param {type: "integer"}
#
# import urllib.request
# import os
# import random
#
# # if "pdbcodes.txt" not in os.listdir():
# #   urllib.request.urlretrieve(r"https://raw.githubusercontent.com/cathepsin/PublicData/main/All_PDB_Codes_Jan_12_2024.txt", "pdbcodes.txt")
# # with open("pdbcodes.txt", "r") as fp:
# #   codes = fp.readlines()
# # code_set = random.sample(codes, num_to_generate)
# # for code in code_set:
# #   print(code.strip())
# #   pdb = apalib.PDB()
# #   pdb.Fetch(code)
#
#
# pdb = apalib.PDB()
# pdb.Fetch('6Q25')
# # pdb.Fetch('1m1c') #Lots of chains and a ton of matrices
# # pdb.Fetch('7wub') #Only one matrix
# # pdb.Fetch('6pd4') #Two biomolecules
# # x = pdb.Contents().DumpAtoms()
# # pdb.Contents().PopulateResidueGroups()
# # pdb.RemoveWater()
# # potential_neighborhood = pdb.Contents().Chains['A'].values()
# # x = pdb.Contents().Chains['A'][14].GetNeighborhood(potential_neighborhood=potential_neighborhood, distance = 20)
# # print(x)
#
#
# sym = pdb.Contents().GetSymmetry(0)
#
# chainA = pdb.Contents().GetChain('A')
#
# sym_chain = sym.GenerateSymmetricCollection(chainA)
# pdb.AddChain(sym_chain[1])
# pdb.AddChain(sym_chain[2])
#
# pdb.WritePDB("test_copy.pdb")
#
# print("Stop")
#
# #7E93 is missing an alpha carbon at chain E, ASN 169