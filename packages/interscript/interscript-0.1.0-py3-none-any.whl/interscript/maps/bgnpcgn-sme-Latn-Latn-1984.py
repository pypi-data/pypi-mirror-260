import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-sme-Latn-Latn-1984")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1755111520583703833)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-sme-Latn-Latn-1984", "main", _stage_main)
_PTREE_1755111520583703833 = {330:{None:"Ń"},331:{None:"ń"}}
