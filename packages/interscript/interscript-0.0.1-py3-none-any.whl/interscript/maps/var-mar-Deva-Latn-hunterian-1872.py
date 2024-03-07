import interscript
import regex as re
interscript.load_map("var-hin-Deva-Latn-hunterian-1872")
interscript.stdlib.define_map("var-mar-Deva-Latn-hunterian-1872")
def _stage_main(s):
    s = interscript.transliterate("var-hin-Deva-Latn-hunterian-1872", s, "main")
    return s

interscript.stdlib.add_map_stage("var-mar-Deva-Latn-hunterian-1872", "main", _stage_main)
