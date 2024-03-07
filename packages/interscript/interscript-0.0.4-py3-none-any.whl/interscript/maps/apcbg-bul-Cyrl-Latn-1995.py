import interscript
import regex as re
interscript.stdlib.define_map("apcbg-bul-Cyrl-Latn-1995")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1269638138976032207)
    return s

interscript.stdlib.add_map_stage("apcbg-bul-Cyrl-Latn-1995", "main", _stage_main)
_PTREE_1269638138976032207 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1044:{None:"D"},1045:{None:"E"},1046:{None:"Zh"},1047:{None:"Z"},1048:{None:"I"},1049:{None:"Y"},1050:{None:"K"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1060:{None:"F"},1061:{None:"H"},1062:{None:"Ts"},1063:{None:"Ch"},1064:{None:"Sh"},1065:{None:"Sht"},1066:{None:"A"},1068:{None:"Y"},1070:{None:"Yu"},1071:{None:"Ya"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1076:{None:"d"},1077:{None:"e"},1078:{None:"zh"},1079:{None:"z"},1080:{None:"i"},1081:{None:"y"},1082:{None:"k"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1092:{None:"f"},1093:{None:"h"},1094:{None:"ts"},1095:{None:"ch"},1096:{None:"sh"},1097:{None:"sht"},1098:{None:"a"},1100:{None:"y"},1102:{None:"yu"},1103:{None:"ya"},1130:{None:"Ŭ"},1131:{None:"ŭ"},1122:{None:"YE"},1123:{None:"ye"}}
