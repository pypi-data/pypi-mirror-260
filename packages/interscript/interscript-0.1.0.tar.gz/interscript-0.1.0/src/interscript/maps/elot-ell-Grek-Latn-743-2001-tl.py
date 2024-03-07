import interscript
import regex as re
interscript.load_map("iso-ell-Grek-Latn-843-1997-t1")
interscript.stdlib.define_map("elot-ell-Grek-Latn-743-2001-tl")
def _stage_main(s):
    s = interscript.transliterate("iso-ell-Grek-Latn-843-1997-t1", s, "main")
    return s

interscript.stdlib.add_map_stage("elot-ell-Grek-Latn-743-2001-tl", "main", _stage_main)
