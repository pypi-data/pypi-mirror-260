import interscript
import regex as re
interscript.stdlib.define_map("icao-mkd-Cyrl-Latn-9303")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4110437859711020641)
    return s

interscript.stdlib.add_map_stage("icao-mkd-Cyrl-Latn-9303", "main", _stage_main)
_PTREE_4110437859711020641 = {39:{None:""},1040:{None:"A"},1041:{None:"B"},1044:{None:"D"},1025:{None:"E"},1045:{None:"E"},1069:{None:"E"},1060:{None:"F"},1043:{None:"G"},1048:{None:"I"},1049:{None:"I"},1050:{None:"KJ"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1042:{None:"V"},1067:{None:"Y"},1047:{None:"Z"},1063:{None:"CH"},1071:{None:"IA"},1070:{None:"IU"},1061:{None:"H"},1064:{None:"SH"},1065:{None:"SHCH"},1062:{None:"C"},1046:{None:"ZH"},1168:{None:"G"},1038:{None:"U"},1130:{None:"U"},1026:{None:"D"},1029:{None:"DZ"},1032:{None:"J"},1033:{None:"LJ"},1034:{None:"NJ"},1210:{None:"C"},1039:{None:"DJ"},1028:{None:"IE"},1031:{None:"I"},1027:{None:"GJ"},1072:{None:"a"},1073:{None:"b"},1076:{None:"d"},1105:{None:"e"},1077:{None:"e"},1101:{None:"e"},1092:{None:"f"},1075:{None:"g"},1080:{None:"i"},1081:{None:"i"},1082:{None:"kj"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:""},1074:{None:"v"},1099:{None:"y"},1079:{None:"z"},1095:{None:"ch"},1103:{None:"ia"},1102:{None:"i"},1093:{None:"h"},1096:{None:"sh"},1097:{None:"shch"},1094:{None:"c"},1078:{None:"zh"},1169:{None:"g"},1118:{None:""},1131:{None:""},1106:{None:"d"},1109:{None:"dz"},1112:{None:"j"},1113:{None:"lj"},1114:{None:"nj"},1211:{None:"c"},1119:{None:"dj"},1108:{None:"ie"},1111:{None:"i"},1107:{None:"gj"}}
