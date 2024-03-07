import interscript
import regex as re
interscript.load_map("odni-ara-Arab-Latn-2015")
interscript.stdlib.define_map("odni-ara-Arab-Latn-2004")
def _stage_main(s):
    s = interscript.transliterate("odni-ara-Arab-Latn-2015", s, "main")
    return s

interscript.stdlib.add_map_stage("odni-ara-Arab-Latn-2004", "main", _stage_main)
