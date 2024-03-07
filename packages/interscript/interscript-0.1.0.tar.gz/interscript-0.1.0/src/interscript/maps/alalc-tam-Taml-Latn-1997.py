import interscript
import regex as re
interscript.load_map("din-tam-Taml-Latn-33903-2016")
interscript.stdlib.define_map("alalc-tam-Taml-Latn-1997")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3126061212979072067)
    s = interscript.transliterate("din-tam-Taml-Latn-33903-2016", s, "main")
    return s

interscript.stdlib.add_map_stage("alalc-tam-Taml-Latn-1997", "main", _stage_main)
_PTREE_3126061212979072067 = {2947:{None:"ḵa"}}
