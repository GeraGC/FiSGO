import json
import logging
import math
import FiSGO.PrimesHandler as Ph
import re
from typing import Any

"""
Module implementing simple group objects.

    .. |Tits| replace:: :sup:`2`\ F\ :sub:`4`\ (2\)'
    .. |RG| replace:: :sup:`2`\ G\ :sub:`2`\ (3\ :sup:`2n+1`)
    .. |RF| replace:: :sup:`2`\ F\ :sub:`4`\ (2\ :sup:`2n+1`)
    .. |2E| replace:: :sup:`2`\ E\ :sub:`6`\ (q\ :sup:`2`)
    .. |3D| replace:: :sup:`3`\ D\ :sub:`4`\ (q\ :sup:`3`)
    .. |E6| replace:: E\ :sub:`6`\ (q)
    .. |E7| replace:: E\ :sub:`7`\ (q)
    .. |E8| replace:: E\ :sub:`8`\ (q)
    .. |F4| replace:: F\ :sub:`4`\ (q)
    .. |G2| replace:: G\ :sub:`2`\ (q)
    .. |SZ| replace:: :sup:`2`\ B\ :sub:`2`\ (2\ :sup:`2n+1`)
    .. |CA| replace:: A\ :sub:`n`\ (q)
    .. |CB| replace:: B\ :sub:`n`\ (q)
    .. |CC| replace:: C\ :sub:`n`\ (q)
    .. |CD| replace:: D\ :sub:`n`\ (q)
    .. |SA| replace:: :sup:`2`\ A\ :sub:`n`\ (q\ :sup:`2`)
    .. |SD| replace:: :sup:`2`\ D\ :sub:`n`\ (q\ :sup:`2`)
"""

# TODO: Module documentation
# TODO: Alternating groups smallest pirrep degree
# TODO: Implement reading the Hiss-Malle data, recall that Th has an 'all' representation, denoted
#   by None in both 'char' and 'not_char'.


GLOBAL_VALIDATE = True

TITS_ORDER = [11, 3, 2, 0, 0, 1]

CHEVALLEY_E6_POWER_INDICES = [2,5,6,8,9,12]
CHEVALLEY_E7_POWER_INDICES = [2,6,8,10,12,14,18]
CHEVALLEY_E8_POWER_INDICES = [2,8,12,14,18,20,24,30]
CHEVALLEY_F4_POWER_INDICES = [2,6,8,12]
CHEVALLEY_G2_POWER_INDICES = [2,6]
STEINBERG_2E6_POWER_INDICES = [2,5,6,8,9,12]


class SimpleGroup:
    def __init__(self):
        """
        Base class for simple groups.
        """
        self.__order = None
        self.__schur_multiplier = None

    @classmethod
    def from_code(cls, code: str):
        """
        Given a valid simple group code, returns the corresponding simple group object.

        A simple group code is a string formed by an ID and the group parameters:

        * ID: identifies to which family of simple groups the code refers to. It consists of two characters, all valid IDs are listed in SimpleGroups.simple_group_ids().
        * Parameters: Any group has up to two parameters. Except for sporadic groups, these parameters are called 'n' or 'q'. 'n' refers to a positive integer, while 'q' refers to a prime power. A 'q' parameter can be given either as the number or as a pair [prime number]_[power].
        * Sporadic group names: All valid names for sporadic groups are listed in SimpleGroups.sporadic_group_names().

        A code is formed by joining the code and its parameters using '-' as the separator. The syntax is as follows:

        * 0-parametric group: "[ID]", Example: "TT".
        * 1-parametric group: "[ID]-[parameter]", Examples: "E6-9", "E6-3_2", "SZ-6".
        * 2-parametric group: "[ID]-[n parameter]-[q parameter]", Examples: "CA-1-2", "SA-2-9", "SA-2-3_2".
        * Sporadic group: "SP-[group name]", Examples: "SP-M11", "SP-Fi24\'".

        CAUTION: The name of the Fischer group 24' is "Fi24\'", if printed, it will show "Fi24'" as the character "'" is
        being formated, this may create confusion.

        :param code: Code corresponding to some simple group.
        :return: The simple group object corresponding to the given code.
        """
        if re.search(r"^(C[ABCD]|S[AD])-\d+-\d+(_\d+)?$", code) is not None:
            if "_" not in code:
                n, q = (int(i) for i in re.split(r"-", code[3:]))
            else:
                n = int(re.split(r"-", code[3:])[0])
                q = tuple(int(i) for i in re.split(r"-", code[3:])[1].split("_"))
            return BiParamSimpleGroup.from_id(code[:2], n, q)
        elif re.search(r"^(CY|AA|E[678]|F4|G2|2E|3D|SZ|R[FG])-\d+(_\d+)?$", code) is not None:
            if "_" in code:
                return UniParamSimpleGroup.from_id(code[:2], tuple(int(i) for i in code[3:].split(r"_")))
            return UniParamSimpleGroup.from_id(code[:2], int(code[3:]))
        elif re.search(r"^SP-.+", code) is not None:
            return Sporadic(code[3:])
        elif code == "TT":
            return Tits()
        else:
            raise ValueError("Invalid simple group identifier")

    def compute_order(self) -> int:
        """
        Computes the order of the group.

        :return: Order of the group.
        """
        pass

    def order(self) -> int:
        """
        Returns the order of the group.

        If the order has not been calculated before (i.e. has not been internally stored yet), it calculates the order
        and returns it.

        :return: Order of the group.
        """
        if self.__order is None:
            self.__order = self.compute_order()
        return self.__order

    def compute_multiplier(self):
        """
        Computes the size Schur multiplier of the simple group (these are known values).

        :return: Order of the simple group's Schur multiplier.
        """
        pass

    def multiplier(self) -> int:
        """
        Returns the order of simple group's Schur multiplier.

        If it has not been calculated before (i.e. has not been internally stored yet), it calculates it
        and returns it.

        :return: Order of the simple group's Schur multiplier.
        """
        if self.__schur_multiplier is None:
            self.__schur_multiplier = self.compute_multiplier()
        return self.__schur_multiplier

    def p_sylow_power(self, p: int) -> int:
        """
        Given a prime number p, it returns exponent n of the size of its p-Sylow subgroup(s), p**n.

        :param p: Prime number.
        :return: Number n such that the p-Sylow subgroup(s) of the simple group have order p**n.
        """
        return Ph.contained_power(self.order(), p)

    def isomorphisms(self) -> list[str]:
        """
        Returns a list of group codes whose groups are isomorphic to self. Returns an empty list if the group is
        not isomorphic to any other group apart from itself.

        :return: Codes of groups isomorphic to itself.
        """
        return []

    def latex_name(self) -> list[str]:
        """
        Returns a list of strings containing possible notations for the simple group in a LaTeX format. To properly
        visualize the string in LaTeX format, the strings need to be printed.

        The first string of the list corresponds to the `Wikipedia List of finite simple groups`_ recommended names.

        :return: List of possible notations for the simple group formatted in LaTeX.

        .. _Wikipedia List of finite simple groups: https://en.wikipedia.org/wiki/List_of_finite_simple_groups
        """
        pass

    def GAP_name(self) -> str:
        """
        Returns a string with the name of the simple group in GAP4/Atlas like notation. This name can be used to
        look up the group character table in GAP if already available in a package such as AtlasRep or CTblLib.

        :return: Name of the group in GAP4/Atlas like notation.
        """
        pass

    def code(self) -> str:
        """
        Returns the code of the simple group.

        :return: Code of the simple group.
        """
        pass

    def normalized_code(self) -> str:
        """
        There are two formats for the q parameter of the groups (power of a prime number): either as a single number or
        as a pair of numbers. The normalized code corresponds to the pair of numbers. This function returns the normalized
        code. If the group does not have a q parameter, it returns the same as self.code().

        Example: "CA-1-4" or "CA-1-2_2" are both valid codes for the Chevalley A group with parameters n=1 and q=4,
        the normalized code is "CA-1-2_2".

        :return: Normalized code of the simple group.
        """
        pass

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        """
        Using the bounds of Seitz, Landazuri, Tiep and Zalesskii, returns the degree of the smallest non-trivial
        projective irreducible complex representation of the simple group. Furthermore, it also returns the number of
        different representations of that degree.

        :return: The degree of the smallest non-trivial complex projective representation and the number of different
            representations of that degree.
        """
        # We first handle the possible exceptions
        with open("PrecomputedData/smallest_pirrep_degree_exceptions.json", "r") as exceptions_file:
            for exception in json.load(exceptions_file):
                if self.code() in exception["code"]:
                    return exception["degree"], exception["irreps"]
        # Non-exceptional cases are handled in the derived classes
        return 0, 0


