# Do something like CharacterDegrees(CharacterTable(G)) and extract all reps lt 250, then
# crossreference with Hiss and Malle's article.

file := "small_pirreps_data.txt";
max_degree := 250;

PIrrepExtraction := function()
local group_list, groups_with_pirrep, group, i, collected_degrees, pair;
group_list := AllCharacterTableNames(IsQuasisimple, true, IsDuplicateTable, false);
collected_degrees := [];
for group in group_list do
    Add(collected_degrees, [group, Filtered(List(CharacterDegrees(CharacterTable(group)), i -> i[1]), i -> i <= max_degree)]);
od;
PrintTo(file, "");
AppendTo(file, "[\n");
for i in [2..max_degree] do
    AppendTo(file, "{\n\"degree\": \"", i, "\",\n");
    groups_with_pirrep := [];
    for pair in collected_degrees do
        if i in pair[2] then
                Add(groups_with_pirrep, pair[1]);
            fi;
    od;
    AppendTo(file, "\"groups\":", groups_with_pirrep, "\n},\n");
od;
AppendTo(file, "\n]");
end;;
