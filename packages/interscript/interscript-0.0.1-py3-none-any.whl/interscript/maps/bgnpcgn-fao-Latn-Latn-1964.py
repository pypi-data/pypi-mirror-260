import interscript
import regex as re
interscript.load_map("bgnpcgn-isl-Latn-Latn-1964")
interscript.stdlib.define_map("bgnpcgn-fao-Latn-Latn-1964")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_535214406135556975)
    s = interscript.transliterate("bgnpcgn-isl-Latn-Latn-1964", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1661262374662432095)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-fao-Latn-Latn-1964", "main", _stage_main)
_PTREE_535214406135556975 = {222:{None:"<XXX>"},254:{None:"<xxx>"}}
_PTREE_1661262374662432095 = {60:{88:{88:{88:{62:{None:"Þ"}}}},120:{120:{120:{62:{None:"þ"}}}}}}
