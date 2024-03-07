import interscript
import regex as re
interscript.load_map("var-kor-Kore-Hang-2013")
interscript.load_map("var-kor-Hang-Latn-mr-1939")
interscript.stdlib.define_map("var-kor-Kore-Latn-mr-1939")
def _stage_main(s):
    s = interscript.transliterate("var-kor-Kore-Hang-2013", s, "main")
    s = interscript.transliterate("var-kor-Hang-Latn-mr-1939", s, "main")
    s = interscript.functions.compose(s, {})
    s = interscript.functions.title_case(s, {})
    return s

interscript.stdlib.add_map_stage("var-kor-Kore-Latn-mr-1939", "main", _stage_main)
