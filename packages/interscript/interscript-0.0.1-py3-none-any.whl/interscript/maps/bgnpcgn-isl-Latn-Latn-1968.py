import interscript
import regex as re
interscript.load_map("bgnpcgn-isl-Latn-Latn-1964")
interscript.stdlib.define_map("bgnpcgn-isl-Latn-Latn-1968")
def _stage_main(s):
    s = interscript.transliterate("bgnpcgn-isl-Latn-Latn-1964", s, "main")
    return s

interscript.stdlib.add_map_stage("bgnpcgn-isl-Latn-Latn-1968", "main", _stage_main)
