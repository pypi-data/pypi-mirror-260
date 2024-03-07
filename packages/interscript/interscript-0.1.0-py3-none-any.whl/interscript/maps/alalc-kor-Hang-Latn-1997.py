import interscript
import regex as re
interscript.load_map("var-kor-Hang-Latn-mr-1939")
interscript.stdlib.define_map("alalc-kor-Hang-Latn-1997")
def _stage_main(s):
    s = interscript.transliterate("var-kor-Hang-Latn-mr-1939", s, "main")
    s = interscript.functions.compose(s, {})
    s = interscript.functions.title_case(s, {})
    return s

interscript.stdlib.add_map_stage("alalc-kor-Hang-Latn-1997", "main", _stage_main)
