"""
Module implementing order search functions.
"""
import logging
import math
from functools import wraps

import FiSGO.PrimesHandler as ph
import FiSGO.SimpleGroups as sg


# TODO: Test all candidates functions
# TODO: Test absolute bounding works
# TODO: Module documentation


def order_search_logger(func):
    """ Decorator for logging candidate search functions. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Starting candidate search for {func.__name__.replace("candidates_", "")} groups.")
        result = func(*args, **kwargs)
        logging.info("Found {0} compatible groups.".format(len(result)))
        logging.info(f"Finished candidate search for {func.__name__.replace('candidates_', '')} groups.")
        return result
    return wrapper


def add_lists(list1: list[int], list2: list[int]) -> list[int]:
    """
    Adds two lists of integers of the same length pointwise.

    Example:

    >>> add_lists([1,2,3],[0,1,2])
    [1, 3, 5]

    :param list1: A list of integers.
    :param list2: A list of integers.
    :return: Pointwise addition of list1 and list2.
    """
    try:
        return [list1[i] + list2[i] for i in range(max(len(list1), len(list2)))]
    except IndexError:
        raise IndexError("The lists must have the same length")


def substract_lists(list1: list[int], list2: list[int]) -> list[int]:
    """
    Substracts two lists of integers with the same length pointwise.

    Example:

    >>> substract_lists([1,2,3],[0,1,2])
    [1, 1, 1]

    :param list1: A list of integers.
    :param list2: A list of integers.
    :return: Pointwise substraction of list1 and list2, list1-list2.
    """

    try:
        return [list1[i] - list2[i] for i in range(max(len(list1), len(list2)))]
    except IndexError:
        raise IndexError("The lists must have the same length")


def prod_scanned(factored1: tuple[list[int], int], factored2: tuple[list[int], int]) -> tuple[list[int], int]:
    """
    Given two tuples originating from PrimesHandler.prime_scanner with the same upper_bound (or same length), returns
    the product of both decompositions.

    Idea: if factored1 corresponds to a number n1 and factored2 to n2, then
    prod_scanned returns Primes.prime_scanner(n1*n2, upper_bound) without having to construct n1*n2 explicitely.

    Example:

    >>> prod_scanned(([1,1],1), ([3,0], 7))
    ([4, 1], 7)

    :param factored1: Tuple with a list of integers and an integer.
    :param factored2: Tuple with a list of integers and an integer.
    :return: Partially factorized product of the numbers represented by factored1 and factored2.
    """
    return add_lists(factored1[0], factored2[0]), factored1[1]*factored2[1]


def div_scanned(factored1: tuple[list[int], int], factored2: tuple[list[int], int]) -> tuple[list[int], int]:
    """
    Given two tuples originating from PrimesHandler.prime_scanner with the same upper_bound, returns the division
    of both decompositions.

    Idea: if factored1 corresponds to a number n1 and factored2 to n2, then prod_scanned returns
    Primes.prime_scanner(n1/n2, upper_bound) without having to construct n1/n2 explicitely.

    .. caution:: May return negative factors if the n1/n2 is not an integer! We expect the input to already be correct.

    Example:

    >>> div_scanned(([3,1],49), ([1,1], 7))
    ([2, 0], 7)

    :param factored1: Tuple with a list of integers and an integer.
    :param factored2: Tuple with a list of integers and an integer.
    :return: Partially factorized division of the numbers represented by factored1 and factored2.
    """
    return substract_lists(factored1[0], factored2[0]), factored1[1]//factored2[1]


def check_candidate(code: str, bound: list[int]) -> bool:
    """
    Given a simple group code and a bound, determines if the group order divides the given bound.

    :param code: A simple group code.
    :param bound: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means
        the order of the group must divide 2^2*5^1*11^3.
    :return: True if the order of the group divides the given bound, otherwise, returns False.
    """
    group_order_factors = ph.factor(sg.simple_group(code).order(), list_output=True)[0]
    if len(group_order_factors) > len(bound):
        return False
    for i in range(len(group_order_factors)):
        if group_order_factors[i] > bound[i]:
            return False
    return True


def prime_bound_compatiblity(order: tuple[list[int], int], bound: list[int]) -> bool:
    """
    Given the partial factorization of a number and a bound to the factorized part, the function checks
    if the given factorization satisfies the bound.

    A partial factorization refers to a number given in the format of PrimesHandler.prime_scanner.

    .. caution:: the length of order[0] is expected to be the same as bound, we are checking one factorization against the
        other

    Example:

    >>> prime_bound_compatiblity(([1,2],1), [3,3])
    True

    >>> prime_bound_compatiblity(([1,2],7), [3,3])
    False

    >>> prime_bound_compatiblity(([2,6],1), [3,3])
    False

    :param order: Tuple with a list of integers and an integer.
    :param bound: List of integers.
    :return: True if order is bounded by bound, False otherwise.
    """
    if order[1] != 1:
        # There have appeared primes which are not in prime_bounds, so this group is not a candidate
        return False
    # We now check prime order compatibility against the relative order
    for j, b in enumerate(bound):
        if order[0][j] > b:
            # A factor is greater than allowed, so this group is not a candidate
            return False
    return True


def absolute_bound_filter(group_list: list[str] | list[sg.SimpleGroup], bound: int, codes: bool):
    """
    Given a list of simple groups, returns only those whose order is less than or equal to a given bound.

    :param group_list: List of simple group codes (strings) or SimpleGroup derived objects corresponding to specific
        simple groups.
    :param bound: An integer.
    :param codes: True if group_list provides simple group codes, False if it provides SimpleGroup derived objects.
    :return: Returns a list of simple groups codes (strings) if codes is True, or a list of SimpleGroup derived objects
        if codes is false. The list contains only simple groups whose order is less than or equal to bound
    """
    if codes:
        for code in group_list:
            if sg.simple_group(code).order() > bound:
                group_list.remove(code)
    else:
        for group in group_list:
            if group.order() > bound:
                group_list.remove(group)
    return group_list


def powers_sequence(prime: int, n: int) -> int:
    """
    The function returns the exponent corresponding to the maximum power of 'prime' that divides prime*n.
    Rather than calculating prime*n and computing PrimesHandler.contained_power(prime*n, prime), this is done recursively.

    Example: If prime = 3, then the sequence is [1,1,2,1,1,2,1,1,3,1,...] where each entry corresponds to the power of 3
    contained in [3,6,9,12,15,18,21,24,27,30,...].

    .. caution:: We index the sequence starting at n=1.

    :param prime: A prime number.
    :param n: A positive integer.
    :return: The n-th term of the described sequence.
    """
    if n % prime != 0:
        return 1
    else:
        return 1 + powers_sequence(prime, n // prime)


def candidate_from_power(max_power: int, prime: int) -> int:
    """
    Given a positive integer 'max_power' and a prime number 'prime', the function calculates which is the largest number
    n such that prime^max_power divides n!. To do this, we consider the summation sequence s(m) of OrderSearch.powers_sequence,
    whose m-th term precisely gives the maximum power of 'prime' contained in (prime*m)!. Thus, if m is the smallest
    integer such that max_power < s(m), then n = prime*m - 1.

    :param max_power: A positive integer.
    :param prime: A prime number.
    :return: Largest positive integer n such that prime^max_power exactly divides n!.
    """
    # Summation sequence s(m) of OrderSearch.powers_sequence
    s = 1
    m = 1
    while not max_power < s:
        # If max_power < s, then we add the next term of the sequence to s, i.e. consider s(m+1)
        m += 1
        s += powers_sequence(prime, m)
    return prime * m - 1


def smallest_factorial_from_bound(bound: int) -> int:
    """
    Given a positive integer 'bound' it returns the largest integer n such that n! <= bound.

    :param bound: A positive integer.
    :return: The largest integer n such that n! <= bound.
    """
    n = 1
    while bound > 0:
        n += 1
        bound //= n
    return n-1


@order_search_logger
def candidates_AA(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all simple alternating groups :math:`\\mathrm{A}_n` whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    group_candidates = []
    n_candidates = []
    # Since the order of a simple alternating group is n!/2 (consider n > 4), the largest A_n compatible with the given
    # prime powers is limited by the smallest missing prime in the list. So we cut the list to only the relevant powers.
    if 0 in prime_bounds:
        prime_bounds = prime_bounds[:prime_bounds.index(0)]
    # The smallest simple alternating group is A_5, with order [2,1,1], so we check it is compatible
    if len(prime_bounds) < 3:
        return []
    if prime_bounds[0] < 2:
        return []
    # Instead of looking for an n!/2 satisfying our bounds, we look for an n! satisifying 2 * our bounds, so
    prime_bounds[0] += 1
    # The first limiting factor is the smallest prime p not dividing the order, so n is at most p-1
    n_candidates.append(ph.nth_prime(len(prime_bounds)+1)-1)
    # For each power 'm' in prime_bounds corresponding to a prime 'p', we find the largest n such that p ** m exactly divides n!
    for i in range(len(prime_bounds)):
        n_candidates.append(candidate_from_power(prime_bounds[i], ph.nth_prime(i+1)))
    # If there is an absolute bound, we compute the largest n such that n! < abs_bound and add it to the candidates
    if abs_bound is not None:
        n_candidates.append(smallest_factorial_from_bound(abs_bound*2))
    # The n compatible with all restrictions is the smallest in n_candidates
    for n in range(5, min(n_candidates)+1):
        if return_codes:
            group_candidates.append("AA-{0}".format(n))
        else:
            group_candidates.append(sg.Alternating(n))
    return group_candidates


@order_search_logger
def candidates_CA(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all classical Chevalley :math:`A_n(q)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    for i, prime in enumerate(primes):
        # Chevalley type A groups depend on n and q=prime**k, n>0
        # If the allowed power of the prime is 0, it cannot appear, so we proceed to the next one
        if prime_bounds[i] == 0:
            continue
        # We run through the allowed k range, upper bounded by prime_bounds[i]
        for k in range(1, prime_bounds[i] + 1):
            q = prime ** k
            n = 1
            # We will build the order of the product term iteratibly for each q
            product_order = ([0 for _ in range(len(prime_bounds))], 1)
            # Since the order contains q**(n*(n+1)/2) we have a stopping condition to test each n, furthermore,
            # no other part of the product is divisible by q
            while prime_bounds[i] >= k * n * (n + 1) // 2:
                # We build the term of the product for the current n and scan its primes
                term_order = ph.prime_scanner_local(q ** (n + 1) - 1, primes)
                # We build product order now, notice it may have primes not found in it already
                product_order = prod_scanned(term_order, product_order)
                # We cannot modify product_order since we may need it in the next iteration,
                # so we create a relative product order to take care of the gcd term
                relative_product_order = product_order
                # We multiply the relative order by 1/(gcd(n+1,q-1)), notice it divides q**2-1
                if math.gcd(n + 1, q - 1) != 1:
                    gcd_scan = ph.prime_scanner_local(math.gcd(n + 1, q - 1), primes)
                    relative_product_order = div_scanned(relative_product_order, gcd_scan)
                # We check prime factors compatibility
                if not prime_bound_compatiblity(relative_product_order, prime_bounds):
                    # Relative order at most divides by q-1, if taking this out does not satisfy the bounds,
                    # then no other does for greater n's
                    max_relative_product_order = div_scanned(product_order,ph.prime_scanner_local(q-1, primes))
                    if not prime_bound_compatiblity(max_relative_product_order,prime_bounds):
                        break
                    n+=1
                    continue
                # Notice: (q,n)=(2,1) and (q,n)=(3,1) are not simple groups
                if (q == 2 and n == 1) or (q == 3 and n == 1):
                    n += 1
                    continue
                if return_codes:
                    group_candidates.append("CA-{0}-{1}_{2}".format(n, prime, k))
                else:
                    group_candidates.append(sg.ChevalleyA(n,(prime, k)))
                # We increase n by 1
                n += 1
    # If given an absolute bound, we discard groups that surpas it
    if not(abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates


@order_search_logger
def candidates_CB(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all classical Chevalley :math:`B_n(q)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    prime_gen = ph.primes(len(prime_bounds))
    for i in range(len(prime_bounds)):
        # Chevalley type B groups depend on n and q=prime**k, n>1
        # Prime number to be used to construct the group parameter q
        prime = next(prime_gen)
        # If the allowed power of the prime is 0, it cannot appear, so we proceed to the next one
        if prime_bounds[i] == 0:
            continue
        # We run through the allowed k range, upper bounded by prime_bounds[i]
        for k in range(1, prime_bounds[i] // 4 + 1):
            q = prime ** k
            n = 2
            # We will build the order of the product term iteratibly for each q (initializing at n=1)
            product_order = ph.prime_scanner_local(q**2-1, primes)
            # We multiply the order by 1/(gcd(2,q-1)), notice it divides q**2-1, which always appears as a factor
            # If q is odd, gcd(2,q-1)=2, otherwise, gcd(2,q-1) = 1, so we can adjust the power of 2 in product_order
            if prime != 2:
                product_order[0][0] -= 1
            # Since the order contains q**(n**2) we have a stopping condition to test each n, furthermore,
            # no other part of the product is divisible by q
            while prime_bounds[i] >= k * (n ** 2):
                # We build the term of the product for the current n and scan its primes
                term_order = ph.prime_scanner_local(q ** (2 * n) - 1, primes)
                # We build product order now, notice it may have primes not found in it already
                product_order = prod_scanned(term_order, product_order)
                # We check prime factors compatibility
                if not prime_bound_compatiblity(product_order, prime_bounds):
                    n+=1
                    break
                # Notice: (q,n)=(2,2) is not a simple group
                if q == 2 and n == 2:
                    n += 1
                    continue
                if return_codes:
                    group_candidates.append("CB-{0}-{1}_{2}".format(n, prime, k))
                else:
                    group_candidates.append(sg.ChevalleyB(n,(prime, k)))
                # We increase n by 1
                n += 1
    # If given an absolute bound, we discard groups that surpas it
    if not(abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates


@order_search_logger
def candidates_CC(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all classical Chevalley :math:`C_n(q)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    # The checks are the same as in Chevalley B groups, as their orders coincide, so we work from the candidates of CB
    candidates = candidates_CB(prime_bounds, abs_bound= abs_bound, return_codes=True)
    if return_codes:
        return [code.replace("B","C") for code in candidates if code.split("-")[1] != "2"]
    return [sg.simple_group(code.replace("B","C")) for code in candidates if code.split("-")[1] != "2"]


@order_search_logger
def candidates_CD(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all classical Chevalley :math:`D_n(q)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    prime_gen = ph.primes(len(prime_bounds))
    for i in range(len(prime_bounds)):
        # Chevalley type D groups depend on n and q=prime**k, n>0
        # Prime number to be used to construct the group parameter q
        prime = next(prime_gen)
        # If the allowed power of the prime is 0, it cannot appear, so we proceed to the next one
        if prime_bounds[i] == 0:
            continue
        # We run through the allowed k range, upper bounded by prime_bounds[i]
        for k in range(1, prime_bounds[i] + 1):
            q = prime ** k
            n = 4
            # We will build the order of the product term iteratibly for each q (initializing at n=3)
            product_order = ph.prime_scanner_local((q**2-1)*(q**4-1), primes)
            # Since the order contains q**(n*(n-1)) we have a stopping condition to test each n, furthermore,
            # no other part of the product is divisible by q
            while prime_bounds[i] >= k * n * (n - 1):
                # We build the term of the product for the current n and scan its primes
                term_order = ph.prime_scanner_local(q ** (2*n - 2) - 1, primes)
                # We build product order now, notice it may have primes not found in it already
                product_order = prod_scanned(term_order, product_order)
                # We cannot modify product_order since we may need it in the next iteration,
                # so we create a relative product order to take care of the gcd term
                # We have to consider the extra term q**n-1:
                relative_product_order = prod_scanned(product_order, ph.prime_scanner_local(q**n-1, primes))
                # We multiply the relative order by 1/(gcd(4,q**n-1))
                # Notice that if q == 2**k then gcd(4,q**n-1)=1, as such
                if prime != 2:
                    if math.gcd(4, q ** n - 1) == 2:
                        relative_product_order[0][0] -= 1
                    else:
                        relative_product_order[0][0] -= 2
                # We check prime factors compatibility
                if not prime_bound_compatiblity(relative_product_order, prime_bounds):
                    # Relative order at most divides by 4, if taking this out does not satisfy the bounds,
                    # then no other does for greater n's
                    max_relative_product_order = product_order
                    max_relative_product_order[0][0] -= 2
                    if not prime_bound_compatiblity(max_relative_product_order, prime_bounds):
                        break
                    n+=1
                    continue
                if return_codes:
                    group_candidates.append("CD-{0}-{1}_{2}".format(n, prime, k))
                else:
                    group_candidates.append(sg.ChevalleyD(n,(prime, k)))
                # We increase n by 1
                n += 1
    # If given an absolute bound, we discard groups that surpas it
    if not(abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates


def candidates_exceptional_chevalley(prime_bounds: list[int], abs_bound: int | None, q_power: int,
                                     product_indices: list[int], gcd_value: int, group_id: str, return_codes: bool):
    """
    Generic function with the procedure to find exceptional Chevalley groups whose order divides prime_bounds and is less
    than or equal to abs_bound.

    To understand the parameters refering to the group order, see the order table in `Wikipedia`_.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param q_power: Exponent of the q factor in the group order.
    :param product_indices: Indices of the capital Pi notation in the group order.
    :param gcd_value: In the group order, number corresponding to gcd(gcd_value, q-1).
    :param group_id: The ID of the exceptional Chevalley group.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.

    .. _Wikipedia: https://en.wikipedia.org/wiki/List_of_finite_simple_groups#Summary
    """
    # First compatibility check
    if max(prime_bounds) < q_power:
        return []
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    prime_gen = ph.primes(len(prime_bounds))
    for i in range(len(prime_bounds)):
        # Exceptional Chevalley groups depend on n and q=prime**k, n>0
        # Prime number to be used to construct the group parameter q
        prime = next(prime_gen)
        # If the allowed power of the prime is 0, it cannot appear, so we proceed to the next one
        if prime_bounds[i] == 0:
            continue
        # We run through the allowed k range, upper bounded by prime_bounds[i] and q**q_power dividing the order
        # Notice no other part of the product is divisible by q
        for k in range(1, prime_bounds[i] // q_power + 1):
            q = prime ** k
            # We will build the order of the product term
            product_order = ph.prime_scanner_local(math.prod(q ** i - 1 for i in product_indices),
                                             primes)
            # We add 1/gcd(gcd_value,q-1) (gcd_value can be 1,2 or 3)
            if gcd_value == 3:
                if math.gcd(gcd_value, prime ** k - 1) != 1:
                    product_order[0][1] -= 1
            elif gcd_value == 2:
                if math.gcd(gcd_value, prime ** k - 1) != 1:
                    product_order[0][0] -= 1
            # We check prime factors compatibility
            if not prime_bound_compatiblity(product_order, prime_bounds):
                continue
            # Group G_2(2) is not simple
            if group_id == "G2" and q == 2:
                continue

            if return_codes:
                group_candidates.append("{0}-{1}_{2}".format(group_id, prime, k))
            else:
                group_candidates.append(sg.simple_group_ids()[group_id]((prime, k)))
    # If given an absolute bound, we discard groups that surpas it
    if not (abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates


@order_search_logger
def candidates_E6(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all exceptional Chevalley :math:`E_6(q)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    return candidates_exceptional_chevalley(prime_bounds, abs_bound, 36, sg.CHEVALLEY_E6_POWER_INDICES,
                                            3, "E6",return_codes)


@order_search_logger
def candidates_E7(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all exceptional Chevalley :math:`E_7(q)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    return candidates_exceptional_chevalley(prime_bounds, abs_bound, 63, sg.CHEVALLEY_E7_POWER_INDICES,
                                            2, "E7",return_codes)


@order_search_logger
def candidates_E8(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all exceptional Chevalley :math:`E_8(q)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    return candidates_exceptional_chevalley(prime_bounds, abs_bound, 120, sg.CHEVALLEY_E8_POWER_INDICES,
                                            1, "E8",return_codes)


@order_search_logger
def candidates_F4(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all exceptional Chevalley :math:`F_4(q)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    return candidates_exceptional_chevalley(prime_bounds, abs_bound, 24, sg.CHEVALLEY_F4_POWER_INDICES,
                                            1, "F4",return_codes)


@order_search_logger
def candidates_G2(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all exceptional Chevalley :math:`G_2(q)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    return candidates_exceptional_chevalley(prime_bounds, abs_bound, 6, sg.CHEVALLEY_G2_POWER_INDICES,
                                            1, "G2",return_codes)


@order_search_logger
def candidates_SA(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all classical Steinberg :math:`{}^2A_n(q^2)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    prime_gen = ph.primes(len(prime_bounds))
    for i in range(len(prime_bounds)):
        # Steinberg type A groups depend on n and q=prime**k, n>1
        # Prime number to be used to construct the group parameter q
        prime = next(prime_gen)
        # If the allowed power of the prime is 0, it cannot appear, so we proceed to the next one
        if prime_bounds[i] == 0:
            continue
        # We run through the allowed k range, upper bounded by prime_bounds[i]
        for k in range(1, prime_bounds[i] + 1):
            q = prime ** k
            n = 2
            # We will build the order of the product term iteratibly for each q, initialize at n=1
            product_order = ph.prime_scanner_local(q ** 2 - 1, primes)
            # Since the order contains q**(n*(n+1)/2) we have a stopping condition to test each n, furthermore,
            # no other part of the product is divisible by q
            while prime_bounds[i] >= k * n * (n + 1) / 2:
                # We build the term of the product for the current n and scan its primes
                term_order = ph.prime_scanner_local(q ** (n + 1) - (-1) ** (n + 1), primes)
                # We build product order now, notice it may have primes not found in it already
                product_order = prod_scanned(term_order, product_order)
                # We cannot modify product_order since we may need it in the next iteration,
                # so we create a relative product order to take care of the gcd term
                relative_product_order = product_order
                # We multiply the relative order by 1/(gcd(n+1,q+1)), notice it divides q**2-1
                if math.gcd(n + 1, q + 1) != 1:
                    gcd_scan = ph.prime_scanner_local(math.gcd(n + 1, q + 1), primes)
                    relative_product_order = div_scanned(relative_product_order, gcd_scan)
                # We check prime factors compatibility
                if not prime_bound_compatiblity(relative_product_order, prime_bounds):
                    # Relative order at most divides by q+1, if taking this out does not satisfy the bounds,
                    # then no other does for greater n's
                    max_relative_product_order = div_scanned(product_order, ph.prime_scanner_local(q + 1, primes))
                    if not prime_bound_compatiblity(max_relative_product_order, prime_bounds):
                        break
                    n+=1
                    continue
                # Notice: (q,n)=(2,2) is not a simple group
                if q == 2 and n == 2:
                    n += 1
                    continue
                if return_codes:
                    group_candidates.append("SA-{0}-{1}_{2}".format(n, prime, k))
                else:
                    group_candidates.append(sg.Steinberg2A(n,(prime, k)))
                # We increase n by 1
                n += 1
    # If given an absolute bound, we discard groups that surpas it
    if not(abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates


@order_search_logger
def candidates_SD(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all classical Steinberg :math:`{}^2D_n(q^2)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    prime_gen = ph.primes(len(prime_bounds))
    for i in range(len(prime_bounds)):
        # Steinberg type D groups depend on n and q=prime**k, n>3
        # Prime number to be used to construct the group parameter q
        prime = next(prime_gen)
        # If the allowed power of the prime is 0, it cannot appear, so we proceed to the next one
        if prime_bounds[i] == 0:
            continue
        # We run through the allowed k range, upper bounded by prime_bounds[i]
        for k in range(1, prime_bounds[i] + 1):
            q = prime ** k
            n = 4
            # We will build the order of the product term iteratibly for each q (initializing at n=3)
            product_order = ph.prime_scanner_local((q**2-1)*(q**4-1), primes)
            # Since the order contains q**(n*(n-1)) we have a stopping condition to test each n, furthermore,
            # no other part of the product is divisible by q
            while prime_bounds[i] >= k * n * (n - 1):
                # We build the term of the product for the current n and scan its primes
                term_order = ph.prime_scanner_local(q ** (2*n - 2) - 1, primes)
                # We build product order now, notice it may have primes not found in it already
                product_order = prod_scanned(term_order, product_order)
                # We cannot modify product_order since we may need it in the next iteration,
                # so we create a relative product order to take care of the gcd term
                # We have to consider the extra term q**n+1:
                relative_product_order = prod_scanned(product_order, ph.prime_scanner_local(q**n+1, primes))
                # We multiply the relative order by 1/(gcd(4,q**n+1))
                # Notice that if q == 2**k then gcd(4,q**n+1)=1, as such
                if prime != 2:
                    if math.gcd(4, q ** n + 1) == 2:
                        relative_product_order[0][0] -= 1
                    else:
                        relative_product_order[0][0] -= 2
                # We check prime factors compatibility
                if not prime_bound_compatiblity(relative_product_order, prime_bounds):
                    # Relative order at most divides by 4, if taking this out does not satisfy the bounds,
                    # then no other does for greater n's
                    max_relative_product_order = product_order
                    max_relative_product_order[0][0] -= 2
                    if not prime_bound_compatiblity(max_relative_product_order, prime_bounds):
                        break
                    n+=1
                    continue
                if return_codes:
                    group_candidates.append("SD-{0}-{1}_{2}".format(n, prime, k))
                else:
                    group_candidates.append(sg.Steinberg2D(n,(prime, k)))
                # We increase n by 1
                n += 1
    # If given an absolute bound, we discard groups that surpas it
    if not(abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates


@order_search_logger
def candidates_2E(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all exceptional Steinberg :math:`{}^2E_6(q^2)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    # First compatibility check
    if max(prime_bounds) < 36:
        return []
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    prime_gen = ph.primes(len(prime_bounds))
    for i in range(len(prime_bounds)):
        # Exceptional Steinberg 2E6 groups depend on q=prime**k
        # Prime number to be used to construct the group parameter q
        prime = next(prime_gen)
        # If the allowed power of the prime is 0, it cannot appear, so we proceed to the next one
        if prime_bounds[i] == 0:
            continue
        # We run through the allowed k range, upper bounded by prime_bounds[i] and q**36 dividing the order
        # Notice no other part of the product is divisible by q
        for k in range(1, prime_bounds[i] // 36 + 1):
            q = prime ** k
            # We will build the order of the product term
            product_order = ph.prime_scanner_local(math.prod(q ** i - (-1) ** i for i in sg.STEINBERG_2E6_POWER_INDICES),
                                             primes)
            # We add 1/gcd(gcd_value,q-1) (gcd_value can be 1,2 or 3)
            if math.gcd(3, prime ** k + 1) != 1:
                product_order[0][1] -= 1
            # We check prime factors compatibility
            if not prime_bound_compatiblity(product_order, prime_bounds):
                continue
            if return_codes:
                group_candidates.append("2E-{0}_{1}".format(prime, k))
            else:
                group_candidates.append(sg.ExcetionalSteinberg2E6((prime, k)))
    # If given an absolute bound, we discard groups that surpas it
    if not (abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates


@order_search_logger
def candidates_3D(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all exceptional Steinberg :math:`{}^3D_4(q^3)`, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    # First compatibility check
    if max(prime_bounds) < 12:
        return []
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    prime_gen = ph.primes(len(prime_bounds))
    for i in range(len(prime_bounds)):
        # Exceptional Steinberg 3D4 groups depend on q=prime**k
        # Prime number to be used to construct the group parameter q
        prime = next(prime_gen)
        # If the allowed power of the prime is 0, it cannot appear, so we proceed to the next one
        if prime_bounds[i] == 0:
            continue
        # We run through the allowed k range, upper bounded by prime_bounds[i] and q**12 dividing the order
        # Notice no other part of the product is divisible by q
        for k in range(1, prime_bounds[i] // 12 + 1):
            q = prime ** k
            # We build the order of the group except for q**12
            product_order = ph.prime_scanner_local(math.prod([q ** 8 + q ** 4 + 1, q ** 6 - 1, q ** 2 - 1]), primes)
            # We check prime factors compatibility
            if not prime_bound_compatiblity(product_order, prime_bounds):
                continue
            if return_codes:
                group_candidates.append("3D-{0}_{1}".format(prime, k))
            else:
                group_candidates.append(sg.ExcetionalSteinberg3D4((prime, k)))
    # If given an absolute bound, we discard groups that surpas it
    if not (abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates


@order_search_logger
def candidates_SZ(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all Suzuki :math:`{}^2B_2(2^{2n+1})` groups, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    # Suzuki groups all have a power 2**6
    if prime_bounds[0] < 6:
        return []
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    # Since q=2**(2n+1) for Suzuki grups, we have q**2 = q**(4n+2), we start at n=1
    n = 1
    while 4 * n + 2 <= prime_bounds[0]:
        q = 2 ** (2 * n + 1)
        # We build the order of the group except for q**2
        product_order = ph.prime_scanner_local((q ** 2 + 1) * (q - 1), primes)
        # We check prime factors compatibility
        if not prime_bound_compatiblity(product_order, prime_bounds):
            n += 1
            continue
        if return_codes:
            group_candidates.append("SZ-{0}".format(n))
        else:
            group_candidates.append(sg.Suzuki(n))
        n += 1
    # If given an absolute bound, we discard groups that surpas it
    if not (abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates


@order_search_logger
def candidates_RF(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all Ree :math:`{}^2F_4(2^{2n+1})` groups, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    # Ree 2F4 groups all have a power 2**36
    if prime_bounds[0] < 36:
        return []
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    # Since q=2**(2n+1) for Suzuki grups, we have q**12 = q**(24n+12), we start at n=1
    n = 1
    while 24 * n + 12 <= prime_bounds[0]:
        q = 2 ** (2 * n + 1)
        # We build the order of the group except for q**12
        product_order = ph.prime_scanner_local(math.prod([q ** 6 + 1, q ** 4 - 1, q ** 3 + 1, q - 1]), primes)
        # We check prime factors compatibility
        if not prime_bound_compatiblity(product_order, prime_bounds):
            n += 1
            continue
        if return_codes:
            group_candidates.append("RF-{0}".format(n))
        else:
            group_candidates.append(sg.Ree2F4(n))
        n += 1
    # If given an absolute bound, we discard groups that surpas it
    if not (abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates


@order_search_logger
def candidates_TT(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns the Tits group :math:`{}^2F_4(2)'` if its order divides prime_bounds and is less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    # We check prime order compatibility
    try:
        for i in range(len(sg.TITS_ORDER)):
            if sg.TITS_ORDER[i] > prime_bounds[i]:
                return []
    except IndexError:
        # If we have more elements in sg.TITS_ORDER than in prime_bounds, the code raises IndexError, meaning we are
        # considering too few primes, so it is not a candidate.
        return []
    # Check the absolute bound:
    if not(abs_bound is None):
        if ph.prime_reconstructor(sg.TITS_ORDER, 1) > abs_bound:
            return []
    if return_codes:
        return ["TT"]
    return [sg.Tits()]


@order_search_logger
def candidates_RG(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all Ree :math:`{}^2G_2(3^{2n+1})` groups, simple groups of Lie type, whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """

    # Ree 2G2 groups all have a power 3**9
    if prime_bounds[1] < 9:
        return []
    group_candidates = []
    primes = list(ph.primes(len(prime_bounds)))
    # Since q=2**(2n+1) for Suzuki grups, we have q**3 = q**(6n+3), we start at n=1
    n = 1
    while 6 * n + 3 <= prime_bounds[1]:
        q = 3 ** (2 * n + 1)
        # We build the order of the group except for q**12
        product_order = ph.prime_scanner_local((q ** 3 + 1) * (q - 1), primes)
        # We check prime factors compatibility
        if not prime_bound_compatiblity(product_order, prime_bounds):
            n += 1
            continue
        if return_codes:
            group_candidates.append("RG-{0}".format(n))
        else:
            group_candidates.append(sg.Ree2G2(n))
        n += 1
    # If given an absolute bound, we discard groups that surpas it
    if not (abs_bound is None):
        return absolute_bound_filter(group_candidates, abs_bound, return_codes)
    return group_candidates

