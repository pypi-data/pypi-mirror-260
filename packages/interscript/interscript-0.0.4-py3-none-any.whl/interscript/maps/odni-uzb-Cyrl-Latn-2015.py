import interscript
import regex as re
interscript.stdlib.define_map("odni-uzb-Cyrl-Latn-2015")
def _stage_main(s):
    s = re.compile("("+interscript.stdlib.aliases["any_character"]+")\\1", re.MULTILINE).sub("\\1", s)
    s = re.compile("("+interscript.stdlib.aliases["any_character"]+")\\1", re.MULTILINE).sub("\\1", s)
    s = re.compile("("+interscript.stdlib.aliases["any_character"]+")\\1", re.MULTILINE).sub("\\1", s)
    s = re.compile("("+interscript.stdlib.aliases["any_character"]+")\\1", re.MULTILINE).sub("\\1", s)
    s = re.compile("("+interscript.stdlib.aliases["any_character"]+")\\1", re.MULTILINE).sub("\\1", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2983120566840125846)
    return s

interscript.stdlib.add_map_stage("odni-uzb-Cyrl-Latn-2015", "main", _stage_main)
_PTREE_2983120566840125846 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1170:{None:"Gh"},1044:{None:"D"},1045:{None:"E"},1025:{None:"Yo"},1046:{None:"J"},1047:{None:"Z"},1048:{None:"I"},1049:{None:"Y"},1050:{None:"K"},1178:{None:"Q"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1038:{None:"O"},1060:{None:"F"},1061:{None:"Kh"},1202:{None:"H"},1062:{None:"Ts"},1063:{None:"Ch"},1064:{None:"Sh"},1069:{None:"E"},1070:{None:"Yu"},1071:{None:"Ya"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1171:{None:"gh"},1076:{None:"d"},1077:{None:"e"},1105:{None:"yo"},1078:{None:"j"},1079:{None:"z"},1080:{None:"i"},1081:{None:"y"},1082:{None:"k"},1179:{None:"q"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1118:{None:"o"},1092:{None:"f"},1099:{None:"y"},1095:{None:"ch"},1103:{None:"ia"},1102:{None:"iu"},1093:{None:"kh"},1203:{None:"h"},1096:{None:"sh"},1101:{None:"e"},1097:{None:"shch"},1094:{None:"ts"},1169:{None:"g"},1131:{None:"u"},1106:{None:"d"},1109:{None:"dz"},1112:{None:"j"},1113:{None:"lj"},1114:{None:"nj"},1211:{None:"c"},1119:{None:"dz"},1108:{None:"ie"},1111:{None:"i"},1107:{None:"g"},1066:{None:""},1068:{None:""},1098:{None:""},1100:{None:""}}
