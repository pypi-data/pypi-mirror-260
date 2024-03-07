import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-tgk-Cyrl-Latn-1994")
def _stage_main(s):
    s = re.compile("(?<=[ГгЗзКкСс])ҳ", re.MULTILINE).sub("·h", s)
    s = re.compile("(?<=[ГгЗзКкСс])Ҳ", re.MULTILINE).sub("·H", s)
    s = re.compile("Ц(?=[АаЕеЁёИиОоУуЫыЭэЮюЯя])", re.MULTILINE).sub("S", s)
    s = re.compile("ц(?=[АаЕеЁёИиОоУуЫыЭэЮюЯя])", re.MULTILINE).sub("s", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1270117178638487143)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-tgk-Cyrl-Latn-1994", "main", _stage_main)
_PTREE_1270117178638487143 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1170:{None:"Gh"},1044:{None:"D"},1045:{None:"E"},1025:{None:"Yo"},1046:{None:"Zh"},1047:{None:"Z"},1048:{None:"I"},1250:{None:"Í"},1049:{None:"Y"},1050:{None:"K"},1178:{None:"Q"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1262:{None:"Ŭ"},1060:{None:"F"},1061:{None:"Kh"},1202:{None:"H"},1063:{None:"Ch"},1206:{None:"J"},1062:{None:"Ts"},1064:{None:"Sh"},1065:{None:"Sh"},1066:{None:"’"},1067:{None:"I"},1068:{None:""},1069:{None:"Ė"},1070:{None:"Yu"},1071:{None:"Ya"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1171:{None:"gh"},1076:{None:"d"},1077:{None:"e"},1105:{None:"yo"},1078:{None:"zh"},1079:{None:"z"},1080:{None:"i"},1251:{None:"í"},1081:{None:"y"},1082:{None:"k"},1179:{None:"q"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1263:{None:"ŭ"},1092:{None:"f"},1093:{None:"kh"},1203:{None:"h"},1095:{None:"ch"},1207:{None:"j"},1094:{None:"ts"},1096:{None:"sh"},1097:{None:"sh"},1098:{None:"’"},1099:{None:"i"},1100:{None:""},1101:{None:"ė"},1102:{None:"yu"},1103:{None:"ya"}}
