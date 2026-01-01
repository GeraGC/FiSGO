from FiSGO import SimpleGroups as sg
import FiSGO.PrimesHandler as ph
import FiSGO.PIrrepsSearch as pis
import FiSGO.OrderSearch as Os
import math
import timeit

from FiSGO.OrderSearch import candidates_AA
from FiSGO.SimpleGroups import simple_group

"""
A5 = sg.simple_group("CA-2-2_3")
A4 = sg.simple_group("SP-Fi24\'")
print(A5.order())
print(A5.multiplier())
print(A4.order())
print(A4.multiplier())
print(type(A4))
print(type(A5))
print(A5.code())
print(A4.code())

L = (1,1,1,1,1)
print(L)
print(ph.prime_list(len(L)))
print(ph.nth_prime(len(L)))
primes = ph.primes(10)
print()
print(next(primes))
print(next(primes))
print(next(primes))
print(next(primes))
S = L.copy()
S += [2]
print(L)


bound = [25, 28, 18, 14, 11, 10, 1, 1, 1, 1, 1]
LA = QP.candidates_CA(bound, return_codes=True)
print(len(LA), LA)
LB = QP.candidates_CB(bound, return_codes=True)
print(len(LB), LB)
LC = [code for code in QP.candidates_CC(bound, return_codes=True) if code.split("-")[-1][:2] != "2_"]
print(len(LC), LC)
print(len(LC) + len(LB))
LD = QP.candidates_CD(bound, return_codes=True)
print(len(LD), LD)

"""
# def check_candidate(code, bound):
#     group_order_factors = ph.factor(sg.simple_group(code).order(), list_output=True)[0]
#     if len(group_order_factors) > len(bound):
#         return False
#     for i in range(len(group_order_factors)):
#         if group_order_factors[i] > bound[i]:
#             return False
#     return True
#
# codes = []
# bound = [120, 120] + [15 for i in range(65)] + [1 for j in range(1000)]
# for F in [OS.candidates_E6, OS.candidates_E7, OS.candidates_E8, OS.candidates_F4, OS.candidates_G2]:
#     L = F(bound, return_codes=True)
#     codes += L
#     print(len(L), L)
#
# for code in codes:
#     if not check_candidate(code, bound):
#         print(code)
#

# print(ph.factor(sg.simple_group("E8-3_1").order()))
# print(ph.factor(sg.simple_group("E6-3_2").order(), list_output=True))

# print(sg.sporadic_group_ids())
# print(len(sg.sporadic_group_ids()))
# print(sg.simple_group_ids().keys())
#
# print(sg.sporadic_lookup_property("id", "J2", "latex_name"))
#
# print(sg.simple_group("CA-1-5").latex_name())
# print(sg.simple_group("SA-4-2").latex_name())
# print(sg.simple_group("CC-3-2").latex_name())
# print(sg.simple_group("CB-3-3").latex_name())

# bound = pis.build_single_bound(1000)
# print(bound)
#
# bounds = pis.build_bounds([250,1001])
# print(bounds)

# print(pis.hiss_malle_range([100,120]))
# print(pis.pirreps_search([100,121]))

# def prime_bound_compatiblity_alt(order: tuple[list[int], int], bound: list[int]) -> bool:
#     if order[1] != 1:
#         # There have appeared primes which are not in prime_bounds, so this group is not a candidate
#         return False
#     # We now check prime order compatibility against the relative order
#     res = True
#     for j, b in enumerate(bound):
#         res &= order[0][j] > b
#     return True if res else False
#
#
# order = ([120, 120] + [13 for i in range(65)] + [1 for j in range(999)] + [2], 1)
# bound = [120, 120] + [15 for i in range(65)] + [1 for j in range(1000)]
# iters = 10000
#
# t1 = timeit.timeit(lambda: prime_bound_compatiblity_alt(order, bound), number=iters)/iters
# t2 = timeit.timeit(lambda: Os.prime_bound_compatiblity(order, bound), number=iters)/iters
#
# print(prime_bound_compatiblity_alt(order, bound))
# print(Os.prime_bound_compatiblity(order, bound))
#
# print(t1, t2, t2/t1)
#
# print(pis.build_single_bound(1000))
# print(pis.build_bounds([250,1001]))

code_list_bi = ["CA-4-3", "CA-3-4", "CA-2-13", "CA-1-2_2", "CA-8-3", "CA-10-25"]
code_list_uni = ["E6-3", "E6-4", "E6-7"]
code_list_RF = ["RF-2", "RF-3", "RF-6", "RF-5"]
code_list_SZ = ["SZ-1", "SZ-2", "SZ-3", "SZ-6", "SZ-5"]
code_list_RG = ["RG-2", "RG-3", "RG-6", "RG-5"]

code_list = code_list_bi
group_list = [sg.simple_group(code) for code in code_list]
group_id = "CA"

reps, unavailable = pis.lubeck_bulk_get(group_id, group_list)
print("Representation degrees:")
for group in reps.keys():
    print(f"Degrees of {group.normalized_code()}")
    print(reps[group])
print("Unavailable groups:")
print([group.normalized_code() for group in unavailable])