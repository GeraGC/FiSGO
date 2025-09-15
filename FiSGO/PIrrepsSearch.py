"""
Module implementing the search of projective irreducible representations.
"""
import logging
from typing import Any

import FiSGO.SimpleGroups as Sg
import FiSGO.OrderSearch as Os
import FiSGO.PrimesHandler as Ph
import math

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
    """
    Bounds on the prime powers of an n-dimensional (quasi)primitive group in characteristic zero.

    The bounds are computed using the following results:

    Let G be an n-dimensional (quasi)primitive group in characteristic zero. Let p be a prime and k denote the largest
    power of p dividing |G|. Let (n!)_p denote the largest power of p dividing n!.

    * (Brauer) if p | |G| then p < 2n+1.
    * (Brauer) if p > n+1 then p**2 does not divide |G|.
    * (Blichfeld, Brauer) if p is coprime to |G|, then k < (n!)_p + n-1.
    * (Blichfeld) if p | |G|, then p**k <= (n!)_p*6**(n-1).

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


    .. caution:: The end of the range is NOT included.

    :param n_range:
    :param ignore:
    :param use_absolute_bound:
    :param include_origin:
    :return:
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
        if include_origin:
            pirreps = [(a, b, "Hiss-Malle") for a,b in hiss_malle_range([min_n, 250])]
        else:
            pirreps = hiss_malle_range([min_n, 250])
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
                if include_origin:
                    pirreps.append((group.smallest_pirrep_degree()[0], group.normalized_code(), "Smallest pirrep"))
                else:
                    pirreps.append((group.smallest_pirrep_degree()[0], group.normalized_code()))
    logging.info(f"Smallest pirrep degrees successfully checked with {len(group_candidates)} groups remaining.")
    # Here we check the sporadics -> gives complete_data
    logging.info("Checking sporadic pirreps...")
    for sporadic_group in (group for group in group_candidates.copy() if isinstance(group, Sg.Sporadic)):
        exists_pirrep = False
        for degree in sporadic_group.pirrep_degrees():
            if min_n <= degree <= max_n:
                exists_pirrep = True
                if include_origin:
                    pirreps.append((degree, sporadic_group.normalized_code(), "Sporadic"))
                else:
                    pirreps.append((degree, sporadic_group.normalized_code()))
        group_candidates.remove(sporadic_group)
        # If there is no pirrep in the range, we do not need it to appear anywhere
        if exists_pirrep:
            complete_data.append(sporadic_group.normalized_code())
    logging.info("Sporadic pirreps successfully checked.")
    # Here we check using Lubeck -> gives complete_data
    ...
    # Here we check using Dixon and Zalesskii relatively small pirreps -> can give either data type
    ...

    # We clean the data of duplicates
    if include_origin:
        ...
    else:
        pirreps = list(sorted(set(pirreps)))
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