import interscript
import regex as re
interscript.load_map("sasm-mon-Mong-Latn-phonetic-1978")
interscript.stdlib.define_map("un-mon-Mong-Latn-phonetic-2013")
def _stage_main(s):
    s = interscript.transliterate("sasm-mon-Mong-Latn-phonetic-1978", s, "main")
    return s

interscript.stdlib.add_map_stage("un-mon-Mong-Latn-phonetic-2013", "main", _stage_main)
