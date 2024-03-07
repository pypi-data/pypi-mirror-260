import interscript
import regex as re
interscript.load_map("din-san-Deva-Latn-33904-2018")
interscript.stdlib.define_map("din-hin-Deva-Latn-33904-2018")
def _stage_main(s):
    s = interscript.transliterate("din-san-Deva-Latn-33904-2018", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3759309453348748740)
    return s

interscript.stdlib.add_map_stage("din-hin-Deva-Latn-33904-2018", "main", _stage_main)
_PTREE_3759309453348748740 = {2418:{None:"ê"},2321:{None:"ô"},2325:{2364:{None:"ḵa",2381:{None:"ḵ"}}},2326:{2364:{None:"ḵha",2381:{None:"ḵh"}}},2327:{2364:{None:"g̲a",2381:{None:"g̲"}}},2332:{2364:{None:"j̲a",2381:{None:"j̲"}}},2337:{2364:{None:"ṙa",2381:{None:"ṙ"}}},2338:{2364:{None:"ṙha",2381:{None:"ṙh"}}},2347:{2364:{None:"p̲ha",2381:{None:"p̲h"}}},2360:{2364:{None:"s̲a",2381:{None:"s̲"}}},2361:{2364:{None:"h̲a",2381:{None:"h̲"}}}}
