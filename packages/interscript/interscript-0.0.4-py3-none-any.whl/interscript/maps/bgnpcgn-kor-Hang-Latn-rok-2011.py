import interscript
import regex as re
interscript.load_map("moct-kor-Hang-Latn-2000")
interscript.stdlib.define_map("bgnpcgn-kor-Hang-Latn-rok-2011")
def _stage_main(s):
    s = interscript.transliterate("moct-kor-Hang-Latn-2000", s, "main")
    s = interscript.functions.title_case(s, {})
    return s

interscript.stdlib.add_map_stage("bgnpcgn-kor-Hang-Latn-rok-2011", "main", _stage_main)
