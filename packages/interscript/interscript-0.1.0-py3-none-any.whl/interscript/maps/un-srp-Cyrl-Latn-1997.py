import interscript
import regex as re
interscript.load_map("alalc-srp-Cyrl-Latn-2013")
interscript.stdlib.define_map("un-srp-Cyrl-Latn-1997")
def _stage_main(s):
    s = interscript.transliterate("alalc-srp-Cyrl-Latn-2013", s, "main")
    return s

interscript.stdlib.add_map_stage("un-srp-Cyrl-Latn-1997", "main", _stage_main)
