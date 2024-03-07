import interscript
import regex as re
interscript.load_map("var-san-Deva-Latn-iast-1912")
interscript.stdlib.define_map("var-pra-Deva-Latn-iast-1912")
def _stage_main(s):
    s = interscript.transliterate("var-san-Deva-Latn-iast-1912", s, "main")
    return s

interscript.stdlib.add_map_stage("var-pra-Deva-Latn-iast-1912", "main", _stage_main)
