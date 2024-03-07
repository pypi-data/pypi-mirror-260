import interscript
import regex as re
interscript.load_map("alalc-asm-Deva-Latn-1997")
interscript.stdlib.define_map("alalc-asm-Deva-Latn-2012")
def _stage_main(s):
    s = interscript.transliterate("alalc-asm-Deva-Latn-1997", s, "main")
    return s

interscript.stdlib.add_map_stage("alalc-asm-Deva-Latn-2012", "main", _stage_main)
