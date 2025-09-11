import json
import FiSGO.PrimesHandler as ph
import logging
from typing import Any


def q_value(q):
    return q[0]**q[1]


def is_prime_power(n):
    factors = ph.factor(n)[0]
    if len(factors) == 1:
        return list(factors.items())[0][0]
    else:
        return None


def append_base_char(_list, q):
    if None in _list:
        _list.remove(None)
    if q[0] not in _list:
        _list.append(q[0])


def json_lookup_property(file_path: str, field: str, match: Any, return_field: str | list[str] | None) -> Any:
    with open(file_path, "r") as data_file:
        data = json.load(data_file)
        if type(return_field) is str:
            return (point[return_field] for point in data if point[field] == match)
        elif return_field is None:
            return (point for point in data if point[field] == match)
        else:
            return ({i:point[i] for i in return_field} for point in data if point[field] == match)



def main():
    # We need to compute representation data for L_2(q), q<499 and A_n for n<249
    # We start with the alternating groups
    hiss_malle_data = []
    for n in range(14, 252):
        factors = list(ph.factor(n)[0].keys())
        hiss_malle_data.append({"degree": n-1,
                                "name": f"A_{{{n}}}",
                                "field": None,
                                "ind": 1,
                                "char": None,
                                "not_char": factors,
                                "code": f"AA-{n}"
                                })

        hiss_malle_data.append({"degree": n - 2,
                                "name": f"A_{{{n}}}",
                                "field": None,
                                "ind": 1,
                                "char": factors,
                                "not_char": None,
                                "code": f"AA-{n}"
                                })

    hiss_malle_data.append({"degree": 252-2,
                            "name": f"A_{{{252}}}",
                            "field": None,
                            "ind": 1,
                            "char": list(ph.factor(252)[0].keys()),
                            "not_char": None,
                            "code": f"AA-{252}"
                            })

    # We move on to the L_2 groups
    # First we search for all prime powers less than 499
    primes = ph.primes_lt(500)
    prime_powers = []
    for p in primes:
        i = 1
        while p**i < 500:
            prime_powers.append((p, i))
            i += 1
    # Remove redundant or invalid powers
    prime_powers.remove((2, 1))
    prime_powers.remove((2, 2))
    prime_powers.remove((3, 1))
    prime_powers.remove((3, 2))


    for q in prime_powers:
        base_dict = {"degree": 1,
                     "name": f"{{\\rm PSL}}_{{2}}({q_value(q)})",
                     "field": "Not implemented",
                     "ind": 1,
                     "char": None,
                     "not_char": None,
                     "code": f"CA-2-{q[0]}_{q[1]}"
                     }
        base_cover_dict = base_dict.copy()
        base_cover_dict["name"] = "2." + base_dict["name"]

        # Reps common to all cases
        rep0 = base_dict.copy()
        rep0["degree"] = q_value(q)
        rep0["not_char"] = list(ph.factor(q_value(q) + 1)[0].keys())
        append_base_char(rep0["not_char"], q)
        hiss_malle_data.append(rep0)

        rep1 = base_dict.copy()
        rep1["degree"] = q_value(q) - 1
        rep1["not_char"] = [q[0]]
        hiss_malle_data.append(rep1)

        if q[0] == 2:
            rep3 = base_dict.copy()
            rep3["degree"] = q_value(q)+1
            rep3["not_char"] = [is_prime_power(q_value(q)-1)]
            append_base_char(rep3["not_char"], q)
            if q_value(q)-1 != 1:
                hiss_malle_data.append(rep3)

        elif q_value(q) % 4 == 1:
            rep1 = base_dict.copy()
            rep1["degree"] = (q_value(q)-1)//2
            rep1["char"] = [2]
            rep1["ind"] = -1
            hiss_malle_data.append(rep1)

            rep2 = base_cover_dict.copy()
            rep2["degree"] = (q_value(q) - 1) // 2
            rep2["not_char"] = [2, q[0]]
            rep2["ind"] = -1
            hiss_malle_data.append(rep2)

            rep3 = base_dict.copy()
            rep3["degree"] = (q_value(q) + 1) // 2
            rep3["not_char"] = [2, q[0]]
            hiss_malle_data.append(rep3)

            rep5 = base_cover_dict.copy()
            rep5["degree"] = q_value(q) - 1
            rep5["not_char"] = [is_prime_power((q_value(q) + 1) // 2)]
            append_base_char(rep5["not_char"], q)
            rep5["ind"] = -1
            if (q_value(q) + 1) // 2 != 1:
                hiss_malle_data.append(rep5)

            rep7 = base_dict.copy()
            rep7["degree"] = q_value(q) + 1
            rep7["not_char"] = [is_prime_power((q_value(q) - 1) // 4)]
            append_base_char(rep7["not_char"], q)
            if (q_value(q) - 1) // 4 != 1:
                hiss_malle_data.append(rep7)

            rep8 = base_cover_dict.copy()
            rep8["degree"] = q_value(q) + 1
            rep8["not_char"] = [2, q[0]]
            rep8["ind"] = -1
            hiss_malle_data.append(rep8)

        elif q_value(q) % 4 == 3:
            rep1 = base_dict.copy()
            rep1["degree"] = (q_value(q)-1)//2
            rep1["not_char"] = [q[0]]
            rep1["ind"] = 0
            hiss_malle_data.append(rep1)

            rep2 = base_cover_dict.copy()
            rep2["degree"] = (q_value(q) + 1) // 2
            rep2["not_char"] = [q[0], 2]
            rep2["ind"] = 0
            hiss_malle_data.append(rep2)

            rep4 = base_cover_dict.copy()
            rep4["degree"] = q_value(q) - 1
            rep4["not_char"] = [2, q[0]]
            rep4["ind"] = -1
            hiss_malle_data.append(rep4)

            rep6 = base_dict.copy()
            rep6["degree"] = q_value(q) + 1
            rep6["not_char"] = [is_prime_power((q_value(q) - 1) // 2)]
            append_base_char(rep6["not_char"], q)
            if (q_value(q) - 1) // 2 != 1:
                hiss_malle_data.append(rep6)

            rep7 = base_cover_dict.copy()
            rep7["degree"] = q_value(q) + 1
            rep7["not_char"] = [is_prime_power((q_value(q) - 1) // 2)]
            append_base_char(rep7["not_char"], q)
            append_base_char(rep7["not_char"], (2,1))
            rep7["ind"] = -1
            if (q_value(q) - 1) // 2 != 1:
                hiss_malle_data.append(rep7)
    
    with open("Hiss_Malle_missing_data.json", "w") as hiss_malle_file:
        json.dump(hiss_malle_data, hiss_malle_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # main()
    with open("Hiss_Malle_missing_data.json", "r") as hiss_malle_file:
        hiss_malle_data = json.load(hiss_malle_file)
    gen = json_lookup_property("Hiss_Malle_missing_data.json", "code", "CA-2-3_3",
                               ["degree","name", "char", "not_char", "ind"])
    for i in list(gen):
        print(i)
    print(3**3 % 4)
    print(len(hiss_malle_data))

    ...
