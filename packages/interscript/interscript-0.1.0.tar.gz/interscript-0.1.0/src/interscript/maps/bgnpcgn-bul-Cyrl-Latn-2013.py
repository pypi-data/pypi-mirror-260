import interscript
import regex as re
interscript.load_map("bgnpcgn-bul-Cyrl-Latn-1952")
interscript.stdlib.define_map("bgnpcgn-bul-Cyrl-Latn-2013")
def _stage_main(s):
    s = re.compile("България", re.MULTILINE).sub("Bulgaria", s)
    s = re.compile("(?<=И)Я(?="+interscript.stdlib.aliases["boundary"]+")", re.MULTILINE).sub("A", s)
    s = re.compile("(?<=и)я(?="+interscript.stdlib.aliases["boundary"]+")", re.MULTILINE).sub("a", s)
    s = interscript.transliterate("bgnpcgn-bul-Cyrl-Latn-1952", s, "main")
    return s

interscript.stdlib.add_map_stage("bgnpcgn-bul-Cyrl-Latn-2013", "main", _stage_main)
