import interscript
import regex as re
interscript.load_map("var-Cyrl")
interscript.stdlib.define_map("gki-bel-Cyrl-Latn-2000")
def _stage_main(s):
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")Е", re.MULTILINE).sub("IE", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")е", re.MULTILINE).sub("ie", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")Ё", re.MULTILINE).sub("IO", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")ё", re.MULTILINE).sub("io", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")Ю", re.MULTILINE).sub("IU", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")ю", re.MULTILINE).sub("iu", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")Я", re.MULTILINE).sub("IA", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")я", re.MULTILINE).sub("ia", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1819753040975380253)
    s = re.compile("Ь", re.MULTILINE).sub("'", s)
    s = re.compile("ь", re.MULTILINE).sub("'", s)
    return s

interscript.stdlib.add_map_stage("gki-bel-Cyrl-Latn-2000", "main", _stage_main)
_PTREE_1819753040975380253 = {39:{None:""},1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"H"},1044:{None:"D"},1045:{None:"Je"},1025:{None:"Jo"},1046:{None:"Ž"},1047:{None:"Z"},1030:{None:"I"},1049:{None:"J"},1050:{None:"K"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},85:{48:{52:{48:{69:{None:"Ŭ"}}}}},1060:{None:"F"},1061:{None:"Ch"},1062:{None:"C"},1063:{None:"Č"},1064:{None:"Š"},1067:{None:"Y"},1069:{None:"E"},1070:{None:"Ju"},1071:{None:"Ja"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"h"},1076:{None:"d"},1077:{None:"je"},1105:{None:"jo"},1078:{None:"ž"},1079:{None:"z"},1110:{None:"i"},1081:{None:"j"},1082:{None:"k"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1118:{None:"ŭ"},1092:{None:"f"},1093:{None:"ch"},1094:{None:"c"},1095:{None:"č"},1096:{None:"š"},1099:{None:"y"},1101:{None:"e"},1102:{None:"ju"},1103:{None:"ja"}}
