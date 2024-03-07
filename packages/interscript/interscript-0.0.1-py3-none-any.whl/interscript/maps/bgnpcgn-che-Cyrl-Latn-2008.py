import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-che-Cyrl-Latn-2008")
def _stage_main(s):
    s = re.compile("(?<!"+interscript.stdlib.aliases["boundary"]+"’)"+interscript.stdlib.aliases["boundary"]+"Е", re.MULTILINE).sub("Ye", s)
    s = re.compile("(?<!"+interscript.stdlib.aliases["boundary"]+"’)"+interscript.stdlib.aliases["boundary"]+"е", re.MULTILINE).sub("ye", s)
    s = re.compile("ккх", re.MULTILINE).sub("qq", s)
    s = re.compile("ккЪ", re.MULTILINE).sub("q̇q̇", s)
    s = re.compile("ККх", re.MULTILINE).sub("QQ", s)
    s = re.compile("ККЪ", re.MULTILINE).sub("Q̇Q̇", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4410364427963153957)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bgnpcgn-che-Cyrl-Latn-2008", "main", _stage_main)
_PTREE_4410364427963153957 = {1040:{None:"A",1100:{None:"Ä"}},1041:{None:"B"},1042:{None:"V"},1043:{None:"G",1216:{None:"Ġ"}},1044:{None:"D"},1045:{None:"E"},1025:{None:"Yo"},1046:{None:"Z̵"},1047:{None:"Z"},1048:{None:"I"},1067:{None:"Y"},1050:{None:"K",1093:{None:"Q"},1098:{None:"Q̇"},1216:{None:"Kh"}},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O",1100:{None:"Ö"}},1055:{None:"P",1216:{None:"Ph"}},1056:{None:"R"},1057:{None:"S"},1058:{None:"T",1216:{None:"Th"}},1059:{None:"U",1100:{None:"Ü"}},1060:{None:"F"},1061:{None:"X",1100:{None:"Ẋ"},1216:{None:"H"}},1208:{None:"C",1216:{None:"Ċ"}},1063:{None:"Ç",1216:{None:"Ç̇"}},1064:{None:"Ş"},1065:{None:"ŞÇ"},1066:{None:"’"},1068:{None:""},1069:{None:"E"},1070:{None:"Yu",1100:{None:"Yü"}},1071:{None:"Ya",1100:{None:"Yä"}},1216:{None:"J"},1072:{None:"a",1100:{None:"ä"}},1073:{None:"b"},1074:{None:"v"},1075:{None:"g",1231:{None:"ġ"}},1076:{None:"d"},1077:{None:"e"},1105:{None:"yo"},1078:{None:"z̵"},1079:{None:"z"},1080:{None:"i"},1081:{None:"y"},1082:{None:"k",1093:{None:"q"},1098:{None:"q̇"},1231:{None:"kh"}},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o",1100:{None:"ö"}},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t",1231:{None:"th"}},1091:{None:"u",1100:{None:"ü"}},1092:{None:"f"},1093:{None:"x",1100:{None:"ẋ"},1231:{None:"h"}},1209:{None:"c",1231:{None:"с̇"}},1095:{None:"ç",1231:{None:"cç̇"}},1096:{None:"ş"},1097:{None:"şç"},1098:{None:"’"},1099:{None:"y"},1100:{None:""},1101:{None:"e"},1102:{None:"yü"},1103:{None:"yä"},1231:{None:"j"}}
