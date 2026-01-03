"""
Module implementing simple group objects.
"""

import bz2
import json
import logging
import math
import FiSGO.PrimesHandler as Ph
import re
from typing import Any
import importlib.resources as ires

# TODO: Module documentation
# TODO: Alternating groups smallest pirrep degree
# TODO: Lubeck docstrings
# TODO: Handle groups with exceptional multipliers

GLOBAL_VALIDATE = True

PRECOMPUTED_DATA_DIR = ires.files("FiSGO.PrecomputedData")

TITS_ORDER = [11, 3, 2, 0, 0, 1]

CHEVALLEY_E6_POWER_INDICES = [2,5,6,8,9,12]
CHEVALLEY_E7_POWER_INDICES = [2,6,8,10,12,14,18]
CHEVALLEY_E8_POWER_INDICES = [2,8,12,14,18,20,24,30]
CHEVALLEY_F4_POWER_INDICES = [2,6,8,12]
CHEVALLEY_G2_POWER_INDICES = [2,6]
STEINBERG_2E6_POWER_INDICES = [2,5,6,8,9,12]

EXCEPTIONAL_MULTIPLIER_CODES = ["CA-1-2_2", "CA-1-3_2", "CA-2-2_1", "CA-2-2_2", "CA-3-2_1",
                                "CB-3-2_1", "CB-3-3_1", "CC-3-2_1", "CD-4-2_1", "F4-2_1",
                                "G2-3_1", "G2-2_2", "SA-3-2_1", "SA-3-3_1", "SA-5-2_1",
                                "2E-2_1", "SZ-1"]


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

        .. caution:: The name of the Fischer group 24' is "Fi24\'", if printed, it will show "Fi24'" as the character "'" is
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
            raise ValueError(f"{code} is an invalid simple group identifier")

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
        return code_normalizer(self.code())

    def smallest_pirrep_degree(self) -> tuple[int, int | None]:
        """
        Using the bounds of Seitz, Landazuri, Tiep and Zalesskii, returns the degree of the smallest non-trivial
        projective irreducible complex representation of the simple group. Furthermore, it also returns the number of
        different representations of that degree.

        .. caution:: In the case of the alternating groups, only the smallest degree is currently implemented,
            the number of different representations is given as None.

        :return: The degree of the smallest non-trivial complex projective representation and the number of different
            representations of that degree.
        """
        # We first handle the possible exceptions
        with PRECOMPUTED_DATA_DIR.joinpath("smallest_pirrep_degree_exceptions.json").open('r') as exceptions_file:
            for exception in json.load(exceptions_file):
                if self.code() in exception["code"]:
                    return exception["degree"], exception["irreps"]
        # Non-exceptional cases are handled in the derived classes
        return 0, 0

    def hiss_malle_pirreps(self, char: int | None = 0, all_pirrep_data: bool=False, allow_duplicates: bool=False) -> list[int | dict]:
        """
        This function looks for projective representations of degree up to 250.

        The representations are obtained from the tables given by Gerard Hiss and Gunter Malle in [HM1]_ and [HM2]_.
        By default, it returns a list with all degrees (less than 251) of the simple group's characteristic zero pirreps.

        Information of positive characteristic absolutely irreducible represenations can be obtained by changing the char parameter.
        Furthermore, if char is set to None, it returns all the information available for the simple group as a list of dicts,
        which can be parsed into a JSON file.

        For a fixed characteristic, all information on the pirreps can be obtained by setting all_pirrep_data to True. Again,
        as a list of dicts which can be parsed into a JSON file.

        Finally, it is possible for different covers of a simple group to produce different projective representations of the same
        degree. As such, it is possible that the returned list of degrees may contain duplicates. If this is desired,
        for instance, to detect this phenomenon, set allow_duplicates to True.

        :param char: Characteristic in which to look for projective (absolutely) irreps. If None, it will look for all projective
            absolutely irreducible represenations, regardless of the characteristic, and return all available information
            as a list of dicts. By default, char is 0.
        :param all_pirrep_data: False by default. If True, it will return all the information available for each representation and return
            a list of dicts. If False, it will return only the degrees of the simple group's pirreps. This parameter is
            ignored if char is None.
        :param allow_duplicates: False by default. If True, it will allow duplicates in the returned list of degrees.
            This parameter is ignored if all_pirrep_data is True or if char is None.
        :return: By default, a list of degrees less than 251 of the simple group's pirreps in characteristic 0. See the
            parameters' description for more details on changing the function's output.

        .. [HM1] Hiss, G., & Malle, G. (2001). Low-Dimensional Representations of Quasi-Simple Groups. LMS Journal of Computation
            and Mathematics, 4, 22–63.
        .. [HM2] Hiss, G., & Malle, G. (2002). Corrigenda: Low-dimensional Representations of Quasi-simple Groups.
            LMS Journal of Computation and Mathematics, 5, 95–126.
        """
        match_values = [{"code": code} for code in [self.normalized_code()] + self.isomorphisms()]
        # We first define the return fields, if char is None, we want all data
        if all_pirrep_data or char is None:
            return_fields = None
        else:
            return_fields = ["degree", "char", "not_char"]
        data = []
        for match_code in match_values:
            data += hiss_malle_lookup(match_code, return_fields)
        # If we want all pirreps for any characteristic
        if char is None:
            return data
        # We now filter the pirreps to match the characteristic
        matches = []
        for pirrep in data:
            if char_check(char, pirrep["char"], pirrep["not_char"]):
                matches.append(pirrep)
        # We now select the data to return
        if all_pirrep_data:
            return matches
        if allow_duplicates:
            return sorted(pirrep["degree"] for pirrep in matches)
        return sorted(set(pirrep["degree"] for pirrep in matches))

    def lubeck_pirreps(self):
        """
        This function computes projective representations of Lie type groups of rank at most 8.

        :return: If available, returns a list of pairs containing the projective representations of the
            group alongside their multiplicities in the Schur covering.
        """
        return []


