import interscript
import regex as re
interscript.load_map("gost-rus-Cyrl-Latn-16876-71-1983")
interscript.stdlib.define_map("un-rus-Cyrl-Latn-1987")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2345769265814317941)
    s = interscript.transliterate("gost-rus-Cyrl-Latn-16876-71-1983", s, "main")
    return s

interscript.stdlib.add_map_stage("un-rus-Cyrl-Latn-1987", "main", _stage_main)
_PTREE_2345769265814317941 = {1066:{None:"”"},1068:{None:"’"},1098:{None:"”"},1100:{None:"’"},1070:{None:"Ju"},1102:{None:"ju"},1071:{None:"Ja"},1103:{None:"ja"}}
