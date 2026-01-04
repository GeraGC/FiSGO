"""
Module implementing the search of projective irreducible representations.
"""
import logging
import sys
import math
from typing import Any

import FiSGO.SimpleGroups as Sg
import FiSGO.OrderSearch as Os
import FiSGO.PrimesHandler as Ph


# TODO: Handle Lübeck exceptions and test everything


# Setup logger to stdout
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


LUBECK_SQRT_CODES = ["RF", "RG", "SZ"]
LUBECK_MAX_RANK = ["CA", "CB", "CC", "CD", "SA", "SD"]
LUBECK_NO_MAX_RANK = ["E6", "E7", "E8", "2E", "3D", "G2", "F4"]
LIE_TYPE_GROUP_IDS = LUBECK_SQRT_CODES + LUBECK_MAX_RANK + LUBECK_NO_MAX_RANK


def factorial_factor(n: int, p:int) -> int:
    """
    An implementation of Legendre's formula to compute the largest power of p dividing n!.

    The formula is:

    .. math::
        \\nu_p(n!) = \\sum_{i=1}^{\\infty} \\lfloor \\frac{n}{p^{i}}\\rfloor

    :param n: value of n whose factorial is to be checked.
    :param p: prime number.
    :return: the largest power of p that divides n!.
    """
    nu_p = 0
    # Calculate nu_p = n//p + n//(p^2) + n//(p^3) + ....
    while n > 0:
        n //= p
        nu_p += n
    return nu_p


def build_single_bound(n: int) -> list[int]:
    r"""
    Bounds on the prime powers of an n-dimensional (quasi)primitive group in characteristic zero.

    The bounds are computed using the following results:

    Let :math:`G` be an n-dimensional (quasi)primitive group in characteristic zero. Let :math:`p` be a prime and :math:`k` denote the largest
    power of :math:`p` dividing :math:`|G|`. Let :math:`(n!)_p` denote the largest power of :math:`p` dividing :math:`n!`.

    * (Brauer) if :math:`p \,|\, |G|` then :math:`p < 2n+1`.
    * (Brauer) if :math:`p > n+1` then :math:`p^2` does not divide :math:`|G|`.
    * (Blichfeld, Brauer) if :math:`p` is coprime to :math:`|G|`, then :math:`k < \log_p (n!)_p + n-1`.
    * (Blichfeld) if :math:`p \,|\, |G|`, then :math:`p^k <= (n!)_p 6^{n-1}`.

    :param n: Dimension
    :return: List of bounds to the prime powers dividing the order of the group. Each entry of the list corresponds
        to a prime, in ascending order starting from 2.
    """
    small_primes = [p for p in Ph.primes_lt(n*2+2) if p<=n+1]
    bounds6 = [0 for _ in small_primes]
    n_factorial = [factorial_factor(n, p) for p in small_primes]
    # We build 6-bounds
    for i, p in enumerate(small_primes):
        bounds6[i] = math.floor((n-1)/math.log(p, 6)) + n_factorial[i]
    # Build Blichfeld's coprime bounds
    blichfeld_bound = [n-1 + m for m in n_factorial]
    # Check all bounds against each other directly
    # Primes greater than n+1 may only appear once
    orders = [min(pair) for pair in zip(blichfeld_bound, bounds6)] + [1 for p in Ph.primes_lt(n*2+2) if p > n + 1]
    # The previous step is only valid for primes coprime to n, or if n is prime
    for p in Ph.factor(n)[0].keys():
        orders[small_primes.index(p)] = bounds6[small_primes.index(p)]
    return orders


def build_bounds(n_range: list[int]|int) -> list[int]:
    """
    Generic bounds on the prime powers of an n-dimensional (quasi)primitive group in characteristic zero, for any n on
    the given range.

    See :py:func:`FiSGO.PIrrepsSearch.build_single_bound` for more details.

    .. caution:: The end of the range is NOT included.

    :param n_range: A pair of integers, the input of range(n_range[0], n_range[1]).
    :return: List of bounds to the prime powers dividing the order of the group. Each entry of the list corresponds
        to a prime, in ascending order starting from 2.
    """
    if isinstance(n_range, int):
        return build_single_bound(n_range)
    generic_bound = build_single_bound(n_range[1]-1)
    for i in reversed(range(n_range[0], n_range[1]-1)):
        for j, b in enumerate(build_single_bound(i)):
            generic_bound[j] = max(b, generic_bound[j])
    return generic_bound
    ...


