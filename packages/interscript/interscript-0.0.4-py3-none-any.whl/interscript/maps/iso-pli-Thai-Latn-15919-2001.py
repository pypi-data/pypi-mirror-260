import interscript
import regex as re
interscript.load_map("iso-tha-Thai-Latn-11940-1998")
interscript.stdlib.define_map("iso-pli-Thai-Latn-15919-2001")
def _stage_main(s):
    s = interscript.transliterate("iso-tha-Thai-Latn-11940-1998", s, "main")
    return s

interscript.stdlib.add_map_stage("iso-pli-Thai-Latn-15919-2001", "main", _stage_main)
