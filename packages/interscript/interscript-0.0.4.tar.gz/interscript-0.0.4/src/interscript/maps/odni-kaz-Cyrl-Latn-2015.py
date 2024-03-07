import interscript
import regex as re
interscript.stdlib.define_map("odni-kaz-Cyrl-Latn-2015")
def _stage_main(s):
    s = re.compile("([Ғғ])[Ғғ]", re.MULTILINE).sub("\\1", s)
    s = re.compile("([Ёё])[Ёё]", re.MULTILINE).sub("\\1", s)
    s = re.compile("([Жж])[Жж]", re.MULTILINE).sub("\\1", s)
    s = re.compile("([Ңң])[Ңң]", re.MULTILINE).sub("\\1", s)
    s = re.compile("([Хх])[Хх]", re.MULTILINE).sub("\\1", s)
    s = re.compile("([Цц])[Цц]", re.MULTILINE).sub("\\1", s)
    s = re.compile("([Чч])[Чч]", re.MULTILINE).sub("\\1", s)
    s = re.compile("([Шш])[Шш]", re.MULTILINE).sub("\\1", s)
    s = re.compile("([Щщ])[Щщ]", re.MULTILINE).sub("\\1", s)
    s = re.compile("([Юю])[Юю]", re.MULTILINE).sub("\\1", s)
    s = re.compile("([Яя])[Яя]", re.MULTILINE).sub("\\1", s)
    s = re.compile("[ъь]", re.MULTILINE).sub(interscript.stdlib.aliases["none"], s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2959709869944117734)
    return s

interscript.stdlib.add_map_stage("odni-kaz-Cyrl-Latn-2015", "main", _stage_main)
_PTREE_2959709869944117734 = {1040:{None:"A"},1240:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1170:{None:"Gh"},1044:{None:"D"},1045:{None:"E"},1025:{None:"Yo"},1046:{None:"Zh"},1047:{None:"Z"},1048:{None:"I"},1030:{None:"I"},1049:{None:"Y"},1050:{None:"K"},1178:{None:"Q"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1186:{None:"Ng"},1054:{None:"O"},1256:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1198:{None:"U"},1200:{None:"U"},1060:{None:"F"},1061:{None:"Kh"},1210:{None:"H"},1062:{None:"Ts"},1063:{None:"Ch"},1064:{None:"Sh"},1065:{None:"Shch"},1067:{None:"Y"},1069:{None:"E"},1070:{None:"Yu"},1071:{None:"Ya"},1072:{None:"a"},1241:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1171:{None:"gh"},1076:{None:"d"},1077:{None:"e"},1105:{None:"yo"},1078:{None:"zh"},1079:{None:"z"},1080:{None:"i"},1110:{None:"i"},1081:{None:"y"},1082:{None:"k"},1179:{None:"q"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1187:{None:"ng"},1086:{None:"o"},1257:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1199:{None:"u"},1201:{None:"u"},1092:{None:"f"},1093:{None:"kh"},1211:{None:"h"},1094:{None:"ts"},1095:{None:"ch"},1096:{None:"sh"},1097:{None:"shch"},1099:{None:"y"},1101:{None:"e"},1102:{None:"yu"},1103:{None:"ya"}}
