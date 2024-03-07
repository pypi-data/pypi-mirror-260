import interscript
import regex as re
interscript.load_map("bgnpcgn-srp-Cyrl-Latn-2005")
interscript.stdlib.define_map("bgnpcgn-srp-Cyrl-Latn-1962")
def _stage_main(s):
    s = interscript.transliterate("bgnpcgn-srp-Cyrl-Latn-2005", s, "main")
    return s

interscript.stdlib.add_map_stage("bgnpcgn-srp-Cyrl-Latn-1962", "main", _stage_main)
