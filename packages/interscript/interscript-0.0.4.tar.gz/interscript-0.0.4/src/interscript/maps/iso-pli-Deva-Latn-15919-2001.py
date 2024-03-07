import interscript
import regex as re
interscript.load_map("iso-san-Deva-Latn-15919-2001")
interscript.stdlib.define_map("iso-pli-Deva-Latn-15919-2001")
def _stage_main(s):
    s = interscript.transliterate("iso-san-Deva-Latn-15919-2001", s, "main")
    return s

interscript.stdlib.add_map_stage("iso-pli-Deva-Latn-15919-2001", "main", _stage_main)