class UniParamSimpleGroup(SimpleGroup):
    def __init__(self, par: int | tuple[int, int], validate=True):
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

    def lubeck_pirreps(self):
        # Lübeck's data only concerns Lie type groups
        code = self.code()[:2]
        if code in ["AA", "CY"]:
            return []
        # We take exceptions into account
        if self.normalized_code() in EXCEPTIONAL_MULTIPLIER_CODES:
            return []
        data = lubeck_data(code)[code]
        mod_group = modularity_group(self, data, "uni")
        pirreps_data = data["irreps"][mod_group]
        pirreps = []
        # The process is different if the group is of RF,RG or SZ type
        if code in ["RF", "SZ", "RG"]:
            if code == "RG":
                sqrt_value = 3
            else:
                sqrt_value = 2
            for pirrep in pirreps_data:
                mult = _sqrt_horner(pirrep["mult"], self.par, val=sqrt_value)
                if mult != 0:
                    degree = _sqrt_horner(pirrep["degree"], self.par, val=sqrt_value)
                    pirreps.append([degree, mult])
        else:
            for pirrep in pirreps_data:
                mult = _horner(pirrep["mult"], self.par_value())
                if mult != 0:
                    degree = _horner(pirrep["degree"], self.par_value())
                    pirreps.append([degree, mult])
        return pirreps


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

    def lubeck_pirreps(self):
        # We take exceptions into account
        if self.normalized_code() in EXCEPTIONAL_MULTIPLIER_CODES:
            return []
        # The available data is only up to rank 8
        if self.n > 8:
            return []
        code = self.code()[:2]
        data = lubeck_data(code)[f"{code}-{self.n}"]
        mod_group = modularity_group(self, data, "bi")
        pirreps_data = data["irreps"][mod_group]
        pirreps = []
        # The process is different if the group is of RF,RG or SZ type
        for pirrep in pirreps_data:
            mult = _horner(pirrep["mult"], self.q_value())
            if mult != 0:
                degree = _horner(pirrep["degree"], self.q_value())
                pirreps.append([degree, mult])
        return pirreps


