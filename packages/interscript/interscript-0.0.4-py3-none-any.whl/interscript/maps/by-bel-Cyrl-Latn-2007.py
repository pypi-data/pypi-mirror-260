import interscript
import regex as re
interscript.load_map("by-bel-Cyrl-Latn-1998")
interscript.stdlib.define_map("by-bel-Cyrl-Latn-2007")
def _stage_main(s):
    s = interscript.transliterate("by-bel-Cyrl-Latn-1998", s, "main")
    return s

interscript.stdlib.add_map_stage("by-bel-Cyrl-Latn-2007", "main", _stage_main)
