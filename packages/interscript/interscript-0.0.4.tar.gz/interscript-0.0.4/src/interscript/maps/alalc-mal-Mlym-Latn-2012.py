import interscript
import regex as re
interscript.load_map("alalc-mal-Mlym-Latn-1997")
interscript.stdlib.define_map("alalc-mal-Mlym-Latn-2012")
def _stage_main(s):
    s = interscript.transliterate("alalc-mal-Mlym-Latn-1997", s, "main")
    return s

interscript.stdlib.add_map_stage("alalc-mal-Mlym-Latn-2012", "main", _stage_main)
