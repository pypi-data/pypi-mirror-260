import interscript
import regex as re
interscript.stdlib.define_map("odni-che-Cyrl-Latn-2015")
def _stage_main(s):
    s = re.compile("(?<!"+interscript.stdlib.aliases["boundary"]+"’)"+interscript.stdlib.aliases["boundary"]+"Е", re.MULTILINE).sub("Ye", s)
    s = re.compile("(?<!"+interscript.stdlib.aliases["boundary"]+"’)"+interscript.stdlib.aliases["boundary"]+"е", re.MULTILINE).sub("ye", s)
    s = re.compile("(?<="+interscript.stdlib.aliases["not_word"]+")1(?="+interscript.stdlib.aliases["not_word"]+")", re.MULTILINE).sub("ӏ", s)
    s = re.compile("(?<="+interscript.stdlib.aliases["not_word"]+")1", re.MULTILINE).sub("ӏ", s)
    s = re.compile("1(?="+interscript.stdlib.aliases["not_word"]+")", re.MULTILINE).sub("ӏ", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3718796117662126655)
    return s

interscript.stdlib.add_map_stage("odni-che-Cyrl-Latn-2015", "main", _stage_main)
_PTREE_3718796117662126655 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G",1216:{None:"Gh"}},1044:{None:"D"},1045:{None:"E"},1046:{None:"J"},1047:{None:"Z"},1048:{None:"I",1067:{None:"I"}},1067:{None:"Е"},1050:{None:"K",1216:{None:"K"},1093:{None:"Q"},1098:{None:"Q"}},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P",1216:{None:"Ph"}},1056:{None:"R"},1057:{None:"S"},1058:{None:"T",1216:{None:"T"}},1059:{None:"U"},1060:{None:"F"},1061:{None:"Kh",1100:{None:"H"},1216:{None:"H"}},1208:{None:"Ts",1216:{None:"Ts"}},1063:{None:"Ch",1216:{None:"Ch"}},1064:{None:"Sh"},1066:{None:"'"},1069:{None:"E"},1070:{None:"Yu"},1071:{None:"Ya"},1216:{None:"'"},1068:{None:""},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g",1231:{None:"gh"}},1076:{None:"d"},1077:{None:"e"},1078:{None:"j"},1079:{None:"z"},1080:{None:"i",1081:{None:"i"}},1081:{None:"y"},1082:{None:"k",1231:{None:"k"},1093:{None:"q"},1098:{None:"q"}},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t",1231:{None:"t"}},1091:{None:"u"},1092:{None:"f"},1093:{None:"kh",1100:{None:"h"},1231:{None:"h"}},1209:{None:"ts",1231:{None:"ts"}},1095:{None:"ch",1231:{None:"ch"}},1096:{None:"sh"},1098:{None:"'"},1099:{None:"e"},1101:{None:"e"},1102:{None:"yu"},1103:{None:"ya"},1231:{None:"'"},1100:{None:""}}
