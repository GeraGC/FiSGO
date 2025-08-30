## Function Definitions -------------------------
group_list_nt := ['M12', 'M22', 'J2', 'J3', 'Co1', 'Fi22', "Fi24'", 'HS', 'McL', 'Ru', 'Suz', 'ON', 'B'];
group_list_t := ['M11', 'M23', 'M24', 'J1', 'J4', 'Co2', 'Co3', 'Fi23', 'He', 'HN', 'Ly', 'Th', 'M'];
file := "sporadic_data.txt";

SporadicExtraction := function()
PrintTo(file, "");
AppendTo(file, "[\n");
for g in group_list_nt do
    AppendTo(file, "{\"id\": \"", g, "\",\n");
    AppendTo(file, "\"pirreps\": [\n{\n");
    AppendTo(file, Concatenation("\"name\": \"", g, "\",\n"));
    AppendTo(file, "\"degrees\":", CharacterDegrees(CharacterTable(g)), "}\n");
    for r in ProjectivesInfo(CharacterTable(g)) do
        AppendTo(file, ",\n{\n \"name\":\"",r.name,"\",\n");
        AppendTo(file,"\"degrees\":",List(r.chars, i->i[1]), "\n}");
    od;
    AppendTo(file,"\n]\n},")
od;
for g in group_list_t do
    AppendTo(file, "{\"id\": \"", g, "\",\n");
    AppendTo(file, "\"pirreps\": [\n{\n");
    AppendTo(file, Concatenation("\"name\": \"", g, "\",\n"));
    AppendTo(file, "\"degrees\":", CharacterDegrees(CharacterTable(g)), "}\n");
    AppendTo(file,"\n]\n},");
od;
end;;

SporadicExtraction();
