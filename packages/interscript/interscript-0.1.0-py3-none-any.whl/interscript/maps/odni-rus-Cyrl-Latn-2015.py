import interscript
import regex as re
interscript.load_map("bgnpcgn-rus-Cyrl-Latn-1947")
interscript.stdlib.define_map("odni-rus-Cyrl-Latn-2015")
def _stage_main(s):
    s = interscript.transliterate("bgnpcgn-rus-Cyrl-Latn-1947", s, "main")
    s = re.compile("’", re.MULTILINE).sub(interscript.stdlib.aliases["none"], s)
    return s

interscript.stdlib.add_map_stage("odni-rus-Cyrl-Latn-2015", "main", _stage_main)
