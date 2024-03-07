import interscript
import regex as re
interscript.load_map("gost-rus-Cyrl-Latn-16876-71-1983")
interscript.load_map("var-Cyrl")
interscript.stdlib.define_map("by-bel-Cyrl-Latn-1998")
def _stage_main(s):
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")Е", re.MULTILINE).sub("IE", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")е", re.MULTILINE).sub("ie", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")Ё", re.MULTILINE).sub("IO", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")ё", re.MULTILINE).sub("io", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")Ю", re.MULTILINE).sub("IU", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")ю", re.MULTILINE).sub("iu", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")Я", re.MULTILINE).sub("IA", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-Cyrl", "bel_consonant")+")я", re.MULTILINE).sub("ia", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_676267179593490491)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_954313604571989899)
    s = interscript.transliterate("gost-rus-Cyrl-Latn-16876-71-1983", s, "main")
    return s

interscript.stdlib.add_map_stage("by-bel-Cyrl-Latn-1998", "main", _stage_main)
_PTREE_676267179593490491 = {1047:{1068:{None:"Ź"}},1079:{1100:{None:"ź"}},1051:{1068:{None:"Ĺ"}},1083:{1100:{None:"ĺ"}},1057:{1068:{None:"Ś"}},1089:{1100:{None:"ś"}},1062:{1068:{None:"Ć"}},1094:{1100:{None:"ć"}},1053:{1068:{None:"Ń"}},1085:{1100:{None:"ń"}}}
_PTREE_954313604571989899 = {1030:{None:"I"},1043:{None:"H"},1045:{None:"Je"},1025:{None:"Jo"},1038:{None:"Ŭ"},1061:{None:"Ch"},1068:{None:""},1069:{None:"E"},1070:{None:"Ju"},1071:{None:"Ja"},1075:{None:"h"},1110:{None:"i"},1077:{None:"je"},1105:{None:"jo"},1118:{None:"ŭ"},1093:{None:"ch"},1100:{None:""},1101:{None:"e"},1102:{None:"ju"},1103:{None:"ja"},39:{None:""}}
