import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-aze-Cyrl-Latn-1993")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1215480383305543980)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-aze-Cyrl-Latn-1993", "main", _stage_main)
_PTREE_1215480383305543980 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"Q"},1170:{None:"Ğ"},1044:{None:"D"},1045:{None:"E"},1240:{None:"Ə"},1046:{None:"J"},1047:{None:"Z"},1048:{None:"İ"},1067:{None:"I"},1032:{None:"Y"},1050:{None:"K"},1180:{None:"G"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1256:{None:"Ö"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1198:{None:"Ü"},1060:{None:"F"},1061:{None:"X"},1210:{None:"H"},1063:{None:"Ç"},1208:{None:"C"},1064:{None:"Ş"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"q"},1171:{None:"ğ"},1076:{None:"d"},1077:{None:"e"},1241:{None:"ə"},1078:{None:"j"},1079:{None:"z"},1080:{None:"i"},1099:{None:"ı"},1112:{None:"y"},1082:{None:"k"},1181:{None:"g"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1257:{None:"ö"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1199:{None:"ü"},1092:{None:"f"},1093:{None:"x"},1211:{None:"h"},1095:{None:"ç"},1209:{None:"c"},1096:{None:"ş"}}
