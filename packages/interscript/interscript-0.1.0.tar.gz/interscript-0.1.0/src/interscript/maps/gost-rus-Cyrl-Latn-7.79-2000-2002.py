import interscript
import regex as re
interscript.stdlib.define_map("gost-rus-Cyrl-Latn-7.79-2000-2002")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2884859887402058710)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("gost-rus-Cyrl-Latn-7.79-2000-2002", "main", _stage_main)
_PTREE_2884859887402058710 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1044:{None:"D"},1045:{None:"E"},1025:{None:"Ë"},1046:{None:"Ž"},1047:{None:"Z"},1048:{None:"I"},1049:{None:"J"},1050:{None:"K"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1060:{None:"F"},1061:{None:"H"},1062:{None:"C"},1063:{None:"Č"},1064:{None:"Š"},1065:{None:"Ŝ"},1066:{None:"\""},1067:{None:"Y"},1068:{None:"´"},1069:{None:"È"},1070:{None:"Û"},1071:{None:"Â"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1076:{None:"d"},1077:{None:"e"},1105:{None:"ë"},1078:{None:"ž"},1079:{None:"z"},1080:{None:"i"},1081:{None:"j"},1082:{None:"k"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1092:{None:"f"},1093:{None:"h"},1094:{None:"c"},1095:{None:"č"},1096:{None:"š"},1097:{None:"ŝ"},1098:{None:"\""},1099:{None:"y"},1100:{None:"´"},1101:{None:"è"},1102:{None:"û"},1103:{None:"â"}}
