import interscript
import regex as re
interscript.load_map("ua-ukr-Cyrl-Latn-1996")
interscript.stdlib.define_map("ua-ukr-Cyrl-Latn-2010")
def _stage_main(s):
    s = re.compile("'", re.MULTILINE).sub("", s)
    s = re.compile("’", re.MULTILINE).sub("", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2372934404654436008)
    s = interscript.transliterate("ua-ukr-Cyrl-Latn-1996", s, "main")
    return s

interscript.stdlib.add_map_stage("ua-ukr-Cyrl-Latn-2010", "main", _stage_main)
_PTREE_2372934404654436008 = {1168:{None:"G"},1169:{None:"g"},1065:{None:"Shch"},1097:{None:"shch"},1100:{None:""},1068:{None:""},39:{None:""},8217:{None:""}}