class Cyclic(UniParamSimpleGroup):
    def __init__(self, n: int, validate = True):
        """
        Class representing the Cyclic group :math:`\\mathrm{C}_n`, a simple group when n is prime. See `Wikipedia`_.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param int n: Positive integer.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Cyclic_groups,_Zp
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

    def normalized_code(self):
        return self.code()


class Alternating(UniParamSimpleGroup):
    def __init__(self, n: int, validate = True):
        """
        Class representing the Alternating group :math:`\\mathrm{A}_n`, a simple group when n > 4. See `Wikipedia`_.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param int n: Positive integer.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Alternating_groups,_An,_n_>_4
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
            return ["CA-1-2_2", "CA-1-5_1"]
        if self.par == 6:
            return ["CA-1-3_2"]
        if self.par == 8:
            return ["CA-3-2_1"]
        return []

    def code(self) -> str:
        return "AA-{0}".format(self.par)

    def latex_name(self) -> list[str]:
        return [f"A_{{{self.par}}}", f"{{\\rm A}}_{{{self.par}}}", f"{{\\frak A}}_{{{self.par}}}",
                f"{{\\rm Alt}}_{{{self.par}}}"]

    def GAP_name(self) -> str:
        return f"A{self.par}"

    def normalized_code(self):
        return self.code()

    def smallest_pirrep_degree(self) -> tuple[int, int | None]:
        # We check if the current group is an exceptional case:
        exceptional_case = super().smallest_pirrep_degree()
        if not exceptional_case == (0, 0):
            return exceptional_case
        return self.par-1, None


