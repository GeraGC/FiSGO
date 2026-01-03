from FiSGO.SimpleGroups import simple_group, simple_group_ids, sporadic_group_ids, sporadic_lookup_property
import FiSGO.SimpleGroups as sg
import bz2
import timeit
import json
import importlib.resources as ires
import FiSGO.PrimesHandler as ph
import FiSGO.PIrrepsSearch as pis
import math
import FiSGO.OrderSearch as Os
import logging

logging.basicConfig(level=logging.INFO)

# powers_list, remainder = ph.prime_scanner(60, 4)
# print(ph.prime_reconstructor(powers_list, remainder))
#
# tes = ChevalleyA(3,(2,4))
#
# s = [sum([OrderSearch.powers_sequence(3, i) for i in range(1,j+1)]) for j in range(1,100)]
#
# print(s)
#
# n = OrderSearch.candidate_from_power(100, 3)
# print(n)
# print((n+1)//3)
# print(s[(n+1)//3-1])
#
# test = [0,1,1,1,0,1,0,1,0]
# print(test[:test.index(0)])
#
#
# powers = [600,300,100,100,100,100,100,100]
#
# print(OrderSearch.candidates_AA(powers, return_codes=True))
#
# print(prime_scanner(Alternating(22).order(), 23))
# print(prime_scanner(Alternating(21).order(), 23))
# print(prime_scanner(Alternating(20).order(), 23))


# L = ['AA-5'] + Alternating(5).isomorphisms()
# L2 =  [ChevalleyB(3,(2,50)), ChevalleyB(3,(2,50)), ChevalleyC(3,(2,50))] + [simple_group(code) for code in L]
# L3 = (((L + [ChevalleyA(1,7).code()] + ChevalleyA(1,7).isomorphisms()
#       + [ChevalleyA(1,9).code()] + ChevalleyA(1,9).isomorphisms())
#       + [ChevalleyA(3,2).code()] + ChevalleyA(3,2).isomorphisms())
#       + [ChevalleyB(2,3).code()] + ChevalleyB(2,3).isomorphisms())
#
#
# print(L3)
#
# print(OrderSearch.clear_duplicates(L3, True))
#
# print(simple_group('CA-3-2').isomorphisms())


# print(sorted(simple_group_ids().keys()))
# print(sorted(["AA", "SP", "CY", "CA", "CB", "CC", "CD", "SA", "SD", "E6", "E7", "E8", "F4", "2E", "3D", "RF", "SZ", "RG", "G2", "TT"]))
#
# group = simple_group("G2-4")
#
# print(group.latex_name())
# print(group.code())
# print(group.isomorphisms())
# print(group.normalized_code())
# print(group.smallest_pirrep_degree())


# def f_zipped():
#     with bz2.open("../PrecomputedData/BuiltinPrimes.txt.bz2", "rt") as exceptions_file:
#         for i in range(20):
#             exceptions_file.readline().removesuffix("\n")
#
#
# def f_unzipped():
#     with open("../PrecomputedData/BuiltinPrimes.txt", "r") as exceptions_file:
#         for i in range(20):
#             exceptions_file.readline().removesuffix("\n")


# print(timeit.timeit(sporadic_group_ids_zipped, number=100)/100)
# print(timeit.timeit(sporadic_group_ids, number=100)/100)

# print(sporadic_lookup_property("id", "J2", "latex_name"))

# print(simple_group("CA-2-3").hiss_malle_pirreps())
# print(simple_group("AA-5").isomorphisms())
# print(simple_group("CA-1-4").hiss_malle_pirreps())
# print(simple_group("AA-5").hiss_malle_pirreps())
# print(simple_group("AA-5").hiss_malle_pirreps(allow_duplicates=True))
# print(simple_group("CA-2-5").hiss_malle_pirreps(char=7))
# print(simple_group("CA-2-5").hiss_malle_pirreps(char=7, allow_duplicates=True))
# print(simple_group("CA-2-5").hiss_malle_pirreps(char=7, all_pirrep_data=True))
# print(simple_group("CA-2-5").hiss_malle_pirreps(char=None))
# print(len(simple_group("CA-2-5").hiss_malle_pirreps(char=None)))
# print("")
# print(simple_group("CA-1-25").hiss_malle_pirreps(char=7))
# print(simple_group("CA-1-25").hiss_malle_pirreps(char=7, allow_duplicates=True))
# print(simple_group("CA-1-25").hiss_malle_pirreps(char=7, all_pirrep_data=True))
# print(simple_group("CA-1-25").hiss_malle_pirreps(char=None))

# print(timeit.timeit(lambda:pis.build_single_bound(100000), number=100)/100)

# print(simple_group("SP-J2").pirrep_degrees())
# print(simple_group("SP-J2").pirrep_degrees(include_cover=True))
# print(simple_group("SP-J2").multiplier())
# print(list(simple_group_ids().keys()))

ignore_all = ['CA', 'CB', 'CC', 'CD', 'SA', 'SP', 'SD', 'AA', 'E6', 'E7', 'E8', 'F4', 'G2', 'TT', '2E', '3D', 'SZ', 'RF', 'RG', 'CY']
ignore_all.remove('CC')

# print(sporadic_lookup_property("id", r"Fi24'", "id"))

# print(sg.simple_group("SP-M12").smallest_pirrep_degree())
# print(sg.simple_group("SP-M11").smallest_pirrep_degree())
# print(sg.simple_group("SP-M").smallest_pirrep_degree())
# print(sg.simple_group("SP-J4").smallest_pirrep_degree())


# print(timeit.timeit(lambda: Os.candidates_CA(pis.build_single_bound(448)), number=1))

# print(pis.pirreps_search(500))

# print(pis.pirreps_search([251,1001],ignore=["AA"], include_origin=True))

print(Os.simple_group_by_order([4,2,1,2,1,0,1]))