import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-tat-Cyrl-Latn-2007")
def _stage_main(s):
    s = re.compile("Г(?=[ЕеƏәИиӨөҮүЭэ])", re.MULTILINE).sub("G", s)
    s = re.compile("г(?=[ЕеƏәИиӨөҮүЭэ])", re.MULTILINE).sub("g", s)
    s = re.compile("К(?=[ЕеƏәИиӨөҮүЭэ])", re.MULTILINE).sub("K", s)
    s = re.compile("к(?=[ЕеƏәИиӨөҮүЭэ])", re.MULTILINE).sub("k", s)
    s = re.compile("Ю(?=[ЕеƏәИиӨөҮүЭэ])", re.MULTILINE).sub("Yü", s)
    s = re.compile("ю(?=[ЕеƏәИиӨөҮүЭэ])", re.MULTILINE).sub("yü", s)
    s = re.compile("Я(?=[ЕеƏәИиӨөҮүЭэ])", re.MULTILINE).sub("Yä", s)
    s = re.compile("я(?=[ЕеƏәИиӨөҮүЭэ])", re.MULTILINE).sub("yä", s)
    s = re.compile("(?<=[АаЕеƏәОоӨөҮүУуЫыЭэЯяЪъЬь])Е", re.MULTILINE).sub("Yı", s)
    s = re.compile("(?<=[АаЕеƏәОоӨөҮүУуЫыЭэЯяЪъЬь])е", re.MULTILINE).sub("yı", s)
    s = re.compile("(?<=[АаЕеƏәИиОоӨөҮүУуЫыЭэЮюЯяЪъЬь])У", re.MULTILINE).sub("W", s)
    s = re.compile("(?<=[АаЕеƏәИиОоӨөҮүУуЫыЭэЮюЯяЪъЬь])у", re.MULTILINE).sub("w", s)
    s = re.compile("(?<=[АаЕеƏәИиОоӨөҮүУуЫыЭэЮюЯяЪъЬь])Ү", re.MULTILINE).sub("W", s)
    s = re.compile("(?<=[АаЕеƏәИиОоӨөҮүУуЫыЭэЮюЯяЪъЬь])ү", re.MULTILINE).sub("w", s)
    s = re.compile("(?<=[Гг])ый", re.MULTILINE).sub("i", s)
    s = re.compile("(?<=[Ии])Ю", re.MULTILINE).sub("Ü", s)
    s = re.compile("(?<=[Ии])ю", re.MULTILINE).sub("ü", s)
    s = re.compile("(?<=[Ии])Я", re.MULTILINE).sub("Ä", s)
    s = re.compile("(?<=[Ии])я", re.MULTILINE).sub("ä", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1638955554951219241)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-tat-Cyrl-Latn-2007", "main", _stage_main)
_PTREE_1638955554951219241 = {1040:{None:"A"},1240:{None:"Ə"},1041:{None:"B"},1042:{None:"W"},1043:{None:"Ğ"},1044:{None:"D"},1045:{None:"E"},1046:{None:"J"},1174:{None:"C"},1047:{None:"Z"},1048:{None:"İ"},1049:{None:"Y"},1050:{None:"Q"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1186:{None:"Ꞑ"},1054:{None:"O"},1256:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1198:{None:"Ü"},1060:{None:"F"},1061:{None:"Х"},1210:{None:"H"},1062:{None:"Ts"},1063:{None:"Ç"},1064:{None:"Ş"},1065:{None:"ŞÇ"},1066:{None:""},1067:{None:"I"},1068:{None:"’"},1069:{None:"E"},1070:{None:"Yu"},1071:{None:"Ya"},1072:{None:"a"},1241:{None:"ə"},1073:{None:"b"},1074:{None:"w"},1075:{None:"ğ"},1076:{None:"d"},1077:{None:"e"},1078:{None:"j"},1175:{None:"c"},1079:{None:"z"},1080:{None:"i"},1081:{None:"y"},1082:{None:"q"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1187:{None:"ꞑ"},1086:{None:"o"},1257:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1199:{None:"ü"},1092:{None:"f"},1093:{None:"x"},1211:{None:"h"},1094:{None:"ts"},1095:{None:"ç"},1096:{None:"ş"},1097:{None:"şç"},1098:{None:""},1099:{None:"ı"},1100:{None:"’"},1101:{None:"e"},1102:{None:"yu"},1103:{None:"ya"}}