class ChevalleyA(BiParamSimpleGroup):
    def __init__(self, n: int, q: int | tuple[int, int], validate = True):
        """
        Class representing the classical Chevalley group :math:`A_n(q)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        .. note:: The groups with parameters (n,q) = (1,2) and (1,3) are not simple groups.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_An(q),_Bn(q)_n_>_1,_Cn(q)_n_>_2,_Dn(q)_n_>_3
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
                return ["AA-5", "CA-1-5_1"]
            if self.q == 5 or self.q == (5,1):
                return ["AA-5", "CA-1-2_2"]
            if self.q == 7 or self.q == (7,1):
                return ["CA-2-2_1"]
            if self.q == 9 or self.q == (9,1):
                return ["AA-6"]
        if self.n == 2 and (self.q == 2 or self.q == (2,1)):
            return ["CA-1-7_1"]
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
        Class representing the classical Chevalley group :math:`B_n(q)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        .. note:: The groups with parameters (n,q) = (2,2) or n = 1 are not simple groups.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

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
                return [code_normalizer("CC-{0}-{1}".format(self.n, self.q))]
        else:
            if self.q[0] == 2:
                return ["CC-{0}-{1}_{2}".format(self.n, self.q[0], self.q[1])]
        if self.n == 2 and (self.q == 3 or self.q == (3,1)):
            return ["SA-3-2_1"]
        return []

    def latex_name(self) -> list[str]:
        if type(self.q) is int:
            q_string = f"{self.q}"
        else:
            q_string = f"{self.q[0]}^{{{self.q[1]}}}"
        if self.q_value() % 2 == 0:
            return [f"B_{{{self.n}}}({q_string})"]
        elif self.n == 2:
            return [f"B_{{{self.n}}}({q_string})", f"{{\\rm PSp}}_{{{2 * self.n}}}({q_string})",
                    f"{{\\rm PSp}}({2 * self.n}, {q_string})", f"{{\\rm O}}_{{{2 * self.n + 1}}}({q_string})",
                    f"\\Omega_{{{2 * self.n + 1}}}({q_string})"]
        else:
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
        Class representing the classical Chevalley group :math:`C_n(q)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        .. note:: The parameter n must satisfy n > 2 for the group to be a valid simple group.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_An(q),_Bn(q)_n_>_1,_Cn(q)_n_>_2,_Dn(q)_n_>_3
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
                return [code_normalizer("CB-{0}-{1}".format(self.n, self.q))]
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
        Class representing the classical Chevalley group :math:`D_n(q)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        .. note:: The parameter n must satisfy n > 3 for the group to be a valid simple group.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_An(q),_Bn(q)_n_>_1,_Cn(q)_n_>_2,_Dn(q)_n_>_3
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
        Class representing the exceptional Chevalley group :math:`E_6(q)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_E6(q),_E7(q),_E8(q),_F4(q),_G2(q)
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
        Class representing the exceptional Chevalley group :math:`E_7(q)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_E6(q),_E7(q),_E8(q),_F4(q),_G2(q)
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
        Class representing the exceptional Chevalley group :math:`E_8(q)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_E6(q),_E7(q),_E8(q),_F4(q),_G2(q)
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
        Class representing the exceptional Chevalley group :math:`F_4(q)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_E6(q),_E7(q),_E8(q),_F4(q),_G2(q)
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
        Class representing the exceptional Chevalley group :math:`G_2(q)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        .. note:: :math:`G_2(2)` is not a simple group.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Chevalley_groups,_E6(q),_E7(q),_E8(q),_F4(q),_G2(q)
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
        Class representing the classical Steinberg group :math:`{}^2A_n(q^2)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        .. note:: The groups with parameters (n,q) = (2,2) and n = 1 are not simple groups.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Steinberg_groups,_2An(q2)_n_>_1,_2Dn(q2)_n_>_3,_2E6(q2),_3D4(q3)
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
            return ["CB-2-3_1"]
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
        Class representing the classical Steinberg group :math:`{}^2D_n(q^2)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        .. note:: The parameter n must satisfy n > 3 for the group to be simple.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, dimensional parameter of the group.
        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Steinberg_groups,_2An(q2)_n_>_1,_2Dn(q2)_n_>_3,_2E6(q2),_3D4(q3)
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
        Class representing the exceptional Steinberg group :math:`{}^2E_6(q^2)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Steinberg_groups,_2An(q2)_n_>_1,_2Dn(q2)_n_>_3,_2E6(q2),_3D4(q3)
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
        Class representing the exceptional Steinberg group :math:`{}^3D_4(q^3)`, a simple group of Lie type. See `Wikipedia`_.

        The q parameter is a prime power and can be given as an integer or a pair of integers. Example: q = 9 and
        q=(3,2) represent the same parameter as 9 = 3**2. The latter format is preferred when dealing with large powers.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param q: Positive integer or tuple of positive integers. Prime power, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Steinberg_groups,_2An(q2)_n_>_1,_2Dn(q2)_n_>_3,_2E6(q2),_3D4(q3)
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
        Class representing the Suzuki group :math:`{}^2B_2(2^{2n+1})`, a simple group of Lie type. See `Wikipedia`_.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Suzuki_groups,_2B2(22n+1)
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

    def normalized_code(self):
        return self.code()


class Ree2F4(UniParamSimpleGroup):
    def __init__(self, n: int, validate = True):
        """
        Class representing the Ree group :math:`{}^2F_4(2^{2n+1})`, a simple group of Lie type. See `Wikipedia`_.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Ree_groups_and_Tits_group,_2F4(22n+1)
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

    def normalized_code(self):
        return self.code()

