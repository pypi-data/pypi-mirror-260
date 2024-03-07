import interscript
import regex as re
interscript.load_map("elot-ell-Grek-Latn-743-1982-ts")
interscript.stdlib.define_map("bgnpcgn-ell-Grek-Latn-1996")
def _stage_main(s):
    s = interscript.transliterate("elot-ell-Grek-Latn-743-1982-ts", s, "main")
    return s

interscript.stdlib.add_map_stage("bgnpcgn-ell-Grek-Latn-1996", "main", _stage_main)
