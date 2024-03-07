import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-bel-Cyrl-Latn-1979")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4388718144764749607)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_782399730346953008)
    s = re.compile("Ь", re.MULTILINE).sub("’", s)
    s = re.compile("ь", re.MULTILINE).sub("’", s)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-bel-Cyrl-Latn-1979", "main", _stage_main)
_PTREE_4388718144764749607 = {1047:{1043:{None:"Z·H"}},1079:{1075:{None:"z·h"}},1050:{1043:{None:"K·H"}},1082:{1075:{None:"k·h"}},1057:{1043:{None:"S·H"}},1089:{1075:{None:"s·h"}},1058:{1057:{None:"T·S"}},1090:{1089:{None:"t·s"}},1062:{1043:{None:"TS·H"}},1094:{1075:{None:"ts·h"}}}
_PTREE_782399730346953008 = {180:{None:"”"},700:{None:"”"},8217:{None:"”"},1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"H"},1044:{None:"D"},1045:{None:"Ye"},1025:{None:"Yo"},1046:{None:"Zh"},1047:{None:"Z"},1030:{None:"I"},1049:{None:"Y"},1050:{None:"K"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},92:{85:{48:{52:{48:{69:{None:"W"}}}}}},1060:{None:"F"},1061:{None:"Kh"},1062:{None:"Ts"},1063:{None:"Ch"},1064:{None:"Sh"},1067:{None:"Y"},1069:{None:"E"},1070:{None:"Yu"},1071:{None:"Ya"},1168:{None:"G"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"h"},1076:{None:"d"},1077:{None:"ye"},1105:{None:"yo"},1078:{None:"zh"},1079:{None:"z"},1110:{None:"i"},1081:{None:"y"},1082:{None:"k"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1118:{None:"w"},1092:{None:"f"},1093:{None:"kh"},1094:{None:"ts"},1095:{None:"ch"},1096:{None:"sh"},1099:{None:"y"},1101:{None:"e"},1102:{None:"yu"},1103:{None:"ya"},1169:{None:"g"}}
