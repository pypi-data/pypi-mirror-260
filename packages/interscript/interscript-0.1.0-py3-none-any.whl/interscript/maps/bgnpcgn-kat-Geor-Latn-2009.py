import interscript
import regex as re
interscript.load_map("ggg-kat-Geor-Latn-2002")
interscript.stdlib.define_map("bgnpcgn-kat-Geor-Latn-2009")
def _stage_main(s):
    s = interscript.transliterate("ggg-kat-Geor-Latn-2002", s, "main")
    return s

interscript.stdlib.add_map_stage("bgnpcgn-kat-Geor-Latn-2009", "main", _stage_main)
