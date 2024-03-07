import interscript
import regex as re
interscript.load_map("az-aze-Cyrl-Latn-1939")
interscript.stdlib.define_map("az-aze-Cyrl-Latn-1958")
def _stage_main(s):
    s = re.compile("Й", re.MULTILINE).sub("J", s)
    s = re.compile("й", re.MULTILINE).sub("j", s)
    s = interscript.transliterate("az-aze-Cyrl-Latn-1939", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_756874305767594672)
    return s

interscript.stdlib.add_map_stage("az-aze-Cyrl-Latn-1958", "main", _stage_main)
_PTREE_756874305767594672 = {1032:{None:"Y"},1049:{None:"J"},1062:{None:""},1069:{None:""},1070:{None:""},1071:{None:""},1112:{None:"y"},1081:{None:"j"},1094:{None:""},1101:{None:""},1102:{None:""},1103:{None:""}}
