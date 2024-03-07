import interscript
import regex as re
interscript.load_map("posix")
interscript.stdlib.define_map("alalc-mkd-Cyrl-Latn-1997")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2424993385471402695)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+"?)Dz("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("\\1"+"DZ"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+")Dz("+interscript.stdlib.get_alias_re("posix", "upper")+"?)", re.MULTILINE).sub("\\1"+"DZ"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+")Lj("+interscript.stdlib.get_alias_re("posix", "upper")+"?)", re.MULTILINE).sub("\\1"+"LJ"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+"?)Lj("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("\\1"+"LJ"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+")Nj("+interscript.stdlib.get_alias_re("posix", "upper")+"?)", re.MULTILINE).sub("\\1"+"NJ"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+"?)Nj("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("\\1"+"NJ"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+")Dž("+interscript.stdlib.get_alias_re("posix", "upper")+"?)", re.MULTILINE).sub("\\1"+"DŽ"+"\\2", s)
    s = re.compile("("+interscript.stdlib.get_alias_re("posix", "upper")+"?)Dž("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("\\1"+"DŽ"+"\\2", s)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("alalc-mkd-Cyrl-Latn-1997", "main", _stage_main)
_PTREE_2424993385471402695 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1027:{None:"Ǵ"},1044:{None:"D"},1026:{None:"Đ"},1045:{None:"E"},1046:{None:"Ž"},1047:{None:"Z"},1029:{None:"Dz"},1048:{None:"I"},1032:{None:"J"},1050:{None:"K"},1036:{None:"Ḱ"},1051:{None:"L"},1033:{None:"Lj"},1052:{None:"M"},1053:{None:"N"},1034:{None:"Nj"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1035:{None:"Ć"},1059:{None:"U"},1060:{None:"F"},1061:{None:"H"},1062:{None:"C"},1063:{None:"Č"},1039:{None:"Dž"},1064:{None:"Š"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1107:{None:"ǵ"},1076:{None:"d"},1106:{None:"đ"},1077:{None:"e"},1078:{None:"ž"},1079:{None:"z"},1109:{None:"dz"},1080:{None:"i"},1112:{None:"j"},1082:{None:"k"},1116:{None:"ḱ"},1083:{None:"l"},1113:{None:"lj"},1084:{None:"m"},1085:{None:"n"},1114:{None:"nj"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1115:{None:"ć"},1091:{None:"u"},1092:{None:"f"},1093:{None:"h"},1094:{None:"c"},1095:{None:"č"},1119:{None:"dž"},1096:{None:"š"}}