class UniParamSimpleGroup(SimpleGroup):
    def __init__(self, par: int | tuple[int, int], validate = True):
        """
        Base class for simple groups with one parameter.

        On object initialization, if validate is True, it will attempt to check if the introduced parameter is valid.
        Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param par: A parameter for a simple group.
        :param validate: If True, the given parameter is validated on object initialization. If False, any checks are
            skipped.
        """
        super().__init__()
        self.par = par
        if validate and GLOBAL_VALIDATE:
            self.__validate_parameters__()

    @classmethod
    def from_id(cls, id_, par):
        """
        Given an uniparametric simple group ID and its parameter par, returns the corresponding simple group object.

        For information on which IDs are valid and uniparametric, see the documentation of SimpleGroups.simple_group_ids.

        :param id_: ID of an uniparametric simple group.
        :param par: The n or q parameter of the group.
        :return: An object of a derived class of UniParamSimpleGroup.
        """
        id_to_class = {"AA": Alternating, "E6": ExcetionalChevalleyE6, "E7": ExcetionalChevalleyE7,
                       "E8": ExcetionalChevalleyE8, "F4": ExcetionalChevalleyF4, "G2": ExcetionalChevalleyG2,
                       "2E": ExcetionalSteinberg2E6, "3D": ExcetionalSteinberg3D4, "SZ": Suzuki, "RF": Ree2F4,
                       "RG": Ree2G2, "CY": Cyclic}
        try:
            return id_to_class[id_](par)
        except KeyError:
            raise ValueError("An uniparametric simple group with ID: " + id_ + " does not exist")

    def __validate_parameters__(self) -> None:
        """
        Attemps to check if the given parameter is a valid parameter for the corresponding simple group.

        Parameter validation can be locally disabled by passing the keyword argument validate = False when initializing
        the object.

        Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :return: None. Raises a ValueError if the parameter is invalid.
        """
        if type(self.par) == int:
            if self.par < 1:
                raise ValueError("The parameter must be a positive integer")

    def __validate_par__(self) -> None:
        """
        Attemps to check if self.par is a valid parameter of q-type, i.e., a prime power.

        :return: None. Raises a ValueError if the parameter is invalid.
        """
        if type(self.par) == tuple:
            if self.par[1] < 1:
                raise ValueError("The second entry of q must be > 0")
            try:
                if not Ph.is_prime(self.par[0]):
                    raise ArithmeticError("The first entry of q must be a prime")
            except ValueError:
                print("Could not verify if the number " + str(self.par[0]) + " is a prime number, you should probably "
                                                                           "consider working with more primes")
        else:
            try:
                n_factors = Ph.factor(self.par)
                if n_factors[1] != 1:
                    raise ValueError
                if len(n_factors[0]) != 1 or self.par < 2:
                    raise ArithmeticError("q must be a prime power")
            except ValueError:
                print("Could not verify if the number " + str(self.par) + " is a prime power, you should probably "
                                                                           "consider working with more primes")

    def par_value(self) -> int:
        """
        Returns the value of the group parameter as an integer. If the parameter is of q-type and stored as a pair
        of integers, it returns the computed value.

        Example:

        >>> UniParamSimpleGroup((3,2)).par_value()
        9

        :return: The value of the group parameter.
        :rtype: int
        """
        if type(self.par) == int:
            return self.par
        else:
            return self.par[0]**self.par[1]

    def normalized_code(self):
        code = self.code()
        if "_" in code:
            return code
        factors, res = Ph.factor(self.par)
        if len(factors) > 1 or res != 1:
            return code
        code_split = code.split("-")
        return f"{code_split[0]}-{list(factors.items())[0][0]}_{list(factors.items())[0][1]}"


