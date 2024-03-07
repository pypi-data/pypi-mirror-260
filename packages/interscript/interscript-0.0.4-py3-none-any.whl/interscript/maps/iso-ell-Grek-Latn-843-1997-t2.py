import interscript
import regex as re
interscript.load_map("elot-ell-Grek-Latn-743-1982-ts")
interscript.stdlib.define_map("iso-ell-Grek-Latn-843-1997-t2")
def _stage_main(s):
    s = interscript.transliterate("elot-ell-Grek-Latn-743-1982-ts", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4227155468880292713)
    return s

interscript.stdlib.add_map_stage("iso-ell-Grek-Latn-843-1997-t2", "main", _stage_main)
_PTREE_4227155468880292713 = {988:{None:"W"},989:{None:"w"},1010:{None:"s"},1017:{None:"S"},1011:{None:"j"},895:{None:"j"}}
