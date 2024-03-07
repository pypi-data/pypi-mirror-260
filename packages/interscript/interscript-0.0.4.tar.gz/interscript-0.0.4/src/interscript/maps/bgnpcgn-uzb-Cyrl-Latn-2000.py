import interscript
import regex as re
interscript.load_map("bgnpcgn-uzb-Cyrl-Latn-1979")
interscript.stdlib.define_map("bgnpcgn-uzb-Cyrl-Latn-2000")
def _stage_main(s):
    s = re.compile("(?<=[АаЕеЁёИиОоУуЭэЮюЯяЙйЬь])Е", re.MULTILINE).sub("Ye", s)
    s = re.compile("(?<=[АаЕеЁёИиОоУуЭэЮюЯяЙйЬь])е", re.MULTILINE).sub("ye", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2798858337519701047)
    s = interscript.transliterate("bgnpcgn-uzb-Cyrl-Latn-1979", s, "main")
    return s

interscript.stdlib.add_map_stage("bgnpcgn-uzb-Cyrl-Latn-2000", "main", _stage_main)
_PTREE_2798858337519701047 = {1042:{None:"V"},1170:{None:"G‘"},1046:{None:"J"},1038:{None:"O‘"},1061:{None:"X"},1066:{None:"’"},1068:{None:"’"},1074:{None:"w"},1171:{None:"g‘"},1078:{None:"j"},1118:{None:"o‘"},1093:{None:"x"},1098:{None:"’"},1100:{None:"’"}}