class Tits(SimpleGroup):
    def __init__(self):
        """
        Class representing the Tits group :math:`{}^2F_4(2)'`, a simple group of Lie type. See `Wikipedia`_.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Ree_groups_and_Tits_group,_2F4(22n+1)
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
        Class representing the Ree group :math:`{}^2G_2(3^{2n+1})`, a simple group of Lie type. See `Wikipedia`_.

        On object initialization, if validate is True (default), it will attempt to check if the introduced parameters
        are valid. Parameter validation can be globally disabled by changing GLOBAL_VALIDATE to False.

        :param n: Positive integer, finite field parameter of the group.
        :param bool validate: Boolean. If True, it will attempt to validate the given parameters on object initialization;
            if False, it will skip any checks.

        .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Ree_groups,_2G2(32n+1)
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

    def normalized_code(self):
        return self.code()


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
            print(self.id)
            raise ValueError(f"There is no sporadic group with identifier: {self.id}, see Sporadic.id_list()")

    def compute_order(self):
        return Ph.prime_reconstructor(sporadic_lookup_property("id", self.id, "order"))

    def compute_multiplier(self):
        return sporadic_lookup_property("id", self.id, "multiplier")

    def code(self):
        if self.id == r"Fi24'":
            return r"SP-Fi24'"
        return "SP-{0}".format(self.id)

    def latex_name(self) -> list[str]:
        return sporadic_lookup_property("id", self.id, "latex_name")

    def GAP_name(self) -> str:
        return self.id

    def smallest_pirrep_degree(self) -> tuple[int, int]:
        pirreps = sporadic_lookup_property("id", self.id, "pirreps")
        min_irrep_covers = []
        for pirrep in pirreps:
            if pirrep["name"] == self.id:
                # This one contains the trivial irrep, so we ignore it
                min_irrep_covers.append(sorted(pirrep["degrees"], key=lambda l: l[0])[1])
            else:
                min_irrep_covers.append(sorted(pirrep["degrees"], key=lambda l: l[0])[0])
        min_rep = [min(min_irrep_covers)[0], 0]
        for pair in min_irrep_covers:
            if pair[0] == min_rep[0]:
                min_rep[1] += pair[1]
        return min_rep[0], min_rep[1]

    def normalized_code(self) -> str:
        return self.code()

    def pirrep_degrees(self, include_cover: bool=False) \
            -> list[int] | list[tuple[int, str]]:
        """
        Returns a list with the degrees the sporadic group's projective irreducible representations in characteristic 0.

        If include_cover is True, the list will include the name of the covering group producing the pirrep. This
        is given in the form of a tuple with the first element being the degree, and the second the name of the
        covering group.

        :param include_cover: If True, the list will include the name of the covering group producing the pirrep.
        :return: A list with the degrees of the projective irreducible representations in characteristic 0. If include_cover
            is True, the list will include the name of the covering group.
        """
        pirreps = sporadic_lookup_property("id", self.id, "pirreps")
        if include_cover:
            degrees = []
            for pirrep in pirreps:
                degrees += [(pair[0], pirrep["name"]) for pair in pirrep["degrees"]]
            return list(sorted(degrees))
        else:
            degrees = []
            for pirrep in pirreps:
                degrees += [pair[0] for pair in pirrep["degrees"]]
            return list(sorted(set(degrees)))


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

        * "TT": Tits group :math:`{}^2F_4(2)'`

    * Uniparametric

        * "CY": Simple cyclic groups :math:`\\mathrm{C}_n`
        * "AA": Alternating groups :math:`\\mathrm{A}_n`
        * "E6": Exceptional Chevalley groups :math:`E_6(q)`
        * "E7": Exceptional Chevalley groups :math:`E_7(q)`
        * "E8": Exceptional Chevalley groups :math:`E_8(q)`
        * "F4": Exceptional Chevalley groups :math:`F_4(q)`
        * "G2": Exceptional Chevalley groups :math:`G_2(q)`
        * "2E": Exceptional Steinberg groups :math:`{}^2E_6(q^2)`
        * "3D": Exceptional Steinberg groups :math:`{}^3D_4(q^3)`
        * "SZ": Suzuki groups :math:`{}^2B_2(2^{2n+1})`
        * "RF": Ree groups :math:`{}^2F_4(2^{2n+1})`
        * "RG": Ree groups :math:`{}^2G_2(3^{2n+1})`

    * Biparametric

        * "CA": Classical Chevalley groups :math:`A_n(q)`
        * "CB": Classical Chevalley groups :math:`B_n(q)`
        * "CC": Classical Chevalley groups :math:`C_n(q)`
        * "CD": Classical Chevalley groups :math:`D_n(q)`
        * "SA": Classical Steinberg groups :math:`{}^2A_n(q^2)`
        * "SD": Classical Steinberg groups :math:`{}^2D_n(q^2)`

    .. caution:: The Fischer 24\' group should be written as :code:`r"SP-Fi24'"` for proper handling of the \' character.

    :return: A dictionary relating group IDs and their classes.

    .. _Wikipedia : https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Summary
    """
    return {"CA": ChevalleyA, "CB":ChevalleyB, "CC": ChevalleyC, "CD": ChevalleyD, "SA":Steinberg2A, "SP": Sporadic,
            "SD": Steinberg2D, "AA": Alternating, "E6": ExcetionalChevalleyE6, "E7": ExcetionalChevalleyE7,
            "E8": ExcetionalChevalleyE8, "F4": ExcetionalChevalleyF4, "G2": ExcetionalChevalleyG2, "TT": Tits,
            "2E": ExcetionalSteinberg2E6, "3D": ExcetionalSteinberg3D4, "SZ": Suzuki, "RF": Ree2F4, "RG": Ree2G2,
            "CY": Cyclic}


