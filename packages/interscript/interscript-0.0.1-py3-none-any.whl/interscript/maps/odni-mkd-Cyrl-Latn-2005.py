import interscript
import regex as re
interscript.load_map("odni-mkd-Cyrl-Latn-2015")
interscript.stdlib.define_map("odni-mkd-Cyrl-Latn-2005")
def _stage_main(s):
    s = interscript.transliterate("odni-mkd-Cyrl-Latn-2015", s, "main")
    return s

interscript.stdlib.add_map_stage("odni-mkd-Cyrl-Latn-2005", "main", _stage_main)