class BiParamSimpleGroup(SimpleGroup):
    def __init__(self, n: int, q: int | tuple[int, int], validate = True):
        """
        Base class for simple groups with two parameters.

        On object initialization, if validate is True, it will attempt to check if the introduced parameters are valid.
        Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Dimensional parameter of simple group.
        :param q: Finite field parameter of simple group.
        :param validate: If True, the given parameter is validated on object initialization. If False, any checks are
            skipped.
        """
        super().__init__()
        self.n = n
        self.q = q
        if validate and GLOBAL_VALIDATE:
            self.__validate_parameters__()

    @classmethod
    def from_id(cls, id_, n, q):
        """
        Given a biparametric simple group ID and its parameters n and q, returns the corresponding simple group object.

        For information on which IDs are valid and biparametric, see the documentation of SimpleGroups.simple_group_ids().

        :param str id_: ID of an uniparametric simple group.
        :param int n: The n parameter of the group.
        :param int | tuple[int,int] q: The q parameter of the group.
        :return: An object of a derived class of BiParamSimpleGroup.
        :raises ValueError: if an invalid ID is provided.
        """
        id_to_class = {"CA": ChevalleyA, "CB":ChevalleyB, "CC": ChevalleyC, "CD": ChevalleyD, "SA":Steinberg2A,
                       "SD":Steinberg2D}
        try:
            return id_to_class[id_](n,q)
        except KeyError:
            raise ValueError("A biarametric simple group with ID: " + id_ + " does not exist")

    def __validate_parameters__(self) -> None:
        """
        Attemps to check if the given parameter is a valid parameter for the corresponding simple group.

        Parameter validation can be locally disabled by passing the keyword argument validate = False when initializing
        the object.

        Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :return: None
        :raises ValueError: if the parameter is invalid.
        """
        self.__validate_q__()
        if self.n < 1:
            raise ValueError("n must be a positive integer")

    def __validate_q__(self) -> None:
        """
        Attemps to check if self.q is a valid parameter of q-type, i.e., a prime power.

        :return: None
        :raises ValueError: if the parameter is invalid.
        """
        if type(self.q) == tuple:
            if self.q[1] < 1:
                raise ValueError("The second entry of q must be > 0")
            try:
                if not Ph.is_prime(self.q[0]):
                    raise ArithmeticError("The first entry of q must be a prime")
            except ValueError:
                print("Could not verify if the number " + str(self.q[0]) + " is a prime number, you should probably "
                                                                           "consider working with more primes")
        else:
            try:
                q_factors = Ph.factor(self.q)
                if q_factors[1] != 1:
                    raise ValueError
                if len(q_factors[0]) != 1 or self.n < 1:
                    print(q_factors)
                    raise ArithmeticError("q must be a prime power")
            except ValueError:
                print("Could not verify if the number " + str(self.q) + " is a prime power, you should probably "
                                                                           "consider working with more primes")

    def q_value(self):
        """
        Returns the value of the q group parameter as an integer. If the parameter is stored as a pair of integers,
        it returns the computed value.

        Example:

        >>> BiParamSimpleGroup(2,(3,2)).q_value()
        9

        :return: Integer, the value of the q group parameter.
        """
        if type(self.q) == int:
            return self.q
        else:
            return self.q[0]**self.q[1]

    def normalized_code(self):
        code = self.code()
        if "_" in code:
            return code
        factors = list(Ph.factor(self.q)[0].items())[0]
        code_split = code.split("-")
        return f"{code_split[0]}-{code_split[1]}-{factors[0]}_{factors[1]}"


