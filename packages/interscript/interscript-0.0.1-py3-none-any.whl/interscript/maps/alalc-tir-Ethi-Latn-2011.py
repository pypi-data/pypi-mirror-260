import interscript
import regex as re
interscript.load_map("alalc-tir-Ethi-Latn-1997")
interscript.stdlib.define_map("alalc-tir-Ethi-Latn-2011")
def _stage_main(s):
    s = interscript.transliterate("alalc-tir-Ethi-Latn-1997", s, "main")
    return s

interscript.stdlib.add_map_stage("alalc-tir-Ethi-Latn-2011", "main", _stage_main)