def build_absolute_bound(n: int) -> int:
    """
    Implementation of Collins' [[1]_] absolute bound to the order of a group with an n-dimensional projective irreducible representations.

    .. warning:: This function is not yet implemented for n < 20.

    :param n: Dimension.
    :return: Absolute bound on the order of the group.

    .. [1] Michael J. Collins. “On Jordan’s theorem for complex linear groups.” English. In: J. Group
        Theory 10.4 (2007), pp. 411–423. issn: 1433-5883. |DOI:10.1515/JGT.2007.032|

    .. |DOI:10.1515/JGT.2007.032| image:: https://zenodo.org/badge/DOI/10.1515/JGT.2007.032.svg
        :target: https://doi.org/10.1515/JGT.2007.032
    """
    if n > 70 or n in [63, 65, 67, 69]:
        return math.factorial(n+1)
    if 20 <= n <= 70 and n not in [63, 65, 67, 69]:
        r = n // 2
        return 60**r * math.factorial(r)
    raise NotImplementedError


def pirreps_search(n_range: list[int]|int, ignore: list[str] | None=None, use_absolute_bound: bool = False,
                   include_origin: bool=False) \
        -> tuple[list[tuple[int, str]] | list[tuple[int, str, str]], list[str| Any], list[str | Any]] | None:
    """
    Given a dimension or a dimension range, this function tries to search for simple groups containing projective representations
    within the given range.

    This is a high level function, combining most of the functionalities offered by FiSGO into a single function.
    This function may be quite slow, and produces log information. It is recommended to dump the output of the function
    into a file for later use and analysis, rather than using it inside a script.

    .. caution:: The end of the range "n_range" is NOT included.

    :param n_range: Either a positive integer or a pair of positive integers indicating the dimension range of the representation
        search. Example: 1000 or [222,301]
    :param ignore: A list of group ID's to be ignored in the search. Example: ["AA", "SZ"]
    :param use_absolute_bound: If true, uses an additional absolute bound, see :py:func:`build_absolute_bound`
    :param include_origin: If true, returns the database where each representation was sourced from alongside the degree.
    :return: A 3-tuple of lists. The first list contains the projective representation degrees found within the given range.
        The second list contains all those groups whose data representation data is complete, meaning it is known that no other
        representations may appear within the range. The third list contains a list of groups whose data may not be complete,
        meaning there could be representations of such groups within the range that have not been found.
    """
    logging.info("Starting pirreps search -----")
    if isinstance(n_range, int):
        n_range = [n_range, n_range+1]
    max_n = n_range[1]-1
    min_n = n_range[0]
    # Here we store the status of each group
    pirreps = [] # Here goes a list of tuples (degree, code)
    complete_data = []
    partial_data = []  # We always have the smallest pirrep degree
    # Before proceeding further, we check if we can use Hiss-Malle
    if max_n <= 250:
        logging.info("Using Hiss-Malle data for the complete range...")
        # We can use Hiss-Malle for everything
        pirreps = hiss_malle_range([min_n, max_n])
        if include_origin:
            return [(a,b,"Hiss-Malle") for a, b in pirreps], list(set(pair[1] for pair in pirreps)), []
        return pirreps, list(set(pair[1] for pair in pirreps)), []
    elif min_n <= 250:
        # We can partially use Hiss-Malle
        logging.info("Using Hiss-Malle data for degrees up to 250...")
        pirreps = [(a, b, "Hiss-Malle") for a,b in hiss_malle_range([min_n, 250])]
    # All bellow 250 is known with Hiss-Malle, so we search for the rest
    logging.info("Building bounds...")
    bound = build_bounds([max(min_n, 251), max_n+1])
    logging.info("Bounds successfully built.")
    if use_absolute_bound:
        logging.info("Building absolute bound...")
        abs_bound = build_absolute_bound(max_n)
        logging.info("Absolute bound successfully built.")
    else:
        abs_bound = None
    logging.info("Starting group candidates identification...")
    group_candidates = Os.simple_group_by_order(bound, abs_bound=abs_bound, ignore=ignore, return_codes=False)
    logging.info("Successfully identified group candidates.")
    # We check the smallest pirrep degree of each group
    logging.info(f"Checking smallest pirrep degrees on {len(group_candidates)} group candidates...")
    for group in group_candidates.copy():
        if group.smallest_pirrep_degree()[0] > max_n:
            # The smallest pirrep degree is too large, we remove the group from the list
            group_candidates.remove(group)
        else:
            # We check if the smallest pirrep degree is in the range
            if min_n <= group.smallest_pirrep_degree()[0] <= max_n:
                pirreps.append((group.smallest_pirrep_degree()[0], group.normalized_code(), "Smallest pirrep"))
    logging.info(f"Smallest pirrep degrees successfully checked with {len(group_candidates)} groups remaining.")
    # Here we check the sporadics -> gives complete_data
    logging.info("Checking sporadic pirreps...")
    for sporadic_group in (group for group in group_candidates.copy() if isinstance(group, Sg.Sporadic)):
        exists_pirrep = False
        for degree in sporadic_group.pirrep_degrees():
            if min_n <= degree <= max_n:
                exists_pirrep = True
                pirreps.append((degree, sporadic_group.normalized_code(), "Sporadic"))
        group_candidates.remove(sporadic_group)
        # If there is no pirrep in the range, we do not need it to appear anywhere
        if exists_pirrep:
            complete_data.append(sporadic_group.normalized_code())
    logging.info("Sporadic pirreps successfully checked.")
    # Here we check using Lubeck -> gives complete_data
    logging.info("Checking Lübeck data...")
    for lie_group_id in LIE_TYPE_GROUP_IDS:
        logging.info(f"Checking data for group type {lie_group_id}.")
        candidates = [group for group in group_candidates if group.code()[:2] == lie_group_id]
        if not candidates: # if candidates == []
            logging.info(f"### No groups of type {lie_group_id}.")
            continue
        lubeck_data = lubeck_bulk_get(lie_group_id, candidates)
        if not lubeck_data[1]:
            logging.info(f"### Lubeck data for all groups of type {lie_group_id} available!")
        else:
            logging.info(f"### Some groups of type {lie_group_id} have no Lübeck data available.")
        for group, degree_mult_pair in lubeck_data[0].items():
            complete_data.append(group.normalized_code())
            group_candidates.remove(group)
            degrees_in_range = [degree for degree, mult in degree_mult_pair if min_n <= degree <= max_n]
            for degree in degrees_in_range:
                pirreps.append((degree, group.normalized_code(), "Lübeck"))
        logging.info(f"Successfully checked Lübeck data for group type {lie_group_id}.")
    logging.info("Lübeck data successfully checked.")
    # Here we check using Dixon and Zalesskii relatively small pirreps -> can give either data type
    ...

    # We clean the data presentation
    if include_origin:
        ...
    else:
        pirreps_no_origin = [(pirrep[0], pirrep[1]) for pirrep in pirreps]
        # Clean duplicates
        pirreps = list(sorted(set(pirreps_no_origin)))
    # All groups remaining as candidates indicate that we only have partial data
    partial_data = [group.normalized_code() for group in group_candidates]
    # We return info on the groups
    return pirreps, complete_data, partial_data


