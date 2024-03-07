import interscript
import regex as re
interscript.load_map("var-kor-Kore-Hang-2013")
interscript.load_map("bgn-kor-Hang-Latn-1943")
interscript.stdlib.define_map("bgn-kor-Kore-Latn-1943")
def _stage_main(s):
    s = interscript.transliterate("var-kor-Kore-Hang-2013", s, "main")
    s = interscript.transliterate("bgn-kor-Hang-Latn-1943", s, "main")
    s = interscript.functions.compose(s, {})
    s = interscript.functions.title_case(s, {})
    return s

interscript.stdlib.add_map_stage("bgn-kor-Kore-Latn-1943", "main", _stage_main)
