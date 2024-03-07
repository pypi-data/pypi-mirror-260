import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-ron-Cyrl-Latn-2002")
def _stage_main(s):
    s = re.compile("Г(?=[ЕеИиЙйЮю])", re.MULTILINE).sub("Gh", s)
    s = re.compile("г(?=[ЕеИиЙйЮю])", re.MULTILINE).sub("gh", s)
    s = re.compile("Ӂ(?=[ЕеИиЙйЮю])", re.MULTILINE).sub("Gh", s)
    s = re.compile("Ӂ(?=[ЕеИиЙйЮю])", re.MULTILINE).sub("gh", s)
    s = re.compile("К(?=[ЕеИиЙйЮю])", re.MULTILINE).sub("Ch", s)
    s = re.compile("к(?=[ЕеИиЙйЮю])", re.MULTILINE).sub("ch", s)
    s = re.compile("Ч(?=[ЕеИиЙйЮю])", re.MULTILINE).sub("C", s)
    s = re.compile("ч(?=[ЕеИиЙйЮю])", re.MULTILINE).sub("c", s)
    s = re.compile("Ӂ(?=[Аа])", re.MULTILINE).sub("Ge", s)
    s = re.compile("Ӂ(?=[Аа])", re.MULTILINE).sub("ge", s)
    s = re.compile("Ч(?=[А])", re.MULTILINE).sub("CE", s)
    s = re.compile("Ч(?=[а])", re.MULTILINE).sub("Ce", s)
    s = re.compile("ч(?=[Аа])", re.MULTILINE).sub("ce", s)
    s = re.compile("Ь(?="+interscript.stdlib.aliases["boundary"]+")", re.MULTILINE).sub("I", s)
    s = re.compile("ь(?="+interscript.stdlib.aliases["boundary"]+")", re.MULTILINE).sub("i", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4163524738724767104)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-ron-Cyrl-Latn-2002", "main", _stage_main)
_PTREE_4163524738724767104 = {1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1044:{None:"D"},1045:{None:"E"},1046:{None:"ZH"},1217:{None:"GI"},1047:{None:"Z"},1048:{None:"I"},1049:{None:"I"},1050:{None:"C"},1051:{None:"L"},1052:{None:"M"},1053:{None:"N"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1059:{None:"U"},1060:{None:"F"},1061:{None:"H"},1062:{None:"Ţ"},1063:{None:"CI"},1064:{None:"Ş"},1067:{None:"Î"},1068:{None:"’"},1069:{None:"Ă"},1070:{None:"IU"},1071:{None:"EA"},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1076:{None:"d"},1077:{None:"e"},1078:{None:"zh"},1218:{None:"gi"},1079:{None:"z"},1080:{None:"i"},1081:{None:"i"},1082:{None:"c"},1083:{None:"l"},1084:{None:"m"},1085:{None:"n"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1091:{None:"u"},1092:{None:"f"},1093:{None:"h"},1094:{None:"ţ"},1095:{None:"ci"},1096:{None:"ş"},1099:{None:"î"},1100:{None:"’"},1101:{None:"ă"},1102:{None:"iu"},1103:{None:"ea"}}