def hiss_malle_range(degree_range: list[int], char: int=0, allow_duplicates: bool=False) -> list[tuple[int, str]]:
    """
    Given a range of degrees, between 2 and 250, returns the list of pirreps with the given characteristics.

    The function uses the precomputed data from Hiss and Malle. See :py:func:`FiSGO.SimpleGroups.hiss_malle_data`.

    .. caution:: The start and end of the range are included in the search.

    :param degree_range: Range of degrees. Between 2 and 250.
    :param char: The characteristic of the pirreps to be returned.
    :param allow_duplicates: If True, the function will return duplicates. These duplicates indicate the presence of
        different representations with the same degree arising from different coverings of the group. Otherwise,
        these duplicates are removed.
    :return: Returns a list of tuples, each tuple contains the degree and the group code of a pirrep.
    """
    hiss_malle_data = Sg.hiss_malle_data()
    pirreps_in_range = []
    for pirrep in hiss_malle_data:
        if degree_range[0] <= pirrep["degree"] <= degree_range[1]:
            if Sg.char_check(char, pirrep["char"], pirrep["not_char"]):
                pirreps_in_range.append((pirrep["degree"], pirrep["code"]))
    if allow_duplicates:
        return list(sorted(pirreps_in_range))
    return list(sorted(set(pirreps_in_range)))