@order_search_logger
def candidates_SP(prime_bounds: list[int], abs_bound = None, return_codes = True):
    """
    Returns a list of all sporadic simple groups whose order divides prime_bounds and is
    less than or equal to abs_bound.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code. See SimpleGroups.simple_group_ids.
    :return: Returns a list, the contents depend on the return_codes parameter.
    """
    sporadic_orders = {group["id"]: group["order"] for group in sg.sporadic_groups_data()}
    group_candidates = []
    for group in sporadic_orders:
        # We check prime order compatibility
        try:
            for i, prime_power in enumerate(sporadic_orders[group]):
                if prime_power > prime_bounds[i]:
                    continue
        except IndexError:
            # If we have more elements in sporadic_orders[group] than in prime_bounds, the code raises IndexError,
            # meaning we are considering too few primes, so it is not a candidate.
            continue
        # Check the absolute bound:
        if abs_bound is not None and (ph.prime_reconstructor(sporadic_orders[group], 1) > abs_bound):
            continue
        if return_codes:
            group_candidates += [f"SP-{group}"]
        else:
            group_candidates += [sg.Sporadic(group)]
    return group_candidates


def clear_duplicates(groups: list, codes: bool) -> list:
    """
    Given a list of simple group objects or a list of simple group codes, returns a new list clear of duplicates.

    :param groups: List of simple groups, either codes or objects, not mixed.
    :param codes: True if 'groups' contains codes, False if it contains simple group objects.
    :return: A list of simple groups (objects or codes depending on 'codes') free of duplicates.
    """
    duplicate_free = []
    # For the duplication cleaning, we work with the group codes
    if codes:
        codes_list = [sg.simple_group(code).normalized_code() for code in groups]
    else:
        codes_list = [group.normalized_code() for group in groups]
    for code in codes_list:
        # First we check if the same code is duplicated
        if code in duplicate_free:
            continue
        # We obtain the isomorphic codes
        isomorphic_codes = sg.simple_group(code).isomorphisms()
        if not isomorphic_codes:
            # If there are no isomorphisms, the group cannot be a duplicate
            duplicate_free.append(code)
        else:
            duplicate = False
            # We check if any of the isomorphic codes is already present in the list
            for code_iso in isomorphic_codes:
                if code_iso in duplicate_free:
                    # If we find the code in the list, we mark it as a duplicate and break
                    duplicate = True
                    break
            # If we reach the end of the process and the code has not been found, we add it
            if not duplicate:
                duplicate_free.append(code)
    # We return a list of codes or simple group objects depending on the original input
    if not codes:
        return [sg.simple_group(code) for code in duplicate_free]
    return duplicate_free


