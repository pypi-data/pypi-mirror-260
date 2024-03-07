import interscript
import regex as re
interscript.load_map("bgnpcgn-bul-Cyrl-Latn-2013")
interscript.stdlib.define_map("odni-bul-Cyrl-Latn-2015")
def _stage_main(s):
    s = re.compile("Ь", re.MULTILINE).sub("Y", s)
    s = re.compile("Ъ", re.MULTILINE).sub("A", s)
    s = re.compile("ь", re.MULTILINE).sub("y", s)
    s = re.compile("ъ", re.MULTILINE).sub("a", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3379237711662954239)
    s = interscript.transliterate("bgnpcgn-bul-Cyrl-Latn-2013", s, "main")
    return s

interscript.stdlib.add_map_stage("odni-bul-Cyrl-Latn-2015", "main", _stage_main)
_PTREE_3379237711662954239 = {1096:{None:"sh",1096:{None:"sh",1096:{None:"sh",1096:{None:"sh",1096:{None:"sh",1096:{None:"sh"}}}}}},1095:{None:"ch",1095:{None:"ch",1095:{None:"ch",1095:{None:"ch",1095:{None:"ch",1095:{None:"ch"}}}}}}}