def lubeck_bulk_get(group_id: str, groups:list[Sg.UniParamSimpleGroup] | list[Sg.BiParamSimpleGroup] | list[str]) -> tuple[dict, list]:
    """
    Given a list of groups or group codes of the same type, returns their computed Lübeck data.

    :param group_id: Group ID of the codes in 'codes'
    :param groups: List of group objects or group codes of the same type.
    :return: A tuple containing a dictionary pairing each group with a list of degree and multiplicity pairs
        of the projective representations, and a list of all groups whose data is unavailable.
    """

    code_input = False
    if type(groups[0]) is str:
        try:
            code_input = True
            groups_objects = [Sg.simple_group(group) for group in groups]
            groups = groups_objects
        except AttributeError:
            raise TypeError(f"The given groups list is invalid")

    pirreps_computed = dict()
    all_data = Sg.lubeck_data(group_id)
    # We start by filterning out exceptions
    unavailable = [group for group in groups if group.normalized_code() in Sg.EXCEPTIONAL_MULTIPLIER_CODES]
    avaliable: list[Sg.UniParamSimpleGroup] = [group for group in groups if group.normalized_code() not in Sg.EXCEPTIONAL_MULTIPLIER_CODES]

    if group_id in LUBECK_SQRT_CODES:
        # We select the sqrt value depending on the group
        match group_id:
            case "RF" | "SZ":
                sqrt_value = 2
            case _:
                sqrt_value = 3
        # We compute the pirreps for each group
        for group in avaliable:
            pirreps = []
            pirreps_data = all_data[group_id]["irreps"]["0"]
            for pirrep in pirreps_data:
                mult = Sg._sqrt_horner(pirrep["mult"], group.par, val=sqrt_value)
                if mult != 0:
                    degree = Sg._sqrt_horner(pirrep["degree"], group.par, val=sqrt_value)
                    pirreps.append([degree, mult])
            pirreps_computed[group] = pirreps
    elif group_id in LUBECK_NO_MAX_RANK or group_id in LUBECK_MAX_RANK:
        if group_id in LUBECK_NO_MAX_RANK:
            group_type = "uni"
            data = all_data[group_id]
        else: # group_id in LUBECK_MAX_RANK
            group_type = "bi"
            # We filter out those of rank greater than 8
            unavailable += [group for group in groups if group.n > 8]
            avaliable: list[Sg.BiParamSimpleGroup] = [group for group in groups if group.n < 9 and group in avaliable]

        # We compute the pirreps for each group
        for group in avaliable:
            if group_type == "bi":
                data = all_data[f"{group_id}-{group.n}"]
                q_value = group.q_value()
            else: # group_type == "uni"
                q_value = group.par_value()
            mod_group = Sg.modularity_group(group, data, group_type)
            pirreps_data = data["irreps"][mod_group]
            # We compute the degrees
            pirreps = []
            for pirrep in pirreps_data:
                mult = Sg._horner(pirrep["mult"], q_value)
                if mult != 0:
                    degree = Sg._horner(pirrep["degree"], q_value)
                    pirreps.append([degree, mult])
            pirreps_computed[group] = pirreps
    else:
        unavailable = groups
    if code_input:
        pirreps_computed_codes = {key.normalized_code(): pirreps_computed[key] for key in pirreps_computed.keys()}
        return pirreps_computed_codes, [group.normalized_code() for group in unavailable]
    else:
        return pirreps_computed, unavailable