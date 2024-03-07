import interscript
import regex as re
interscript.stdlib.define_map("alalc-ukr-Cyrl-Latn-1997")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_631602777719981270)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("alalc-ukr-Cyrl-Latn-1997", "main", _stage_main)
_PTREE_631602777719981270 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"H"},1168:{None:"G"},1044:{None:"D"},1045:{None:"E"},1028:{None:"I͡e"},1046:{None:"Z͡h"},1047:{None:"Z"},1048:{None:"Y"},1030:{None:"I"},1031:{None:"Ï"},1049:{None:"Ĭ"},1050:{None:"K"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1060:{None:"F"},1061:{None:"Kh"},1062:{None:"T͡s"},1063:{None:"Ch"},1064:{None:"Sh"},1065:{None:"Shch"},1070:{None:"I͡u"},1071:{None:"I͡a"},1068:{None:"ʹ"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"h"},1169:{None:"g"},1076:{None:"d"},1077:{None:"e"},1108:{None:"i͡e"},1078:{None:"z͡h"},1079:{None:"z"},1080:{None:"y"},1110:{None:"i"},1111:{None:"ï"},1081:{None:"ĭ"},1082:{None:"k"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1092:{None:"f"},1093:{None:"kh"},1094:{None:"t͡s"},1095:{None:"ch"},1096:{None:"sh"},1097:{None:"shch"},1102:{None:"i͡u"},1103:{None:"i͡a"},1100:{None:"ʹ"}}
