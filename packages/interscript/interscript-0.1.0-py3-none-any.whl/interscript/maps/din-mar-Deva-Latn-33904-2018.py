import interscript
import regex as re
interscript.load_map("din-san-Deva-Latn-33904-2018")
interscript.stdlib.define_map("din-mar-Deva-Latn-33904-2018")
def _stage_main(s):
    s = interscript.transliterate("din-san-Deva-Latn-33904-2018", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3831120084244564714)
    return s

interscript.stdlib.add_map_stage("din-mar-Deva-Latn-33904-2018", "main", _stage_main)
_PTREE_3831120084244564714 = {2418:{None:"ê"},2321:{None:"ô"}}
