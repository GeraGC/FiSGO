import math
from typing import Generator


# TODO: Module documentation
# TODO: See if function cross reference works and change it


# BuiltinPrimes.txt contains the first 10^5 primes
PRIMES_PATH = "PrecomputedData/BuiltinPrimes.txt"


def primes(n: int, primes_path=PRIMES_PATH) -> Generator[int, None, None]:
    """
    Given an integer n, returns a generator of the first n primes in file primes_path.

    File primes_path is specified to PRIMES_PATH by default, containing 10^5 first primes;
    primes_path should refer to a file where each line contains a single prime number, in ascending order, see
    PRIMES_PATH for an example of the required format.

    If n exceeds the maximum number of prime numbers available in the file primes_path, the function will raise a
    ValueError.

    :param n: Positive integer, maximum number of primes for the generator.
    :param primes_path: Path to a file with an ordered list of prime numbers.
    :return: Generator of the first n prime numbers.
    """
    with open(primes_path, "r") as primes_file:
        # We yield the first n lines of the file primes_file, removing the \n ending and as integers
        for i in range(n):
            try:
                yield int(primes_file.readline().removesuffix("\n"))
            except ValueError:
                raise ValueError("Specified range (" + str(n) + ") exceeds the available number of primes (" + str(i) + ")")


def nth_prime(n: int, primes_path=PRIMES_PATH) -> int:
    """
    Given an integer n, returns the nth prime number.

    CAUTION: the function starts counting at 1, so the prime 2 correspons to n = 1, 3 to n = 2 etc.

    The function uses `PrimesHandler.primes`_, Refer to the documentation of `PrimesHandler.primes`_ for additional
    information.

    .. _PrimesHandler.primes: :py:func:`.primes`

    :param n: Positive integer, position of the prime to search.
    :param primes_path: Path to a file with an ordered list of prime numbers.
    :return: Integer, the nth prime number.
    """
    prime = 2
    for p in primes(n, primes_path=primes_path):
        prime = p
    return prime


def prime_list(n: int, primes_path=PRIMES_PATH) -> list[int]:
    """
    Given an integer n, returns a list of the first n primes in file primes_path using PrimesHandler.primes.

    Refer to the documentation of PrimesHandler.primes for additional information.

    :param n: Positive integer, number of primes to list.
    :param primes_path: String, path to a file with an ordered list of prime numbers.
    :return: List of integers, list of the first n prime numbers.
    """
    return list(primes(n, primes_path=primes_path))


def primes_lt(n: int, primes_path=PRIMES_PATH) -> Generator[int, None, None]:
    """
    Given an integer n, returns a generator of all primes less than n in file primes_path.

    File primes_path is specified to PRIMES_PATH by default, containing 10^5 first primes;
    primes_path should refer to a file where each line contains a single prime number, in ascending order, see
    PRIMES_PATH for an example of the required format.

    :param n: Positive integer, strict upper bound for the primes to yield.
    :param primes_path: String, path to a file with an ordered list of prime numbers.
    :return: Generator of integers, a generator of all prime numbers less than n.
    """
    i = 1
    with open(primes_path, "r") as primes_file:
        while True:
            try:
                i = int(primes_file.readline().removesuffix("\n"))
                if i < n:
                    yield i
                else:
                    break
            except ValueError:
                # If n is higher than the maximum prime, we may lack primes, so we raise an error.
                raise ValueError("Specified number (" + str(n) + ") exceeds the maximum available prime (" + str(i) + ")")


def primes_lt_list(n: int, primes_path=PRIMES_PATH) -> list[int]:
    """
    Given an integer n, returns a list of all primes less than n in file primes_path using PrimesHandler.primes_lt.
    Refer to the documentation of PrimesHandler.primes_lt for additional information.

    :param n: Positive integer, strict upper bound for the primes to list.
    :param primes_path: String, path to a file with an ordered list of prime numbers.
    :return: List of integers, a list of all prime numbers less than n.
    """
    return list(primes_lt(n, primes_path=primes_path))


def is_prime(n: int, primes_path=PRIMES_PATH) -> bool:
    """
    Given an integer n, returns True if it is prime and False if it is not.
    Refer to the documentation of PrimesHandler.primes_lt for additional information on primes_path.

    NOTE: This function is NOT a primality test algorithm, it simply checks if n is a prime number found in primes_path.
    This is enough for the FiSGO modules using this function.

    :param n: Positive integer.
    :param primes_path: String, path to a file with an ordered list of prime numbers.
    :return: Boolean, True if n is a prime number, False otherwise.
    """
    if primes_lt_list(n+1, primes_path=primes_path)[-1] == n:
        return True
    else:
        return False


