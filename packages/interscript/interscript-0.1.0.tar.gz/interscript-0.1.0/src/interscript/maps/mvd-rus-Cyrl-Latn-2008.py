import interscript
import regex as re
interscript.stdlib.define_map("mvd-rus-Cyrl-Latn-2008")
def _stage_translit(s):
    s = re.compile("(?<=[ЗзЛлНнСсЦц])ь", re.MULTILINE).sub("́", s)
    s = re.compile("(?<=[ЗзЛлНнСсЦц])ʹ", re.MULTILINE).sub("́", s)
    s = re.compile("[’Ъъ]Ю", re.MULTILINE).sub("Ju", s)
    s = re.compile("[’Ъъ]ю", re.MULTILINE).sub("ju", s)
    s = re.compile("[’Ъъ]Я", re.MULTILINE).sub("Ja", s)
    s = re.compile("[’Ъъ]я", re.MULTILINE).sub("ja", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3963708851136269186)
    return s

interscript.stdlib.add_map_stage("mvd-rus-Cyrl-Latn-2008", "translit", _stage_translit)
def _stage_main(s):
    s = interscript.transliterate("mvd-rus-Cyrl-Latn-2008", s, "translit")
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("mvd-rus-Cyrl-Latn-2008", "main", _stage_main)
_PTREE_3963708851136269186 = {8217:{None:"j"},1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1044:{None:"D"},1045:{None:"E"},1025:{None:"E"},1046:{None:"Zh"},1047:{None:"Z"},1030:{None:"I"},1049:{None:"J"},1050:{None:"K"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},92:{85:{48:{52:{48:{69:{None:"W"}}}}}},1060:{None:"F"},1061:{None:"Kh"},1062:{None:"Ts"},1063:{None:"Ch"},1064:{None:"Sh"},1065:{None:"Shch"},1066:{None:"J"},1067:{None:"Y"},1068:{None:""},1069:{None:"E"},1070:{None:"Iu"},1071:{None:"Ia"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1076:{None:"d"},1077:{None:"e"},1105:{None:"e"},1078:{None:"zh"},1079:{None:"z"},1110:{None:"i"},1081:{None:"j"},1082:{None:"k"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1118:{None:"w"},1092:{None:"f"},1093:{None:"kh"},1094:{None:"ts"},1095:{None:"ch"},1096:{None:"sh"},1097:{None:"shch"},1098:{None:"j"},1099:{None:"y"},1100:{None:""},1101:{None:"e"},1102:{None:"iu"},1103:{None:"ia"}}
