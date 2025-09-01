from FiSGO import SimpleGroups as sg

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

print(sg.sporadic_group_ids())
print(len(sg.sporadic_group_ids()))
print(sg.simple_group_ids().keys())

print(sg.sporadic_lookup_property("id", "J2", "latex_name"))

print(sg.simple_group("CA-1-5").latex_name())
print(sg.simple_group("SA-4-2").latex_name())
print(sg.simple_group("CC-3-2").latex_name())
print(sg.simple_group("CB-3-3").latex_name())


