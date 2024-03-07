import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-isl-Latn-Latn-1964")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2547447285593695275)
    s = re.compile("(?<=[A-Z])(?:Th|Dh)", re.MULTILINE).sub(interscript.stdlib.upper, s)
    s = re.compile("(?:Th|Dh)(?=[A-Z])", re.MULTILINE).sub(interscript.stdlib.upper, s)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-isl-Latn-Latn-1964", "main", _stage_main)
_PTREE_2547447285593695275 = {208:{None:"Dh"},240:{None:"dh"},222:{None:"Th"},254:{None:"th"}}
