import interscript
import regex as re
interscript.stdlib.define_map("odni-mkd-Cyrl-Latn-2015")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_853485945733505971)
    return s

interscript.stdlib.add_map_stage("odni-mkd-Cyrl-Latn-2015", "main", _stage_main)
_PTREE_853485945733505971 = {83:{None:"Dz"},115:{None:"dz"},1040:{None:"A"},1041:{None:"B"},1042:{None:"V"},1043:{None:"G"},1044:{None:"D"},1027:{None:"Gj"},1045:{None:"E"},1046:{None:"Zh"},1047:{None:"Z"},1048:{None:"I"},1032:{None:"J"},1050:{None:"K"},1051:{None:"L"},1033:{None:"Lj"},1052:{None:"M"},1053:{None:"N"},1034:{None:"Nj"},1054:{None:"O"},1055:{None:"P"},1056:{None:"R"},1057:{None:"S"},1058:{None:"T"},1036:{None:"Kj"},1059:{None:"U"},1060:{None:"F"},1061:{None:"H"},1062:{None:"Ts"},1063:{None:"Ch"},1039:{None:"Dzh"},1064:{None:"Sh"},8217:{None:""},1072:{None:"a"},1073:{None:"b"},1074:{None:"v"},1075:{None:"g"},1076:{None:"d"},1107:{None:"gj"},1077:{None:"e"},1078:{None:"zh"},1079:{None:"z"},1080:{None:"i"},1112:{None:"j"},1082:{None:"k"},1083:{None:"l"},1113:{None:"lj"},1084:{None:"m"},1085:{None:"n"},1114:{None:"nj"},1086:{None:"o"},1087:{None:"p"},1088:{None:"r"},1089:{None:"s"},1090:{None:"t"},1116:{None:"kj"},1091:{None:"u"},1092:{None:"f"},1093:{None:"h"},1094:{None:"ts"},1095:{None:"ch"},1119:{None:"dzh"},1096:{None:"sh"}}
