import interscript
import regex as re
interscript.load_map("un-nep-Deva-Latn-1972")
interscript.stdlib.define_map("un-nep-Deva-Latn-2013")
def _stage_main(s):
    s = interscript.transliterate("un-nep-Deva-Latn-1972", s, "main")
    return s

interscript.stdlib.add_map_stage("un-nep-Deva-Latn-2013", "main", _stage_main)
