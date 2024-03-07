import interscript
import regex as re
interscript.load_map("apcbg-bul-Cyrl-Latn-1995")
interscript.stdlib.define_map("bgna-bul-Cyrl-Latn-2009")
def _stage_main(s):
    s = interscript.transliterate("apcbg-bul-Cyrl-Latn-1995", s, "main")
    return s

interscript.stdlib.add_map_stage("bgna-bul-Cyrl-Latn-2009", "main", _stage_main)
