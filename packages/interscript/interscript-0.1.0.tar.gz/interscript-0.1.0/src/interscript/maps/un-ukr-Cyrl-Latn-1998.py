import interscript
import regex as re
interscript.load_map("gost-rus-Cyrl-Latn-16876-71-1983")
interscript.stdlib.define_map("un-ukr-Cyrl-Latn-1998")
def _stage_main(s):
    s = interscript.transliterate("gost-rus-Cyrl-Latn-16876-71-1983", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1515013442947141536)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("un-ukr-Cyrl-Latn-1998", "main", _stage_main)
_PTREE_1515013442947141536 = {1025:{None:""},1028:{None:"Ê"},1030:{None:"Ì"},1031:{None:"Ì"},1067:{None:""},1069:{None:""},1105:{None:""},1108:{None:"ê"},1110:{None:"ı̀"},1111:{None:"ı̀"},1099:{None:""},1101:{None:""}}
