import json

with open("Hiss_Malle_table_data.json", "r") as table_file:
    table_data = json.load(table_file)
with open("Hiss_Malle_missing_data.json", "r") as omissions_file:
    omissions_data = json.load(omissions_file)

print(len(table_data))
print(len(omissions_data))

complete_data = table_data + omissions_data

print(len(complete_data))

with open("Hiss_Malle_data.json", "w") as complete_file:
    json.dump(complete_data, complete_file, ensure_ascii=False, indent=4)

with open("Hiss_Malle_data.json", "r") as complete_file:
    print(len(json.load(complete_file)))






