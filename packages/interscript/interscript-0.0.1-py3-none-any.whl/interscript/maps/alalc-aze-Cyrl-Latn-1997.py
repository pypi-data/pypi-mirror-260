import interscript
import regex as re
interscript.stdlib.define_map("alalc-aze-Cyrl-Latn-1997")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4315960283072578092)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("alalc-aze-Cyrl-Latn-1997", "main", _stage_main)
_PTREE_4315960283072578092 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1170:{None:"Gh"},1044:{None:"D"},1045:{None:"E"},1240:{None:"Ă"},1046:{None:"Zh"},1047:{None:"Z"},1048:{None:"I"},1067:{None:"Y"},1032:{None:"I̐"},1049:{None:"Y"},1050:{None:"K"},1180:{None:"Ġ"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1256:{None:"Ȯ"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1198:{None:"U̇"},1060:{None:"F"},1061:{None:"Kh"},1210:{None:"Ḣ"},1063:{None:"Ch"},1208:{None:"J"},1064:{None:"Sh"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1171:{None:"gh"},1076:{None:"d"},1077:{None:"e"},1241:{None:"ă"},1078:{None:"zh"},1079:{None:"z"},1080:{None:"i"},1099:{None:"y"},1112:{None:"ı̐"},1081:{None:"y"},1082:{None:"k"},1181:{None:"ġ"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1257:{None:"ȯ"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1199:{None:"u̇"},1092:{None:"f"},1093:{None:"kh"},1211:{None:"ḣ"},1095:{None:"ch"},1209:{None:"j"},1096:{None:"sh"},8217:{None:"’"}}
