import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-bak-Cyrl-Latn-2007")
def _stage_main(s):
    s = re.compile(""+interscript.stdlib.aliases["boundary"]+"В(?=[АаЕеЁёИиОоӨөУуҮЫыЭэӘәЮюЯя])", re.MULTILINE).sub("W", s)
    s = re.compile(""+interscript.stdlib.aliases["boundary"]+"в(?=[АаЕеЁёИиОоӨөУуҮЫыЭэӘәЮюЯя])", re.MULTILINE).sub("w", s)
    s = re.compile(""+interscript.stdlib.aliases["boundary"]+"Е", re.MULTILINE).sub("Ye", s)
    s = re.compile(""+interscript.stdlib.aliases["boundary"]+"е", re.MULTILINE).sub("ye", s)
    s = re.compile("(?<=[АаЕеЁёИиОоӨөУуҮЫыЭэӘәЮюЯя])Е(?="+interscript.stdlib.aliases["boundary"]+")", re.MULTILINE).sub("Ye", s)
    s = re.compile("(?<=[АаЕеЁёИиОоӨөУуҮЫыЭэӘәЮюЯя])е(?="+interscript.stdlib.aliases["boundary"]+")", re.MULTILINE).sub("ye", s)
    s = re.compile("(?<=[АаЕеЁёИиОоӨөУуҮЫыЭэӘәЮюЯя])[УҮ]", re.MULTILINE).sub("W", s)
    s = re.compile("(?<=[АаЕеЁёИиОоӨөУуҮЫыЭэӘәЮюЯя])[уү]", re.MULTILINE).sub("w", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3881663769778167885)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-bak-Cyrl-Latn-2007", "main", _stage_main)
_PTREE_3881663769778167885 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1170:{None:"Ğ"},1044:{None:"D"},1176:{None:"Ź"},1045:{None:"E"},1025:{None:"Ë"},1046:{None:"J"},1047:{None:"Z"},1048:{None:"I"},1049:{None:"Y"},1050:{None:"K"},1184:{None:"Q"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1186:{None:"Ñ"},1054:{None:"O"},1256:{None:"Ö"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1194:{None:"Ś"},1058:{None:"T"},1059:{None:"U"},1198:{None:"Ü"},1060:{None:"F"},1061:{None:"X"},1210:{None:"H"},1062:{None:"Ts"},1063:{None:"Ç"},1064:{None:"Ş"},1065:{None:"ŞÇ"},1066:{None:""},1067:{None:"I"},1068:{None:""},1069:{None:"E"},1240:{None:"Ə"},1070:{None:"Yu"},1071:{None:"Ya"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1171:{None:"ğ"},1076:{None:"d"},1177:{None:"ź"},1077:{None:"e"},1105:{None:"yo"},1078:{None:"j"},1079:{None:"z"},1080:{None:"i"},1081:{None:"y"},1082:{None:"k"},1185:{None:"q"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1187:{None:"ñ"},1086:{None:"o"},1257:{None:"ö"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1195:{None:"ś"},1090:{None:"t"},1091:{None:"u"},1199:{None:"ü"},1092:{None:"f"},1093:{None:"x"},1211:{None:"h"},1094:{None:"ts"},1095:{None:"ç"},1096:{None:"ş"},1097:{None:"şç"},1098:{None:""},1099:{None:"ı"},1100:{None:""},1101:{None:"e"},1241:{None:"ə"},1102:{None:"yu"},1103:{None:"ya"}}
