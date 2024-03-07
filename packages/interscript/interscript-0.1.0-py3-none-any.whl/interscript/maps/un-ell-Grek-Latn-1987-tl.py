import interscript
import regex as re
interscript.load_map("elot-ell-Grek-Latn-743-1982-tl")
interscript.stdlib.define_map("un-ell-Grek-Latn-1987-tl")
def _stage_main(s):
    s = interscript.transliterate("elot-ell-Grek-Latn-743-1982-tl", s, "main")
    return s

interscript.stdlib.add_map_stage("un-ell-Grek-Latn-1987-tl", "main", _stage_main)
