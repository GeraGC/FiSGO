import json

with open("Hiss_Malle_missing_data.json", "r") as omissions_file:
    omissions_data = json.load(omissions_file)

omissions_table = []
for irrep in omissions_data:
    irrep_row = dict()
    irrep_row["d"] = irrep["degree"]
    irrep_row["G"] = irrep["name"]
    if irrep["char"] is not None:
        irrep_row["ell"] = ", ".join(str(i) for i in irrep["char"])
    if irrep["not_char"] is not None:
        irrep_row["ell"] = "!" + ", ".join(str(i) for i in irrep["not_char"])
    if irrep["field"] is None:
        irrep_row["field"] = ""
    else:
        irrep_row["field"] = irrep["field"]
    irrep_row["ind"] = irrep["ind"]
    omissions_table.append(irrep_row)

with open("Hiss_Malle_omissions_table.json", "w") as omissions_file:
    json.dump(omissions_table, omissions_file, ensure_ascii=False, indent=4)


