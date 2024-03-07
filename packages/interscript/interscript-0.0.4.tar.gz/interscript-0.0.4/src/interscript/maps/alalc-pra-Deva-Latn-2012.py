import interscript
import regex as re
interscript.load_map("alalc-san-Deva-Latn-2012")
interscript.stdlib.define_map("alalc-pra-Deva-Latn-2012")
def _stage_main(s):
    s = interscript.transliterate("alalc-san-Deva-Latn-2012", s, "main")
    return s

interscript.stdlib.add_map_stage("alalc-pra-Deva-Latn-2012", "main", _stage_main)
