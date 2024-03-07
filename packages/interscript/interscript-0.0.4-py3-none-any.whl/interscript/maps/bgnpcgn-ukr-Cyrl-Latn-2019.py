import interscript
import regex as re
interscript.load_map("un-ukr-Cyrl-Latn-2012")
interscript.stdlib.define_map("bgnpcgn-ukr-Cyrl-Latn-2019")
def _stage_main(s):
    s = interscript.transliterate("un-ukr-Cyrl-Latn-2012", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2599968500252763974)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-ukr-Cyrl-Latn-2019", "main", _stage_main)
_PTREE_2599968500252763974 = {39:{None:""}}
