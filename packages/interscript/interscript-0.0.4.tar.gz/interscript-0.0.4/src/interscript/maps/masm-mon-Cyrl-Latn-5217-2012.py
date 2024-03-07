import interscript
import regex as re
interscript.stdlib.define_map("masm-mon-Cyrl-Latn-5217-2012")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2942943969352649321)
    return s

interscript.stdlib.add_map_stage("masm-mon-Cyrl-Latn-5217-2012", "main", _stage_main)
_PTREE_2942943969352649321 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1044:{None:"D"},1045:{None:"Ye"},1025:{None:"Yo"},1046:{None:"J"},1047:{None:"Z"},1048:{None:"I"},1049:{None:"I"},1050:{None:"K"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1256:{None:"Ö"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1198:{None:"Ü"},1060:{None:"F"},1061:{None:"Kh"},1062:{None:"Ts"},1063:{None:"Ch"},1064:{None:"Sh"},1065:{None:"Sh"},1066:{None:"I"},1067:{None:"Y"},1068:{None:"I"},1069:{None:"E"},1070:{None:"Yu"},1071:{None:"Ya"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1076:{None:"d"},1077:{None:"ye"},1105:{None:"yo"},1078:{None:"j"},1079:{None:"z"},1080:{None:"i"},1081:{None:"i"},1082:{None:"k"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1257:{None:"ö"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1199:{None:"ü"},1092:{None:"f"},1093:{None:"kh"},1094:{None:"ts"},1095:{None:"ch"},1096:{None:"sh"},1097:{None:"sh"},1098:{None:"i"},1099:{None:"y"},1100:{None:"i"},1101:{None:"e"},1102:{None:"yu"},1103:{None:"ya"}}