def sporadic_groups_data():
    """
    Interface to the compressed JSON file sporadic_grous_data.json.bz2.

    The file contains data on the sporadic groups, including their codes, IDs, order, multiplier, pirreps and
    latex names.

    For more information on the data, see the README's of `PrecomputedData`_.

    The data can be accessed as a list of dictionaries, each dictionary having the same fields (keys).

    :return: Returns a decoded JSON object, i.e., a list of dictionaries with all the data of the file.

    .. _PrecomputedData: https://github.com/GeraGC/FiSGO/tree/master/FiSGO/PrecomputedData
    """
    with ires.as_file(PRECOMPUTED_DATA_DIR.joinpath('sporadic_groups_data.json.bz2')) as sporadic_data_path:
        with bz2.open(sporadic_data_path, 'rt') as sporadic_data_file:
            sporadic_data = json.load(sporadic_data_file)
    return sporadic_data

def sporadic_group_ids():
    """
    Returns a list with all sporadic simple group IDs. The notations have been taken from `Wikipedia`_.

    :return: A list with all sporadic simple group IDs.

    .. note:: The ID for the Fischer simple group Fi24' is :code:`r"Fi24'"`.

    .. _Wikipedia : https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Summary
    """
    return [group["id"] for group in sporadic_groups_data()]


def sporadic_lookup_property(field: str, match: Any, return_field: str) -> Any:
    """
    Helper function to look up a property of a sporadic group in the JSON file. Given a field and a match, it returns
    the value of the return field for the matching group. If no match is found, it returns None.

    :param field: Field to look up.
    :param match: Value to match for the given field.
    :param return_field: Field to return if a match is found.
    :return: The value of the given return field if a match is found, otherwise None.
    """
    try:
        return next(group for group in sporadic_groups_data() if group[field] == match)[return_field]
    except StopIteration:
        logging.warning(f"No match found for {field}={match}")
        return None


