import interscript
import regex as re
interscript.load_map("ua-ukr-Cyrl-Latn-2010")
interscript.stdlib.define_map("un-ukr-Cyrl-Latn-2012")
def _stage_main(s):
    s = interscript.transliterate("ua-ukr-Cyrl-Latn-2010", s, "main")
    return s

interscript.stdlib.add_map_stage("un-ukr-Cyrl-Latn-2012", "main", _stage_main)
