import interscript
import regex as re
interscript.load_map("var-amh-Ethi-Latn-eae-2003")
interscript.stdlib.define_map("var-gez-Ethi-Latn-eae-2003")
def _stage_main(s):
    s = interscript.transliterate("var-amh-Ethi-Latn-eae-2003", s, "main")
    return s

interscript.stdlib.add_map_stage("var-gez-Ethi-Latn-eae-2003", "main", _stage_main)