def contained_power(n: int, d: int) -> int:
    """
    Given integers n, d, returns the integer m such that d**m divides n but d**(m+1) does not divide n.

    :param n: Integer.
    :param d: Integer.
    :return: Integer, the maximum power of d that divides n.
    """
    for i in range(math.floor(math.log(abs(n), abs(d)))+1):
        if n % d == 0:
            n //= d
            continue
        else:
            return i
    return 0

def is_power(n: int, d: int) -> bool:
    """
    Given two integers n and d, returns True if there exists a positive integer m such that n = d**m, returns
    False otherwise.

    :param n: Integer.
    :param d: Integer.
    :return: Boolean, True if n is power of d, False otherwise.
    """
    if d**contained_power(n, d) == n:
        return True
    return False


def prime_scanner(n:int , upper_bound: int, primes_path = PRIMES_PATH) -> tuple[list[int], int]:
    """
    Given integers n, upper_bound, returns a tuple containing:
        * [0] A list with contained_power(n, p) for each p prime smaller than upper_bound.
        * [1] Leftover factor, containing factors of primes higher than upper_bound.
    This function uses PrimesHandler.primes_lt to get the primes less than upper_bound.

    :param n: Integer.
    :param upper_bound: Integer.
    :param primes_path: String, path to a file with an ordered list of prime numbers.
    :return: Tuple containing a list of integers and an integer. The list contains the exponents of prime powers dividing n,
        with a prime number less than upper_bound. The integer contains the leftover factor, not comprising any prime
        number less than upper_bound.
    """
    powers_list = []
    leftover = n
    for p in primes_lt(upper_bound, primes_path=primes_path):
        powers_list += [contained_power(n, p)]
        leftover //= p**powers_list[-1]
    return powers_list, leftover


def prime_reconstructor(powers: list[int], leftover=1, primes_path=PRIMES_PATH) -> int:
    """
    Given a list of integers 'powers', computes the product N of the first len(powers) primes raised to the integers
    of 'powers', returns N*leftover. By default, leftover is set to 1.

    This function is intended to be used alongside PrimesHandles.prime_scanner, to reconstruct a partially factorized
    number. However, it is not necessary that leftover be coprime to N.

    This function uses PrimesHandler.primes to get the first len(powers) primes.

    Example:

    >>> prime_reconstructor([2,0,1], 7)
    140
    >>> prime_reconstructor(*prime_scanner(60, 4))
    60

    :param powers: List of non-negative integers,
    :param leftover: Integer.
    :param primes_path: String, path to a file with an ordered list of prime numbers.
    :return: Integer, a reconstruction of an integer using powers as the prime exponents of the number, and multiplying
        the additional factor leftover.
    """
    reconstructed = 1
    i = 0
    for p in primes(len(powers), primes_path=primes_path):
        reconstructed *= p**powers[i]
        i += 1
    return reconstructed*leftover


def factor(n: int, primes_path = PRIMES_PATH, list_output = False) -> tuple[dict[int, int],int] | tuple[list, int]:
    """
    Given an integer n, it attempts to find the prime factors of n. Returns a tuple:
        * [0] - dictionary with prime:power entries
        * [1] - leftover factor
    A number has been successfully factorized if the leftover factor is 1. Otherwise, the leftover factor contains all
    prime factors not contained in the list in primes_path.

    File primes_path is specified to PRIMES_PATH by default, containing 10^5 first primes;
    primes_path should refer to a file where each line contains a single prime number, in ascending order, see
    PRIMES_PATH for an example of the required format.

    :param n: Integer. Number to be factorized.
    :param primes_path: String, path to a file with an ordered list of prime numbers.
    :param list_output: Boolean, if True, the function returns a list of the exponents, otherwise, returns a
        dictionary whose keys are prime numbers and values their associated exponents. By default, set to False.
    :return: Tuple containing a list or dictionary of integers and an integer. The first contains the exponents of prime
        powers dividing n. The integer contains the leftover factor if not enough primes are available for a complete
        factorization. The first object of the tuple is a list if list_output is set to True, otherwise it returns a
        dictionary whose keys are prime numbers and values their associated exponents.
    """
    leftover = n
    prime_factors = {}
    with open(primes_path, "r") as primes_file:
        while True:
            try:
                p = int(primes_file.readline().removesuffix("\n"))
                d = contained_power(leftover, p)
                if d == 0:
                     continue
                else:
                    prime_factors[p] = d
                leftover //= p**d
                if leftover == 1:
                    break
            except ValueError:
                break
    if list_output:
        prime_factors_list = []
        for prime in primes_lt(max(list(prime_factors.keys()))+1):
            if prime in prime_factors.keys():
                prime_factors_list += [prime_factors[prime]]
            else:
                prime_factors_list += [0]
        return prime_factors_list, leftover
    return prime_factors, leftover
