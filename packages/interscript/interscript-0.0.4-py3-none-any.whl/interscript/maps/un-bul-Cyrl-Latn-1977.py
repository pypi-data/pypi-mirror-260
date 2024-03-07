import interscript
import regex as re
interscript.load_map("posix")
interscript.stdlib.define_map("un-bul-Cyrl-Latn-1977")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_41742316272375607)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+"?)Št("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("\\1"+"ŠT"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+")Št("+interscript.stdlib.get_alias_re("posix", "upper")+"?)", re.MULTILINE).sub("\\1"+"ŠT"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+"?)Yu("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("\\1"+"YU"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+")Yu("+interscript.stdlib.get_alias_re("posix", "upper")+"?)", re.MULTILINE).sub("\\1"+"YU"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+"?)Ya("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("\\1"+"YA"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+")Ya("+interscript.stdlib.get_alias_re("posix", "upper")+"?)", re.MULTILINE).sub("\\1"+"YA"+"\\2", s)
    return s

interscript.stdlib.add_map_stage("un-bul-Cyrl-Latn-1977", "main", _stage_main)
_PTREE_41742316272375607 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1044:{None:"D"},1045:{None:"E"},1046:{None:"Ž"},1047:{None:"Z"},1048:{None:"I"},1049:{None:"J"},1050:{None:"K"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1060:{None:"F"},1061:{None:"H"},1062:{None:"C"},1063:{None:"Č"},1064:{None:"Š"},1065:{None:"Št"},1066:{None:"Ǎ"},1068:{None:"J"},1070:{None:"Yu"},1071:{None:"Ya"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1076:{None:"d"},1077:{None:"e"},1078:{None:"ž"},1079:{None:"z"},1080:{None:"i"},1081:{None:"j"},1082:{None:"k"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1092:{None:"f"},1093:{None:"h"},1094:{None:"c"},1095:{None:"č"},1096:{None:"š"},1097:{None:"št"},1098:{None:"ǎ"},1100:{None:"j"},1102:{None:"yu"},1103:{None:"ya"}}
