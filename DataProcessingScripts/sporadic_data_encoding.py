import json

SPORADIC_ORDERS = { 'M11' : [4, 2, 1, 0, 1],
                    'M12' : [6, 3, 1, 0, 1],
                    'M22' : [7, 2, 1, 1, 1],
                    'M23' : [7, 2, 1, 1, 1, 0, 0, 0, 1],
                    'M24' : [10, 3, 1, 1, 1, 0, 0, 0, 1],
                    'J1' : [3, 1, 1, 1, 1, 0, 0, 1],
                    'J2' : [7, 3, 2, 1],
                    'J3' : [7, 5, 1, 0, 0, 0, 1, 1],
                    'J4' : [21, 3, 1, 1, 3, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                    'Co1' : [21, 9, 4, 2, 1, 1, 0, 0, 1],
                    'Co2' : [18, 6, 3, 1, 1, 0, 0, 0, 1],
                    'Co3' : [10, 7, 3, 1, 1, 0, 0, 0, 1],
                    'Fi22' : [17, 9, 2, 1, 1, 1],
                    'Fi23' : [18, 13, 2, 1, 1, 1, 1, 0, 1],
                    'Fi24\'' : [21, 16, 2, 3, 1, 1, 1, 0, 1, 1],
                    'HS' : [9, 2, 3, 1, 1],
                    'McL' : [7, 6, 3, 1, 1],
                    'He' : [10, 3, 2, 3, 0, 0, 1],
                    'Ru' : [14, 3, 3, 1, 0, 1, 0, 0, 0, 1],
                    'Suz' : [13, 7, 2, 1, 1, 1],
                    'ON' : [9, 4, 1, 3, 1, 0, 0, 1, 0, 0, 1],
                    'HN' : [14, 6, 6, 1, 1, 0, 0, 1],
                    'Ly' : [8, 7, 6, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                    'Th' : [15, 10, 3, 2, 0, 1, 0, 1, 0, 0, 1],
                    'B' : [41, 13, 6, 2, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
                    'M' : [46, 20, 9, 6, 2, 3, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1]
                   }

SPORADIC_MULTIPLIERS = {'M11' : 1, 'M12' : 2, 'M22' : 12,'M23' : 1,'M24' : 1,'J1' : 1,'J2' : 2,'J3' : 3,'J4' : 1,
                        'Co1' : 2, 'Co2' : 1, 'Co3' : 1,'Fi22' : 6,'Fi23' : 1,'Fi24\'' : 3,'HS' : 2,'McL' : 3,'He' : 1,
                        'Ru' : 2, 'Suz': 6,'ON' : 3,'HN' : 1, 'Ly' : 1,'Th' : 1,'B' : 2,'M' : 1}

LATEX_SPORADICS = {'M11' : ['{\\rm M}_{11}'],
                   'M12' : ['{\\rm M}_{12}'],
                   'M22' : ['{\\rm M}_{22}'],
                   'M23' : ['{\\rm M}_{23}'],
                   'M24' : ['{\\rm M}_{24}'],
                   'J1' : ['{\\rm J}_1', '{\\rm J}(1)', '{\\rm J}(11)'],
                   'J2' : ['{\\rm J}_2', '{\\rm HJ}'],
                   'J3' : ['{\\rm J}_3', '{\\rm HJM}'],
                   'J4' : ['{\\rm J}_4'],
                   'Co1' : ['{\\rm Co}_1'],
                   'Co2' : ['{\\rm Co}_2'],
                   'Co3' : ['{\\rm Co}_3'],
                   'Fi22' : ['{\\rm Fi}_{22}', 'M(22)'],
                   'Fi23' : ['{\\rm Fi}_{23}', 'M(23)'],
                   'Fi24\'' : ['{\\rm Fi}_{24}\'', 'M(24)\'', 'F_{3+}'],
                   'HS' : ['{\\rm HS}'],
                   'McL' : ['{\\rm McL}'],
                   'He' : ['{\\rm He}', '{\\rm HHM}', '{\\rm HTH}', 'F_7'],
                   'Ru' : ['{\\rm Ru}'],
                   'Suz': ['{\\rm Suz}', '{\\rm Sz}'],
                   'ON' : ['{\\rm O\'N}', '{\\rm O\'NS}', '{\\rm O-S}'],
                   'HN' : ['{\\rm HN}', 'F_5', 'D'],
                   'Ly' : ['{\\rm Ly}', '{\\rm LyS}'],
                   'Th' : ['{\\rm Th}', 'F_3', 'E'],
                   'B' : ['{\\rm B}', 'F_2'],
                   'M' : ['{\\rm M}', 'F_1', '{\\rm M}_1']}

SMALLEST_PIRREPS = {'M11': [10, 3], 'M12': [10, 2], 'M22': [10, 2], 'M23': [22, 1], 'M24': [23, 1], 'J1': [56, 2],
                    'J2': [6, 2], 'J3': [18, 2], 'J4': [1333, 2], 'Co1': [24, 1], 'Co2': [23, 1], 'Co3': [23, 1],
                    'Fi22': [78, 1], 'Fi23': [782, 1], "Fi24\'": [783, 1], 'HS': [22, 1], 'McL': [22, 1], 'He': [51, 2],
                    'Ru': [28, 2], 'Suz': [12, 1], 'ON': [342, 2], 'HN': [133, 2], 'Ly': [2480, 2], 'Th': [248, 1],
                    'B': [4371, 1], 'M': [196883, 1]}


def list_counter(l):
    new_list = []
    set_l = set(l)
    for i in set_l:
        new_list.append([i, l.count(i)])
    return sorted(new_list)


def main():
    to_dump = []

    # sporadics = sg.sporadic_group_names()
    #
    # print([group for group in sporadics if sg.simple_group("SP-"+group).multiplier() == 1])
    # print([group for group in sporadics if sg.simple_group("SP-"+group).multiplier() != 1])

    with open("sporadic_data_pirreps.json", "r", encoding='utf-8') as pirreps_file:
        pirreps = json.load(pirreps_file)

    for sporadic_id in SPORADIC_ORDERS:
        group_dict = dict()
        group_dict["code"] = "SP-" + sporadic_id
        group_dict["id"] = sporadic_id
        group_dict["order"] = SPORADIC_ORDERS[sporadic_id]
        group_dict["latex_name"] = LATEX_SPORADICS[sporadic_id]
        group_dict["multiplier"] = SPORADIC_MULTIPLIERS[sporadic_id]
        group_dict["smallest_pirrep"] = SMALLEST_PIRREPS[sporadic_id]
        group_dict["pirreps"] = []
        for pirrep_data in pirreps:
            if pirrep_data["id"] == sporadic_id:
                for fields in pirrep_data["pirreps"]:
                    try:
                        fields["degrees"][0][1]
                        group_dict["pirreps"].append(fields)
                    except TypeError:
                        group_dict["pirreps"].append({"name": fields["name"], "degrees": list_counter(fields["degrees"])})
                break
        to_dump.append(group_dict)

    with open("sporadic_groups_data.json", "w", encoding='utf-8') as f:
        json.dump(to_dump, f, ensure_ascii=False, indent=4)


def smallest_pirreps_search():
    smallest_pirreps = dict()
    with open("sporadic_groups_data.json", "r", encoding='utf-8') as sporadic_data_file:
        sporadic_data = json.load(sporadic_data_file)
        for group in sporadic_data:
            if group["multiplier"] == 1:
                smallest_pirreps[group["id"]] = sorted(group["pirreps"][0]["degrees"])[1]
            if group["multiplier"] != 1:
                smallest_pirreps[group["id"]] = sorted([cover["degrees"][0] for cover in group["pirreps"]] +
                                                       [cover["degrees"][1] for cover in group["pirreps"]
                                                        if cover["name"] == group["id"]])[1]
    print(smallest_pirreps)

if __name__ == "__main__":
    main()