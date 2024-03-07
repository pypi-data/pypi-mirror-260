import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-kaz-Cyrl-Latn-1979")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_327761245794660183)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-kaz-Cyrl-Latn-1979", "main", _stage_main)
_PTREE_327761245794660183 = {1040:{None:"A"},1240:{None:"Ä"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1170:{None:"Gh"},1044:{None:"D"},1045:{None:"E"},1025:{None:"Yo"},1046:{None:"Zh"},1047:{None:"Z"},1048:{None:"Ī"},1049:{None:"Y"},1050:{None:"K"},1178:{None:"Q"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1186:{None:"Ng"},1054:{None:"O"},1256:{None:"Ö"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"Ū"},1200:{None:"U"},1198:{None:"Ü"},1060:{None:"F"},1061:{None:"Kh"},1210:{None:"H"},1062:{None:"Ts"},1063:{None:"Ch"},1064:{None:"Sh"},1065:{None:"Shch"},1066:{None:"”"},1067:{None:"Y"},1030:{None:"I"},1068:{None:"’"},1069:{None:"Ė"},1070:{None:"Yu"},1071:{None:"Ya"},1072:{None:"a"},1241:{None:"ä"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1171:{None:"gh"},1076:{None:"d"},1077:{None:"e"},1105:{None:"yo"},1078:{None:"zh"},1079:{None:"z"},1080:{None:"ī"},1081:{None:"y"},1082:{None:"k"},1179:{None:"q"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1187:{None:"ng"},1086:{None:"o"},1257:{None:"ö"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"ū"},1201:{None:"u"},1199:{None:"ü"},1092:{None:"f"},1093:{None:"kh"},1211:{None:"h"},1094:{None:"ts"},1095:{None:"ch"},1096:{None:"sh"},1097:{None:"shch"},1098:{None:"”"},1099:{None:"y"},1110:{None:"i"},1100:{None:"’"},1101:{None:"ė"},1102:{None:"yu"},1103:{None:"ya"}}
