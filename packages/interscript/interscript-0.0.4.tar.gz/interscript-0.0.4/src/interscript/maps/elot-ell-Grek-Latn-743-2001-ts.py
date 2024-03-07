import interscript
import regex as re
interscript.load_map("iso-ell-Grek-Latn-843-1997-t2")
interscript.stdlib.define_map("elot-ell-Grek-Latn-743-2001-ts")
def _stage_main(s):
    s = interscript.transliterate("iso-ell-Grek-Latn-843-1997-t2", s, "main")
    return s

interscript.stdlib.add_map_stage("elot-ell-Grek-Latn-743-2001-ts", "main", _stage_main)
