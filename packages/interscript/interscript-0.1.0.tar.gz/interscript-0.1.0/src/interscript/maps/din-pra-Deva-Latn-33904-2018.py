import interscript
import regex as re
interscript.load_map("din-san-Deva-Latn-33904-2018")
interscript.stdlib.define_map("din-pra-Deva-Latn-33904-2018")
def _stage_main(s):
    s = interscript.transliterate("din-san-Deva-Latn-33904-2018", s, "main")
    return s

interscript.stdlib.add_map_stage("din-pra-Deva-Latn-33904-2018", "main", _stage_main)