def hiss_malle_data():
    """
    Interface to the compressed JSON file Hiss_Malle_data.json.bz2.

    The file contains data on representations of degree less than 250, compiled by Gerard Hiss and Gunter Malle
    in [HM1]_ and [HM2]_.
    For more information on the data, see the README's of `HissMalleTableFormats`_ or `PrecomputedData`_.

    The data can be accessed as a list of dictionaries, each dictionary having the same fields (keys).

    :return: Returns a decoded JSON object, i.e., a list of dictionaries with all the data of the file.

    .. _PrecomputedData: https://github.com/GeraGC/FiSGO/tree/master/FiSGO/PrecomputedData
    .. _HissMalleTableFormats: https://github.com/GeraGC/FiSGO/tree/master/HissMalleTableFormats

    .. [HM1] Hiss, G., & Malle, G. (2001). Low-Dimensional Representations of Quasi-Simple Groups. LMS Journal of Computation
        and Mathematics, 4, 22–63.
    .. [HM2] Hiss, G., & Malle, G. (2002). Corrigenda: Low-dimensional Representations of Quasi-simple Groups.
        LMS Journal of Computation and Mathematics, 5, 95–126.
    """

    with ires.as_file(PRECOMPUTED_DATA_DIR.joinpath('Hiss_Malle_data.json.bz2')) as hiss_malle_data_path:
        with bz2.open(hiss_malle_data_path, 'rt') as hiss_malle_data_file:
            return json.load(hiss_malle_data_file)


def hiss_malle_lookup(match_values: dict, return_fields: list | None):
    """
    A function to browse the file containing data on representations of degree less than 250, compiled by Gerard Hiss and Gunter Malle
    in [HM1]_ and [HM2]_.

    The data can be filtered using a dictionary of field:value pairs given as the first argument.
    The second argument can be used to specify which fields of the matching object are to be returned. If None, all fields are returned.

    For more information on the accessible data, see the README's of `HissMalleTableFormats`_ or `PrecomputedData`_.

    :param match_values: A dictionary of field:value pairs to filter the data.
    :param return_fields: A list of fields to return. If None, all fields are returned.
    :return: Returns a list of dictionaries. Each dictionary corresponds to a representation mathcing the parameters given in match_values.
        The contents of each dictionary correspond to the fields specified in return_fields.

    .. _PrecomputedData: https://github.com/GeraGC/FiSGO/tree/master/FiSGO/PrecomputedData
    .. _HissMalleTableFormats: https://github.com/GeraGC/FiSGO/tree/master/HissMalleTableFormats

    .. [HM1] Hiss, G., & Malle, G. (2001). Low-Dimensional Representations of Quasi-Simple Groups. LMS Journal of Computation
        and Mathematics, 4, 22–63.
    .. [HM2] Hiss, G., & Malle, G. (2002). Corrigenda: Low-dimensional Representations of Quasi-simple Groups.
        LMS Journal of Computation and Mathematics, 5, 95–126.
    """
    return _json_request(hiss_malle_data(), match_values, return_fields)


def lubeck_data(code:str):
    """
        Interface to the compressed JSON files Lubeck_[code].json.bz2.

        The parameter 'code' refers to one of the group codes of the Lie type groups. For example,
        file 'Lubeck_CA.json.bz2' refers to the Chevalley type A group data.

        The files contain data on projective representations degrees and multiplicities for the Lie type
        groups with non-exceptional Schur multipliers.
        For more information on the data, see the README's of `PrecomputedData`_.

        The data can be accessed as a list of dictionaries, each dictionary having the same fields (keys).

        :return: Returns a decoded JSON object, i.e., a list of dictionaries with all the data of the file.

        .. _PrecomputedData: https://github.com/GeraGC/FiSGO/tree/master/FiSGO/PrecomputedData
    """
    with ires.as_file(PRECOMPUTED_DATA_DIR.joinpath(f'Lubeck/Lubeck_{code}.json.bz2')) as lubeck_data_path:
        with bz2.open(lubeck_data_path, 'rt') as lubeck_data_file:
            return json.load(lubeck_data_file)


