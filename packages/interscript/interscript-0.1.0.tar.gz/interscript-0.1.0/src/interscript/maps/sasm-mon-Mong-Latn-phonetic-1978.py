import interscript
import regex as re
interscript.load_map("sasm-mon-Mong-Latn-general-1978")
interscript.stdlib.define_map("sasm-mon-Mong-Latn-phonetic-1978")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4175569335936885993)
    s = interscript.transliterate("sasm-mon-Mong-Latn-general-1978", s, "main")
    return s

interscript.stdlib.add_map_stage("sasm-mon-Mong-Latn-phonetic-1978", "main", _stage_main)
_PTREE_4175569335936885993 = {6179:{None:"ô"},6180:{None:"û"}}