CANDIDATE_FUNCTIONS = {"AA": candidates_AA,
                       "CA": candidates_CA,
                       "CB": candidates_CB,
                       "CC": candidates_CC,
                       "CD": candidates_CD,
                       "E6": candidates_E6,
                       "E7": candidates_E7,
                       "E8": candidates_E8,
                       "F4": candidates_F4,
                       "G2": candidates_G2,
                       "SA": candidates_SA,
                       "SD": candidates_SD,
                       "2E": candidates_2E,
                       "3D": candidates_3D,
                       "SZ": candidates_SZ,
                       "RF": candidates_RF,
                       "TT": candidates_TT,
                       "RG": candidates_RG,
                       "SP": candidates_SP}


def simple_group_by_order(prime_bounds: list[int], abs_bound: int|None=None, return_codes: bool=True, ignore: list[str]|None=None)\
        -> list[str|sg.SimpleGroup]:
    """
    Returns a list of all simple groups whose order divides prime_bounds and is less than or equal to abs_bound.

    Certain groups can be ignored by providing a list of ids to ignore. See :py:func:`FiSGO.SimpleGroups.simple_group_ids`
    for a list of valid ids. By default, no groups are ignored.

    :param prime_bounds: Contains a list with the maximum powers for each prime, example: [2,0,1,0,3] means the order
        of the group must divide 2^2*5^1*11^3.
    :param abs_bound: An integer providing an upper bound to the order of the group, if None, then it is constructed
        from prime_bounds.
    :param return_codes: If False, the function returns a list of derived objects from the SimpleGroup class. If True,
        the function returns a list of strings, each string represents a simple group code.
        See :py:func:`FiSGO.SimpleGroups.simple_group_ids`.
    :param ignore: List of groups to ignore given as a list of code ids, example: ['AA', 'SP']. For all ids see
        :py:func:`FiSGO.SimpleGroups.simple_group_ids`. By default, no groups are ignored.
    :return: A list of simple groups (objects or codes depending on 'return_codes') free of duplicates.
    """

    if ignore is None:
        ignore = []
    group_candidates = []
    for group_type in CANDIDATE_FUNCTIONS:
        if group_type in ignore:
            continue
        group_candidates += CANDIDATE_FUNCTIONS[group_type](prime_bounds, abs_bound=abs_bound, return_codes=return_codes)
    return clear_duplicates(group_candidates, return_codes)
