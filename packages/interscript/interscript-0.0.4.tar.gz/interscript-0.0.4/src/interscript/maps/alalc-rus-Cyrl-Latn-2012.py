import interscript
import regex as re
interscript.load_map("alalc-rus-Cyrl-Latn-1997")
interscript.stdlib.define_map("alalc-rus-Cyrl-Latn-2012")
def _stage_main(s):
    s = interscript.transliterate("alalc-rus-Cyrl-Latn-1997", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1302002809107085107)
    return s

interscript.stdlib.add_map_stage("alalc-rus-Cyrl-Latn-2012", "main", _stage_main)
_PTREE_1302002809107085107 = {1030:{None:"Ī"},1110:{None:"ī"},1122:{None:"I͡E"},1123:{None:"i͡e"},1138:{None:"Ḟ"},1139:{None:"ḟ"},1140:{None:"Ẏ"},1141:{None:"ẏ"}}
