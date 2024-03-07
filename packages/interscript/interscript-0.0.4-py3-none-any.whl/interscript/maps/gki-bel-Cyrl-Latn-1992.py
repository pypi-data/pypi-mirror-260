import interscript
import regex as re
interscript.load_map("gost-rus-Cyrl-Latn-16876-71-1983")
interscript.stdlib.define_map("gki-bel-Cyrl-Latn-1992")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3558557245853608675)
    s = interscript.transliterate("gost-rus-Cyrl-Latn-16876-71-1983", s, "main")
    return s

interscript.stdlib.add_map_stage("gki-bel-Cyrl-Latn-1992", "main", _stage_main)
_PTREE_3558557245853608675 = {1030:{None:"I"},1110:{None:"i"},1043:{None:"G"},1075:{None:"g"},1038:{None:"Ŭ"},1118:{None:"ŭ"},1070:{None:"Ju"},1102:{None:"ju"},1071:{None:"Ja"},1103:{None:"ja"}}