def code_normalizer(code: str) -> str:
    """
    Given a simple group code, returns a normalized version of the code. Normalization is done by replacing the

    :param code: The code to normalize.
    :return: Normalized code.
    """
    if "_" in code:
        # Code is already in a normalized form.
        return code
    code_split = code.split("-")
    if code.count("-") == 2:
        # The code corresponds to a biparametric group
        q = int(code_split[-1])
        factors = list(Ph.factor(q)[0].items())[0]
        return f"{code_split[0]}-{code_split[1]}-{factors[0]}_{factors[1]}"
    # The code corresponds to an uniparametric group
    if code_split[0] in ["AA", "CY", "SZ", "RF", "TT", "SP", "RG"]:
        return code
    factors, res = Ph.factor(int(code_split[-1]))
    return f"{code_split[0]}-{list(factors.items())[0][0]}_{list(factors.items())[0][1]}"


def _json_request(loaded_json: list[dict] | dict, match_values: dict, return_fields: list | None) -> list[dict]:
    """
    Helper function to bulk request data from a JSON file with either a single object or a list of objects containing the
    same fields. Given a loaded JSON object in the form of a list or dictionary,
    a dictionary of match values, and a list of return fields, it returns a list of dictionaries with the specified return
    fields for the objects matching the given match values.

    :param loaded_json: A loaded JSON file, a list of dictionaries or a dictionary.
    :param match_values: A dictionary of fields to match.
    :param return_fields: A list of fields to return for a matching object or None. If None, all fields are returned.
    :return: A list of dictionaries with the specified return fields for the objects matching the given match values.
    """
    if isinstance(loaded_json, dict):
        loaded_json = [loaded_json]
    if return_fields is None:
        return_fields = list(loaded_json[0].keys())
    matches = []
    for obj in loaded_json:
        match = True
        for field, match_value in match_values.items():
            if obj[field] != match_value:
                match = False
                break
        if match:
            matches.append({field: obj[field] for field in return_fields})
    return matches


def char_check(char: int, char_list: list[int] | None, not_char_list: list[int] | None) -> bool:
    """
    Helper function to check if a hiss-malle representation exists in a given characteristic.

    :param char: Characteristic in which to check existence.
    :param char_list: "char" field of the representation.
    :param not_char_list: "not_char" field of the representation.
    :return: True if the representation exists in characteristic char, otherwise False.
    """
    # If both fields are null, then all characteristics admit the representation
    if char_list is None and not_char_list is None:
        return True
    # If char_list is not null, then only the characteristics in char_list admit the representation
    if char_list is not None:
        if char in char_list:
            return True
    # If not_char_list is not null, then only the characteristics not in not_char_list do not admit the representation
    if not_char_list is not None:
        if char not in not_char_list:
            return True
    return False


def _horner(poly: list, x: int):
    """Horner's method to compute Lübeck's pirreps"""
    result = poly[0][0]
    for coef in poly[0][1:]:
        result = result*x + coef
    return result // poly[1]

def _sqrt_horner(poly_list: list, m: int, val: int=2):
    """Horner's method to compute Lübeck's pirreps for RF, RG and SZ groups."""
    # First poly is the even one, second poly is the odd one
    # We have q^2 = val^(val*m+1), val=2 when RF and SZ, val=3 for RG
    x = val**(2*m+1)
    even_value = _horner(poly_list[0], x)
    odd_value = _horner(poly_list[1], x)
    return odd_value*(val**(m+1))+even_value

def modularity_group(group, data, group_type):
    """
    Auxiliary function to find the modularity class of some group in Lübeck's data.

    :param group: The simple group object whose modularity class we ought to find.
    :param data: Dictionary with the Lübeck data of the group
    :param group_type: "uni" if uniparametric, "bi" if biparametric
    :return: The modularity class "mod_group"
    """
    mod_value = data["mod"]
    # We look for the modularity group of our parameter
    if mod_value == 0:
        return "0"

    if group_type == "uni":
        q_mod = group.par_value() % mod_value
    elif group_type == "bi":
        q_mod = group.q_value() % mod_value

    for key, mods in data["mod_groups"].items():
        if q_mod in mods:
            return key
    return None