class Cyclic(UniParamSimpleGroup):
    def __init__(self, n: int, validate = True):
        """
        Class representing the Cyclic group |C_n|, a simple group when n is prime. See `Wikipedia`_.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param int n: Positive integer.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Cyclic_groups,_Zp
        .. |C_n| replace:: C\ :sub:`n`
        """
        super().__init__(n, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        try:
            if not Ph.is_prime(self.par):
                raise ArithmeticError("n must be prime")
        except ValueError:
            print("WARNING: Could not determine if n is prime, consider using a longer prime list")

    def compute_order(self):
        return self.par

    def compute_multiplier(self):
        return 1

    def code(self) -> str:
        return "CY-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        return [f"C_{{{self.par}}}", f"Z_{{{self.par}}}", f"Z/{{{self.par}}}Z"]

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        return 1, self.par


class Alternating(UniParamSimpleGroup):
    def __init__(self, n: int, validate = True):
        """
        Class representing the Alternating group |A_n|, a simple group when n > 4. See `Wikipedia`_.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param int n: Positive integer.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Alternating_groups,_An,_n_>_4
        .. |A_n| replace:: A\ :sub:`n`
        """
        super().__init__(n, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        if self.par < 5:
            raise ValueError("n must be greater than 5 for the alternating group A_n to be simple")

    def compute_order(self):
        return math.factorial(self.par)//2

    def compute_multiplier(self):
        if self.par in [6, 7]:
            return 6
        return 2

    def isomorphisms(self):
        if self.par == 5:
            return ["CA-1-4", "CA-1-5"]
        if self.par == 6:
            return ["CA-1-9"]
        if self.par == 8:
            return ["CA-3-2"]
        return []

    def code(self) -> str:
        return "AA-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        return [f"A_{{{self.par}}}", f"{{\\rm A}}_{{{self.par}}}", f"{{\\frak A}}_{{{self.par}}}",
                f"{{\\rm Alt}}_{{{self.par}}}"]

    def GAP_name(self) -> str:
        return f"A{self.par}"


class ChevalleyA(BiParamSimpleGroup):
    def __init__(self, n: int, q: int | tuple[int, int], validate = True):
        """
        Class representing the classical Chevalley group |A_n(q)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        NOTE: The groups with parameters (n,q) = (1,2) and (1,3) are not simple groups.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_An(q),_Bn(q)_n_>_1,_Cn(q)_n_>_2,_Dn(q)_n_>_3
        .. |A_n(q)| replace:: A\ :sub:`n`\ (q)
        """
        super().__init__(n, q, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        if self.n == 1 and (self.q in [2,(2,1),3,(3,1)]):
            raise ValueError("(n,q) = (1,2) and (1,3) are not simple groups")

    def compute_order(self):
        q = self.q_value()
        order = q**((self.n * (self.n + 1)) // 2)
        order *= math.prod([q**(i+1)-1 for i in range(1,self.n+1)])
        order //= math.gcd(self.n + 1, q-1)
        return order

    def compute_multiplier(self):
        if self.n == 1:
            if self.q == 4 or self.q == (2,2):
                return 2
            if self.q == 9 or self.q == (3, 2):
                return 6
        if self.n == 2:
            if self.q == 2 or self.q == (2,1):
                return 2
            if self.q == 4 or self.q == (2,2):
                return 48
        if self.n == 3 and (self.q == 2 or self.q == (2,1)):
            return 2
        return math.gcd(self.n + 1, self.q_value() - 1)

    def code(self) -> str:
        if type(self.q) == tuple:
            return "CA-{0}-{1}_{2}".format(self.n, self.q[0], self.q[1])
        return "CA-{0}-{1}".format(self.n, self.q)

    def isomorphisms(self):
        if self.n == 1:
            if self.q == 4 or self.q == (2,2):
                return ["AA-5", "CA-1-5"]
            if self.q == 5 or self.q == (5,1):
                return ["AA-5", "CA-1-4"]
            if self.q == 7 or self.q == (7,1):
                return ["CA-2-2"]
            if self.q == 9 or self.q == (9,1):
                return ["AA-6"]
        if self.n == 2 and (self.q == 2 or self.q == (2,1)):
            return ["CA-1-7"]
        if self.n == 3 and (self.q == 2 or self.q == (2, 1)):
            return ["AA-8"]
        return []

    def latex_name(self) -> list[str]:
        if type(self.q) is int:
            q_string = f"{self.q}"
        else:
            q_string = f"{self.q[0]}^{{{self.q[1]}}}"
        psl_latex = f"{{\\rm PSL}}"
        return [f"A_{{{self.n}}}({q_string})", f"{psl_latex}_{{{self.n+1}}}({q_string})",
                f"{psl_latex}({self.n+1}, {q_string})", f"L_{{{self.n+1}}}({q_string})"]

    def GAP_name(self) -> str:
        return f"L{self.n + 1}({self.q_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        # We check if the current group is an exceptional case:
        exceptional_case = super().smallest_pirrep_degree()
        if not exceptional_case == (0,0):
            return exceptional_case
        # If the case is not exceptional, we compute the smallest pirrep degree for the Chevalley group:
        q = self.q_value()
        n = self.n + 1
        if self.n == 1:
            if q % 2 == 0:
                return q-1, q // 2
            return (q-1) // 2, 2
        return (q ** n - q) // (q - 1), 1


class ChevalleyB(BiParamSimpleGroup):
    def __init__(self, n: int, q: int | tuple[int, int], validate = True):
        """
        Class representing the classical Chevalley group |B_n(q)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        NOTE: The groups with parameters (n,q) = (2,2) or n = 1 are not simple groups.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. |B_n(q)| replace:: B\ :sub:`n`\ (q)
        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_An(q),_Bn(q)_n_>_1,_Cn(q)_n_>_2,_Dn(q)_n_>_3
        """
        super().__init__(n, q, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        if self.n <= 1:
            raise ValueError("n must be greater than 1")
        if self.n == 2 and self.q == 2:
            raise ValueError("The group B_2(2)=S_6 is not simple")

    def compute_order(self):
        q = self.q_value()
        order = q**(self.n * self.n)
        order *= math.prod([q**(2*i)-1 for i in range(1,self.n+1)])
        order //= math.gcd(2, q-1)
        return order

    def compute_multiplier(self):
        if self.n == 3:
            if self.q == 2 or self.q == (2,1):
                return 2
            if self.q == 3 or self.q == (3,1):
                return 6
        return math.gcd(2, self.q_value() - 1)

    def code(self)-> str:
        if type(self.q) == tuple:
            return "CB-{0}-{1}_{2}".format(self.n, self.q[0], self.q[1])
        return "CB-{0}-{1}".format(self.n, self.q)

    def isomorphisms(self):
        if type(self.q) == int:
            if Ph.is_power(self.q, 2):
                return ["CC-{0}-{1}".format(self.n, self.q)]
        else:
            if self.q[0] == 2:
                return ["CC-{0}-{1}_{2}".format(self.n, self.q[0], self.q[1])]
        if self.n == 2 and (self.q == 3 or self.q == (3,1)):
            return ["SA-3-2"]
        return []

    def latex_name(self) -> list[str]:
        if type(self.q) is int:
            q_string = f"{self.q}"
        else:
            q_string = f"{self.q[0]}^{{{self.q[1]}}}"
        return [f"B_{{{self.n}}}({q_string})", f"{{\\rm O}}_{{{2 * self.n + 1}}}({q_string})",
                f"\\Omega_{{{2 * self.n + 1}}}({q_string})"]

    def GAP_name(self) -> str:
        return f"O{2 * self.n + 1}({self.q_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        # We check if the current group is an exceptional case:
        exceptional_case = super().smallest_pirrep_degree()
        if not exceptional_case == (0,0):
            return exceptional_case
        # If the case is not exceptional, we compute the smallest pirrep degree for the Chevalley group:
        q = self.q_value()
        n = self.n
        if q == 3:
            return (q ** n - 1) * (q ** n - q) // (q ** 2 - 1), 1
        if q % 2 == 1:
            if n == 2:
                return (q ** n - 1) // 2, 2
            return (q ** (2 * n) - 1) // (q ** 2 - 1), 1
        return ((q ** n - 1) * (q ** n - q)) // (2 * (q + 1)), 1


class ChevalleyC(BiParamSimpleGroup):
    def __init__(self, n: int, q: int | tuple[int, int], validate = True):
        """
        Class representing the classical Chevalley group |C_n(q)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        NOTE: The parameter n must satisfy n > 2 for the group to be a valid simple group.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_An(q),_Bn(q)_n_>_1,_Cn(q)_n_>_2,_Dn(q)_n_>_3
        .. |C_n(q)| replace:: C\ :sub:`n`\ (q)
        """
        super().__init__(n, q, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        if self.n <= 2:
            raise ValueError("n must be greater than 2")

    def compute_order(self):
        q = self.q_value()
        order = q**(self.n * self.n)
        order *= math.prod([q**(2*i)-1 for i in range(1,self.n+1)])
        order //= math.gcd(2, q-1)
        return order

    def compute_multiplier(self):
        if self.n == 3 and (self.q == 2 or self.q == (2,1)):
            return 2
        return math.gcd(2, self.q_value() - 1)

    def code(self) -> str:
        if type(self.q) == tuple:
            return "CC-{0}-{1}_{2}".format(self.n, self.q[0], self.q[1])
        return "CC-{0}-{1}".format(self.n, self.q)

    def isomorphisms(self):
        if type(self.q) == int:
            if Ph.is_power(self.q, 2):
                return ["CB-{0}-{1}".format(self.n, self.q)]
        else:
            if self.q[0] == 2:
                return ["CB-{0}-{1}_{2}".format(self.n, self.q[0], self.q[1])]
        return []

    def latex_name(self) -> list[str]:
        if type(self.q) is int:
            q_string = f"{self.q}"
        else:
            q_string = f"{self.q[0]}^{{{self.q[1]}}}"
        return [f"C_{{{self.n}}}({q_string})", f"{{\\rm PSp}}_{{{2 * self.n}}}({q_string})",
                f"{{\\rm PSp}}({2 * self.n}, {q_string})"]

    def GAP_name(self) -> str:
        return f"S{2 * self.n}({self.q_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        # We check if the current group is an exceptional case:
        exceptional_case = super().smallest_pirrep_degree()
        if not exceptional_case == (0, 0):
            return exceptional_case
        # If the case is not exceptional, we compute the smallest pirrep degree for the Chevalley group:
        q = self.q_value()
        n = self.n
        if q % 2 == 0:
            return ((q ** n - 1) * (q ** n - q)) // (2 * (q + 1)), 1
        return (q ** n - 1) // 2, 2


class ChevalleyD(BiParamSimpleGroup):
    def __init__(self, n: int, q: int | tuple[int, int], validate = True):
        """
        Class representing the classical Chevalley group |D_n(q)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        NOTE: The parameter n must satisfy n > 3 for the group to be a valid simple group.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_An(q),_Bn(q)_n_>_1,_Cn(q)_n_>_2,_Dn(q)_n_>_3
        .. |D_n(q)| replace:: D\ :sub:`n`\ (q)
        """
        super().__init__(n, q, validate = validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        if self.n <= 3:
            raise ValueError("n must be greater than 3")

    def compute_order(self):
        q = self.q_value()
        order = (q**(self.n * (self.n - 1)))*(q**self.n - 1)
        order *= math.prod([q**(2*i)-1 for i in range(1,self.n)])
        order //= math.gcd(4, q**self.n - 1)
        return order

    def compute_multiplier(self):
        if self.n == 4 and (self.q == 2 or self.q == (2,1)):
            return 4
        return math.gcd(4, self.q_value()**self.n - 1)

    def code(self) -> str:
        if type(self.q) == tuple:
            return "CD-{0}-{1}_{2}".format(self.n, self.q[0], self.q[1])
        return "CD-{0}-{1}".format(self.n, self.q)

    def latex_name(self) -> list[str]:
        if type(self.q) is int:
            q_string = f"{self.q}"
        else:
            q_string = f"{self.q[0]}^{{{self.q[1]}}}"
        return [f"D_{{{self.n}}}({q_string})", f"{{\\rm O}}^+_{{{2 * self.n}}}({q_string})",
                f"{{\\rm O}}^+({{{2 * self.n}}}, {q_string})", f"{{\\rm P}}\\Omega^+_{{{2 * self.n}}}({q_string})",
                f"{{\\rm P}}\\Omega^+({{{2 * self.n}}}, {q_string})"]

    def GAP_name(self) -> str:
        return f"O{2 * self.n}+({self.q_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        # We check if the current group is an exceptional case:
        exceptional_case = super().smallest_pirrep_degree()
        if not exceptional_case == (0, 0):
            return exceptional_case
        # If the case is not exceptional, we compute the smallest pirrep degree for the group:
        q = self.q_value()
        n = self.n
        if q == 2 or q == (2,1):
            return (q ** n - 1) * (q ** (n - 1) - 1) // (q ** 2 - 1), 1
        if q == 3 or q == (3,1):
            return (q ** n - 1) * (q ** (n - 1) - 1) // (q ** 2 - 1), 2
        return (q ** n - 1) * (q ** (n - 1) + q) // (q ** 2 - 1), 1



class ExcetionalChevalleyE6(UniParamSimpleGroup):
    def __init__(self, q: int | tuple[int, int], validate = True):
        """
        Class representing the exceptional Chevalley group |E_6(q)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_E6(q),_E7(q),_E8(q),_F4(q),_G2(q)
        .. |E_6(q)| replace:: E\ :sub:`6`\ (q)
        """
        super().__init__(q, validate = validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        self.__validate_par__()

    def compute_order(self):
        q = self.par_value()
        order = q**36
        order *= math.prod([q**i-1 for i in CHEVALLEY_E6_POWER_INDICES])
        order //= math.gcd(3, q-1)
        return order

    def compute_multiplier(self):
        return math.gcd(3, self.par_value() - 1)

    def code(self) -> str:
        if type(self.par) == tuple:
            return "E6-{0}_{1}".format(self.par[0], self.par[1])
        return "E6-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        if type(self.par) is int:
            q_string = f"{self.par}"
        else:
            q_string = f"{self.par[0]}^{{{self.par[1]}}}"
        return [f"E_{{6}}({q_string})"]

    def GAP_name(self) -> str:
        return f"E6({self.par_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        q = self.par_value()
        return q * (q ** 6 + q ** 3 + 1) * (q ** 4 + 1), 1


class ExcetionalChevalleyE7(UniParamSimpleGroup):
    def __init__(self, q: int | tuple[int, int], validate = True):
        """
        Class representing the exceptional Chevalley group |E_7(q)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_E6(q),_E7(q),_E8(q),_F4(q),_G2(q)
        .. |E_7(q)| replace:: E\ :sub:`7`\ (q)
        """
        super().__init__(q, validate = validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        self.__validate_par__()

    def compute_order(self):
        q = self.par_value()
        order = q**63
        order *= math.prod([q**i-1 for i in CHEVALLEY_E7_POWER_INDICES])
        order //= math.gcd(2, q-1)
        return order

    def compute_multiplier(self):
        return math.gcd(2, self.par_value() - 1)

    def code(self) -> str:
        if type(self.par) == tuple:
            return "E7-{0}_{1}".format(self.par[0], self.par[1])
        return "E7-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        if type(self.par) is int:
            q_string = f"{self.par}"
        else:
            q_string = f"{self.par[0]}^{{{self.par[1]}}}"
        return [f"E_{{7}}({q_string})"]

    def GAP_name(self) -> str:
        return f"E7({self.par_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        q = self.par_value()
        return (q * (q ** 14 - 1) * (q ** 4 - q ** 2 + 1)) // (q ** 2 - 1), 1


class ExcetionalChevalleyE8(UniParamSimpleGroup):
    def __init__(self, q: int | tuple[int, int], validate = True):
        """
        Class representing the exceptional Chevalley group |E_8(q)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_E6(q),_E7(q),_E8(q),_F4(q),_G2(q)
        .. |E_8(q)| replace:: E\ :sub:`8`\ (q)
        """
        super().__init__(q, validate = validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        self.__validate_par__()

    def compute_order(self):
        q = self.par_value()
        order = q**120
        order *= math.prod([q**i-1 for i in CHEVALLEY_E8_POWER_INDICES])
        return order

    def compute_multiplier(self):
        return 1

    def code(self) -> str:
        if type(self.par) == tuple:
            return "E8-{0}_{1}".format(self.par[0], self.par[1])
        return "E8-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        if type(self.par) is int:
            q_string = f"{self.par}"
        else:
            q_string = f"{self.par[0]}^{{{self.par[1]}}}"
        return [f"E_{{8}}({q_string})"]

    def GAP_name(self) -> str:
        return f"E8({self.par_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        q = self.par_value()
        return q * (q ** 12 + 1) * (q ** 10 + 1) * (q ** 6 + 1), 1


class ExcetionalChevalleyF4(UniParamSimpleGroup):
    def __init__(self, q: int | tuple[int, int], validate = True):
        """
        Class representing the exceptional Chevalley group |F_4(q)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_E6(q),_E7(q),_E8(q),_F4(q),_G2(q)
        .. |F_4(q)| replace:: F\ :sub:`4`\ (q)
        """
        super().__init__(q, validate = validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        self.__validate_par__()

    def compute_order(self):
        q = self.par_value()
        order = q**24
        order *= math.prod([q**i-1 for i in CHEVALLEY_F4_POWER_INDICES])
        return order

    def compute_multiplier(self):
        if self.par == 2 or self.par == (2, 1):
            return 2
        return 1

    def code(self) -> str:
        if type(self.par) == tuple:
            return "F4-{0}_{1}".format(self.par[0], self.par[1])
        return "F4-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        if type(self.par) is int:
            q_string = f"{self.par}"
        else:
            q_string = f"{self.par[0]}^{{{self.par[1]}}}"
        return [f"F_{{4}}({q_string})"]

    def GAP_name(self) -> str:
        return f"F4({self.par_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        # We check if the current group is an exceptional case:
        exceptional_case = super().smallest_pirrep_degree()
        if not exceptional_case == (0, 0):
            return exceptional_case
        # If the case is not exceptional, we compute the smallest pirrep degree for the group:
        q = self.par_value()
        if q % 2 == 1:
            return q ** 8 + q ** 4 + 1, 1
        return (q * (q ** 4 + 1) * ((q ** 3 - 1) ** 2)) // 2, 1


class ExcetionalChevalleyG2(UniParamSimpleGroup):
    def __init__(self, q: int | tuple[int, int], validate = True):
        """
        Class representing the exceptional Chevalley group |G_2(q)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        NOTE: G_2(2) is not a simple group.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_E6(q),_E7(q),_E8(q),_F4(q),_G2(q)
        .. |G_2(q)| replace:: G\ :sub:`2`\ (q)
        """
        super().__init__(q, validate = validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        self.__validate_par__()
        if self.par == 2 or self.par == (2, 1):
            raise ValueError("The group G_2(2) is not simple")

    def compute_order(self):
        q = self.par_value()
        order = q**6
        order *= math.prod([q**i-1 for i in CHEVALLEY_G2_POWER_INDICES])
        return order

    def compute_multiplier(self):
        if self.par == 3 or self.par == (3, 1):
            return 3
        if self.par == 4 or self.par == (2, 2):
            return 2
        return 1

    def code(self):
        if type(self.par) == tuple:
            return "G2-{0}_{1}".format(self.par[0], self.par[1])
        return "G2-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        if type(self.par) is int:
            q_string = f"{self.par}"
        else:
            q_string = f"{self.par[0]}^{{{self.par[1]}}}"
        return [f"G_{{2}}({q_string})"]

    def GAP_name(self) -> str:
        return f"G2({self.par_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        # We check if the current group is an exceptional case:
        exceptional_case = super().smallest_pirrep_degree()
        if not exceptional_case == (0, 0):
            return exceptional_case
        # If the case is not exceptional, we compute the smallest pirrep degree for the group:
        q = self.par_value()
        if q % 3 == 1:
            return q ** 3 + 1, 1
        if q % 3 == 2:
            return q ** 3 - 1, 1
        return q ** 4 + q ** 2 + 1, 1


class Steinberg2A(BiParamSimpleGroup):
    def __init__(self, n: int, q: int | tuple[int, int], validate = True):
        """
        Class representing the classical Steinberg group |^2A_n(q^2)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        NOTE: The groups with parameters (n,q) = (2,2) and n = 1 are not simple groups.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Steinberg_groups,_2An(q2)_n_>_1,_2Dn(q2)_n_>_3,_2E6(q2),_3D4(q3)
        .. |^2A_n(q^2)| replace:: :sup:`2`\ A\ :sub:`n`\ (q\ :sup:`2`)
        """
        super().__init__(n, q, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        if self.n <= 1:
            raise ValueError("n must be greater than 3")
        if self.n == 2 and (self.q == 2 or self.q == (2,1)):
            raise ValueError("The group ^2A_2(2^2) is not a simple group")

    def compute_order(self):
        q = self.q_value()
        order = q**((self.n * (self.n + 1)) // 2)
        order *= math.prod([q**(i+1)-(-1)**(i+1) for i in range(1,self.n+1)])
        order //= math.gcd(self.n + 1, q+1)
        return order

    def compute_multiplier(self):
        if self.n == 3:
            if self.q == 2 or self.q == (2,1):
                return 2
            if self.q == 3 or self.q == (3,1):
                return 36
        if self.n == 5 and (self.q == 2 or self.q == (2,1)):
            return 12
        return math.gcd(self.n + 1, self.q_value() + 1)

    def code(self) -> str:
        if type(self.q) == tuple:
            return "SA-{0}-{1}_{2}".format(self.n, self.q[0], self.q[1])
        return "SA-{0}-{1}".format(self.n, self.q)

    def isomorphisms(self):
        if self.n == 3 and (self.q == 2 or self.q == (2,1)):
            return ["CB-2-3"]
        return []

    def latex_name(self) -> list[str]:
        if type(self.q) is int:
            q_string = f"{self.q}"
        else:
            q_string = f"{self.q[0]}^{{{self.q[1]}}}"
        psu_latex = f"{{\\rm PSU}}"
        return [f"{{}}^2A_{{{self.n}}}(({q_string})^2)", f"{{}}^2A_{{{self.n}}}({q_string})",
                f"{psu_latex}_{{{self.n + 1}}}({q_string})", f"{psu_latex}_({self.n + 1}, {q_string})",
                f"{{\\rm U}}_{{{self.n + 1}}}({q_string})", f"{{\\rm U}}({self.n + 1}, {q_string})"]

    def GAP_name(self) -> str:
        return f"U{self.n + 1}({self.q_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        # We check if the current group is an exceptional case:
        exceptional_case = super().smallest_pirrep_degree()
        if not exceptional_case == (0, 0):
            return exceptional_case
        # If the case is not exceptional, we compute the smallest pirrep degree for the group:
        q = self.q_value()
        n = self.n + 1
        if n % 2 == 0:
            return (q ** n - 1) // (q + 1), q
        return (q ** n - q) // (q + 1), 1


class Steinberg2D(BiParamSimpleGroup):
    def __init__(self, n: int, q: int | tuple[int, int], validate = True):
        """
        Class representing the classical Steinberg group |^2D_n(q^2)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        NOTE: The parameter n must satisfy n > 3 for the group to be simple.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Steinberg_groups,_2An(q2)_n_>_1,_2Dn(q2)_n_>_3,_2E6(q2),_3D4(q3)
        .. |^2D_n(q^2)| replace:: :sup:`2`\ D\ :sub:`n`\ (q\ :sup:`2`)
        """
        super().__init__(n, q, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        if self.n <= 3:
            raise ValueError("n must be greater than 3")

    def compute_order(self):
        q = self.q_value()
        order = (q**(self.n * (self.n - 1)))*(q**self.n + 1)
        order *= math.prod([q**(2*i)-1 for i in range(1,self.n)])
        order //= math.gcd(4, q**self.n + 1)
        return order

    def compute_multiplier(self):
        return math.gcd(4, self.q_value()**self.n + 1)

    def code(self):
        if type(self.q) == tuple:
            return "SD-{0}-{1}_{2}".format(self.n, self.q[0], self.q[1])
        return "SD-{0}-{1}".format(self.n, self.q)

    def latex_name(self) -> list[str]:
        if type(self.q) is int:
            q_string = f"{self.q}"
        else:
            q_string = f"{self.q[0]}^{{{self.q[1]}}}"
        return [f"{{}}^2D_{{{self.n}}}(({q_string})^2)", f"{{}}^2D_{{{self.n}}}({q_string})",
                f"{{\\rm O}}^-_{{{2 * self.n}}}({q_string})",
                f"{{\\rm O}}^-({{{2 * self.n}}}, {q_string})", f"{{\\rm P}}\\Omega^-_{{{2 * self.n}}}({q_string})",
                f"{{\\rm P}}\\Omega^-({{{2 * self.n}}}, {q_string})"]

    def GAP_name(self) -> str:
        return f"O{2 * self.n}-({self.q_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        # These groups contain no excetional cases, so we can proceed by applying the formula
        q = self.q_value()
        n = self.n
        return (q ** n + 1) * (q ** (n - 1) - q) // (q ** 2 - 1), 1


class ExcetionalSteinberg2E6(UniParamSimpleGroup):
    def __init__(self, q: int | tuple[int, int], validate = True):
        """
        Class representing the exceptional Steinberg group |^2E_6(q^2)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Steinberg_groups,_2An(q2)_n_>_1,_2Dn(q2)_n_>_3,_2E6(q2),_3D4(q3)
        .. |^2E_6(q^2)| replace:: :sup:`2`\ E\ :sub:`6`\ (q\ :sup:`2`)
        """
        super().__init__(q, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        self.__validate_par__()

    def compute_order(self):
        q = self.par_value()
        order = q**36
        order *= math.prod([q**i-(-1)**i for i in STEINBERG_2E6_POWER_INDICES])
        order //= math.gcd(3, q+1)
        return order

    def compute_multiplier(self):
        if self.par == 2 or self.par == (2, 1):
            return 12
        return math.gcd(3, self.par_value() + 1)

    def code(self):
        if type(self.par) == tuple:
            return "2E-{0}_{1}".format(self.par[0], self.par[1])
        return "2E-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        if type(self.par) is int:
            q_string = f"{self.par}"
        else:
            q_string = f"{self.par[0]}^{{{self.par[1]}}}"
        return [f"{{}}^2E_{{6}}(({q_string})^2)", f"{{}}^2E_{{6}}({q_string})"]

    def GAP_name(self) -> str:
        return f"2E6({self.par_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        q = self.par_value()
        return q * (q ** 6 - q ** 3 + 1) * (q ** 4 + 1), 1


class ExcetionalSteinberg3D4(UniParamSimpleGroup):
    def __init__(self, q: int | tuple[int, int], validate = True):
        """
        Class representing the exceptional Steinberg group |^3D_4(q^3)|, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Steinberg_groups,_2An(q2)_n_>_1,_2Dn(q2)_n_>_3,_2E6(q2),_3D4(q3)
        .. |^3D_4(q^3)| replace:: :sup:`3`\ D\ :sub:`4`\ (q\ :sup:`3`)
        """
        super().__init__(q, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()
        self.__validate_par__()

    def compute_order(self):
        q = self.par_value()
        return  math.prod([q ** 12, q**8 + q**4 + 1, q**6 - 1, q**2 - 1])

    def compute_multiplier(self):
        return 1

    def code(self):
        if type(self.par) == tuple:
            return "3D-{0}_{1}".format(self.par[0], self.par[1])
        return "3D-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        if type(self.par) is int:
            q_string = f"{self.par}"
        else:
            q_string = f"{self.par[0]}^{{{self.par[1]}}}"
        return [f"{{}}^3D_{{4}}(({q_string})^3)", f"{{}}^3D_{{4}}({q_string})"]

    def GAP_name(self) -> str:
        return f"3D4({self.par_value()})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        q = self.par_value()
        return q * (q ** 4 - q ** 2 + 1), 1


class Suzuki(UniParamSimpleGroup):
    def __init__(self, n: int, validate = True):
        """
        Class representing the Suzuki group |Suz(n)|, a simple group of Lie type. See `Wikipedia`_.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Suzuki_groups,_2B2(22n+1)
        .. |Suz(n)| replace:: :sup:`2`\ B\ :sub:`2`\ (2\ :sup:`2n+1`)
        """
        super().__init__(n, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()

    def compute_order(self):
        q = 2**(2 * self.par + 1)
        return  math.prod([q ** 2, q**2 + 1, q-1])

    def compute_multiplier(self):
        if self.par == 1:
            return 4
        return 1

    def code(self):
        return "SZ-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        return [f"{{}}^2B_2(2^{{{2 * self.par + 1}}})", f"Suz(2^{{{2 * self.par + 1}}})",
                f"Sz(2^{{{2 * self.par + 1}}})"]

    def GAP_name(self) -> str:
        return f"Sz({2 ** (2 * self.par + 1)})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        q = 2**(2 * self.par + 1)
        return (q - 1) * (2 ** self.par), 2


class Ree2F4(UniParamSimpleGroup):
    def __init__(self, n: int, validate = True):
        """
        Class representing the Ree group |ReeF(n)|, a simple group of Lie type. See `Wikipedia`_.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Ree_groups_and_Tits_group,_2F4(22n+1)
        .. |ReeF(n)| replace:: :sup:`2`\ F\ :sub:`4`\ (2\ :sup:`2n+1`)
        """
        super().__init__(n, validate=validate)
    def __validate_parameters__(self):
        super().__validate_parameters__()

    def compute_order(self):
        q = 2**(2 * self.par + 1)
        return  math.prod([q**12, q**6 + 1, q**4 - 1, q**3 + 1, q - 1])

    def compute_multiplier(self):
        return 1

    def code(self):
        return "RF-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        return [f"{{}}^2F_4(2^{{{2 * self.par + 1}}})"]

    def GAP_name(self) -> str:
        return f"2F4({2 ** (2 * self.par + 1)})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        q = 2**(2 * self.par + 1)
        return (q ** 3 + 1) * (q ** 2 - 1) * (2 ** self.par), 2


class Tits(SimpleGroup):
    def __init__(self):
        """
        Class representing the Tits group |Tits|, a simple group of Lie type. See `Wikipedia`_.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Ree_groups_and_Tits_group,_2F4(22n+1)
        .. |Tits| replace:: :sup:`2`\ F\ :sub:`4`\ (2\)'
        """
        super().__init__()

    def compute_order(self):
        return Ph.prime_reconstructor(TITS_ORDER)

    def compute_multiplier(self):
        return 1

    def code(self):
        return "TT"

    def latex_name(self) -> list[str]:
        return [f"{{}}^2F_4(2)\'"]

    def GAP_name(self) -> str:
        return f"2F4(2)\'"


class Ree2G2(UniParamSimpleGroup):
    def __init__(self, n: int, validate = True):
        """
        Class representing the Ree group |Ree(n)|, a simple group of Lie type. See `Wikipedia`_.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Ree_groups,_2G2(32n+1)
        .. |Ree(n)| replace:: :sup:`2`\ G\ :sub:`2`\ (3\ :sup:`2n+1`)
        """
        super().__init__(n, validate=validate)

    def __validate_parameters__(self):
        super().__validate_parameters__()

    def compute_order(self):
        q = 3**(2 * self.par + 1)
        return  math.prod([q**3, q**3 + 1, q - 1])

    def compute_multiplier(self):
        return 1

    def code(self):
        return "RG-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        return [f"{{}}^2G_2(3^{{{2 * self.par + 1}}})", f"Ree(3^{{{2 * self.par + 1}}})",
                f"R(3^{{{2 * self.par + 1}}})", f"E_2^*(3^{{{2 * self.par + 1}}})"]

    def GAP_name(self) -> str:
        return f"R({3 ** (2 * self.par + 1)})"

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        q = 3**(2 * self.par + 1)
        return q ** 2 - q + 1, 1

class Sporadic(SimpleGroup):
    def __init__(self, id_: str):
        """
        Class representing the Sporadic simple groups. See `Wikipedia`_.

        :param id_: A valid identification string corresponding to a sporadic group. All valid IDs can be consulted
            using SimpleGroups.Sporadic.id_list().

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Sporadic_groups
        """
        super().__init__()
        self.__id = id_
        self.validate_id()

    @classmethod
    def id_list(cls) -> list[str]:
        """
        Provides a list of all valid sporadic group identifiers.

        :return: All valid sporadic group identifiers.
        """
        return sporadic_group_ids()

    @property
    def id(self) -> str:
        """
        Returns the current sporadic group ID.
        :return: Sporadic group ID.
        """
        return self.__id

    def validate_id(self):
        """
        On object initialization, checks if the given ID corresponds to a sporadic simple group.

        :return: None.
        :raises ValueError: if given ID does not correspond to any sporadic group.
        """
        if self.id in self.id_list():
            return
        else:
            raise ValueError(f"There is no sporadic group with identifier: {self.id}, see Sporadic.id_list()")

    def compute_order(self):
        return Ph.prime_reconstructor(sporadic_lookup_property("id", self.id, "order"))

    def compute_multiplier(self):
        return sporadic_lookup_property("id", self.id, "multiplier")

    def code(self):
        if self.id == "Fi24\'":
            return "SP-Fi24\\\'"
        return "SP-{0}".format(self.id)

    def latex_name(self) -> list[str]:
        return sporadic_lookup_property("id", self.id, "latex_name")

    def GAP_name(self) -> str:
        return self.id

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        return sporadic_lookup_property("id", self.id, "smallest_pirrep_degree")


def simple_group(code):
    """
    Given a simple group code, returns a derived object of SimpleGroup corresponding to the provided code.

    For information on simple group codes, see the documentation of SimpleGroups.SimpleGroup.from_code.

    :param code: A valid simple group code.
    :return: A derived object of SimpleGroup corresponding to the provided code.
    """
    return SimpleGroup.from_code(code)


def simple_group_ids():
    """
    Returns a dictionary relating simple group IDs and their classes. IDs are the first two characters of a simple group
    code and serve to identify the family of simple groups. We list the IDs and the corresponding groups and number of
    parameters.

    Group notations taken from `Wikipedia`_.

    * Zero-parametric

        * "TT": Tits group |Tits|

    * Uniparametric

        * "CY": Simple cyclic groups C\ :sub:`p`
        * "AA": Alternating groups A\ :sub:`n`
        * "E6": Exceptional Chevalley groups |E6|
        * "E7": Exceptional Chevalley groups |E7|
        * "E8": Exceptional Chevalley groups |E8|
        * "F4": Exceptional Chevalley groups |F4|
        * "G2": Exceptional Chevalley groups |G2|
        * "2E": Exceptional Steinberg groups |2E|
        * "3D": Exceptional Steinberg groups |3D|
        * "SZ": Suzuki groups |SZ|
        * "RF": Ree groups |RF|
        * "RG": Ree groups |RG|

    * Biparametric

        * "CA": Classical Chevalley groups |CA|
        * "CB": Classical Chevalley groups |CB|
        * "CC": Classical Chevalley groups |CC|
        * "CD": Classical Chevalley groups |CD|
        * "SA": Classical Steinberg groups |SA|
        * "SD": Classical Steinberg groups |SD|

    :return: A dictionary relating group IDs and their classes.

    .. |Tits| replace:: :sup:`2`\ F\ :sub:`4`\ (2\)'
    .. |RG| replace:: :sup:`2`\ G\ :sub:`2`\ (3\ :sup:`2n+1`)
    .. |RF| replace:: :sup:`2`\ F\ :sub:`4`\ (2\ :sup:`2n+1`)
    .. |2E| replace:: :sup:`2`\ E\ :sub:`6`\ (q\ :sup:`2`)
    .. |3D| replace:: :sup:`3`\ D\ :sub:`4`\ (q\ :sup:`3`)
    .. |E6| replace:: E\ :sub:`6`\ (q)
    .. |E7| replace:: E\ :sub:`7`\ (q)
    .. |E8| replace:: E\ :sub:`8`\ (q)
    .. |F4| replace:: F\ :sub:`4`\ (q)
    .. |G2| replace:: G\ :sub:`2`\ (q)
    .. |SZ| replace:: :sup:`2`\ B\ :sub:`2`\ (2\ :sup:`2n+1`)
    .. |CA| replace:: A\ :sub:`n`\ (q)
    .. |CB| replace:: B\ :sub:`n`\ (q)
    .. |CC| replace:: C\ :sub:`n`\ (q)
    .. |CD| replace:: D\ :sub:`n`\ (q)
    .. |SA| replace:: :sup:`2`\ A\ :sub:`n`\ (q\ :sup:`2`)
    .. |SD| replace:: :sup:`2`\ D\ :sub:`n`\ (q\ :sup:`2`)
    .. _Wikipedia : https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Summary
    """
    return {"CA": ChevalleyA, "CB":ChevalleyB, "CC": ChevalleyC, "CD": ChevalleyD, "SA":Steinberg2A, "SP": Sporadic,
            "SD": Steinberg2D, "AA": Alternating, "E6": ExcetionalChevalleyE6, "E7": ExcetionalChevalleyE7,
            "E8": ExcetionalChevalleyE8, "F4": ExcetionalChevalleyF4, "G2": ExcetionalChevalleyG2, "TT": Tits,
            "2E": ExcetionalSteinberg2E6, "3D": ExcetionalSteinberg3D4, "SZ": Suzuki, "RF": Ree2F4, "RG": Ree2G2,
            "CY": Cyclic}


def sporadic_group_ids():
    """
    Returns a list with all sporadic simple group IDs. The notations have been taken from `Wikipedia`_.

    :return: A list with all sporadic simple group IDs.

    NOTE: The ID for the Fischer simple group Fi24' is "Fi24\'".

    .. _Wikipedia : https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Summary
    """
    with open("PrecomputedData/sporadic_groups_data.json", "r") as sporadic_data_file:
        sporadic_data = json.load(sporadic_data_file)
        return [group["id"] for group in sporadic_data]


def sporadic_lookup_property(field: str, match: Any, return_field: str) -> Any:
    """
    Helper function to look up a property of a sporadic group in the JSON file. Given a field and a match, it returns
    the value of the return field for the matching group. If no match is found, it returns None.

    :param field: Field to look up.
    :param match: Value to match for the given field.
    :param return_field: Field to return if a match is found.
    :return: The value of the given return field if a match is found, otherwise None.
    """
    with open("PrecomputedData/sporadic_groups_data.json", "r") as sporadic_data_file:
        sporadic_data = json.load(sporadic_data_file)
        try:
            return next(group for group in sporadic_data if group[field] == match)[return_field]
        except StopIteration:
            logging.warning(f"No match found for {field}={match}")
            return None