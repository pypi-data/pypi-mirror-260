import interscript
import regex as re
interscript.load_map("bgnpcgn-nep-Deva-Latn-2011")
interscript.stdlib.define_map("dos-nep-Deva-Latn-1997")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3275275814051667310)
    s = interscript.transliterate("bgnpcgn-nep-Deva-Latn-2011", s, "main")
    return s

interscript.stdlib.add_map_stage("dos-nep-Deva-Latn-1997", "main", _stage_main)
_PTREE_3275275814051667310 = {2307:{None:"h"}}
