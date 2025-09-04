import json
import re
import logging
from typing import Any

from FiSGO.PrimesHandler import contained_power

def json_lookup_property(file_path: str, field: str, match: Any, return_field: str) -> Any:
    """
    Helper function to look up a property in the JSON file. Given a field and a match, it returns
    the value of the return field for the matching group. If no match is found, it returns None.

    :param file_path: String with the path to the JSON file.
    :param field: Field to look up.
    :param match: Value to match for the given field.
    :param return_field: Field to return if a match is found.
    :return: The value of the given return field if a match is found, otherwise None.
    """
    with open(file_path, "r") as data_file:
        data = json.load(data_file)
        try:
            return next(point for point in data if point[field] == match)[return_field]
        except StopIteration:
            logging.warning(f"No match found for {field}={match}")
            return None


def main():
    with open("raw_Hiss_Malle_table.json", "r") as Hiss_Malle_file:
        raw_data = json.load(Hiss_Malle_file)

    hiss_malle_data = []

    for irrep in raw_data:
        new_irrep = dict()
        new_irrep["degree"] = irrep["d"]
        new_irrep["name"] = irrep["G"]
        new_irrep["field"] = irrep["field"]
        new_irrep["ind"] = irrep["ind"]
        # We reformat the characteristic of the irrep:
        if type(irrep["ell"]) is int:
            new_irrep["char"] = [irrep["ell"]]
            new_irrep["not_char"] = None
        if type(irrep["ell"]) is str:
            if irrep["ell"] == "all":
                # We denote not having conditions over the characteristic by marking both as None
                new_irrep["char"] = None
                new_irrep["not_char"] = None
            elif "!" in irrep["ell"]:
                new_irrep["char"] = None
                new_irrep["not_char"] = [int(i) for i in irrep["ell"].split("!")[1].replace(" ", "").split(",")]
            else:
                new_irrep["char"] = [int(i) for i in irrep["ell"].replace(" ", "").split(",")]
                new_irrep["not_char"] = None
        # Now we find the code of the group from the LaTeX name:
        if "PS" in irrep["G"]:
            id_string = re.search(r"PS\w}_{\d*}\(\d*\)", irrep["G"]).group(0)
            n = int(re.search(r"{\d*}", id_string).group(0)[1:-1])
            q = int(re.search(r"\(\d*\)", id_string).group(0)[1:-1])
            if "PSL" in id_string:
                code = f"CA-{n-1}-{q}"
            if "PSU" in id_string:
                code = f"SA-{n-1}-{q}"
            if "PSp" in id_string:
                code = f"CC-{n//2}-{q}"
        elif "A" in irrep["G"]:
            n = int(re.search(r"{\d*}", irrep["G"]).group(0)[1:-1])
            code = f"AA-{n}"
        elif "G_{2}" in irrep["G"]:
            q = int(re.search(r"\(\d*\)", irrep["G"]).group(0)[1:-1])
            code = f"G2-{q}"
        elif "Sz(" in irrep["G"]:
            q = int(re.search(r"\(\d*\)", irrep["G"]).group(0)[1:-1])
            n = (contained_power(q,2) - 1) // 2
            code = f"SZ-{n}"
        elif "{}^3D_4" in irrep["G"]:
            q = int(re.search(r"\(\d*\)", irrep["G"]).group(0)[1:-1])
            code = f"3D-{q}"
        elif "{}^2F_4(2)" in irrep["G"]:
            code = "TT"
        elif "O" in irrep["G"] and "\'" not in irrep["G"]:
            if "+" in irrep["G"] or "-" in irrep["G"]:
                q = int(re.search(r"\(\d*\)", irrep["G"]).group(0)[1:-1])
                n = int(re.search(r"{\d*}", irrep["G"]).group(0)[1:-1]) // 2
                if "+" in irrep["G"]:
                    code = f"CD-{n}-{q}"
                else:
                    code = f"SD-{n}-{q}"
            else:
                q = int(re.search(r"\(\d*\)", irrep["G"]).group(0)[1:-1])
                n = (int(re.search(r"{\d*}", irrep["G"]).group(0)[1:-1]) - 1) // 2
                code = f"SB-{n}-{q}"
        elif "F_{4}" in irrep["G"]:
            q = int(re.search(r"\(\d*\)", irrep["G"]).group(0)[1:-1])
            code = f"F4-{q}"
        else:
            # We look through the sporadics, otherwise write None if failed identification
            if "." in irrep["G"]:
                # We have a covering group
                id_string = irrep["G"].split(".")[1]
            else:
                id_string = irrep["G"]
            with open("sporadic_groups_data.json", "r") as sporadic_file:
                sporadic_data = json.load(sporadic_file)
            for group in sporadic_data:
                if id_string in group["latex_name"]:
                    code = group["code"]
                    break
        try:
            new_irrep["code"] = code
        except UnboundLocalError:
            new_irrep["code"] = None
        hiss_malle_data.append(new_irrep)

    with open("../FiSGO/PrecomputedData/Hiss_Malle_data.json", "w") as hiss_malle_file:
        json.dump(hiss_malle_data, hiss_malle_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
    print(json_lookup_property("../FiSGO/PrecomputedData/Hiss_Malle_data.json", "code", None, "name"))
