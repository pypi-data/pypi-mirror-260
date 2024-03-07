import interscript
import regex as re
interscript.load_map("var-kor-Kore-Hang-2013")
interscript.load_map("moct-kor-Hang-Latn-2000")
interscript.stdlib.define_map("bgnpcgn-kor-Kore-Latn-rok-2011")
def _stage_main(s):
    s = interscript.transliterate("var-kor-Kore-Hang-2013", s, "main")
    s = interscript.transliterate("moct-kor-Hang-Latn-2000", s, "main")
    return s

interscript.stdlib.add_map_stage("bgnpcgn-kor-Kore-Latn-rok-2011", "main", _stage_main)
