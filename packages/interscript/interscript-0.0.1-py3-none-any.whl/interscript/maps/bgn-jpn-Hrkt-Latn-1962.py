import interscript
import regex as re
interscript.load_map("var-jpn-Hrkt-Latn-hepburn-1954")
interscript.stdlib.define_map("bgn-jpn-Hrkt-Latn-1962")
def _stage_main(s):
    s = re.compile("[んン](?=[ばびぶべぼまみむめもぱぴぷぺぽバビブベボマミムメモパピプペポ])", re.MULTILINE).sub("m", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4357942692901107933)
    s = interscript.transliterate("var-jpn-Hrkt-Latn-hepburn-1954", s, "main")
    return s

interscript.stdlib.add_map_stage("bgn-jpn-Hrkt-Latn-1962", "main", _stage_main)
_PTREE_4357942692901107933 = {12369:{None:"ke"},12465:{None:"ke"},12534:{None:"ga"},12399:{None:"ha"},12402:{None:"hi"},12405:{None:"fu"},12408:{None:"he"},12411:{None:"ho"},12495:{None:"ha"},12498:{None:"hi"},12501:{None:"fu"},12504:{None:"he"},12507:{None:"ho"},12432:{None:"i"},12433:{None:"e"},12528:{None:"i"},12529:{None:"e"},12367:{12431:{None:"ka",12358:{None:"kō"}}},12368:{12431:{None:"ga",12358:{None:"gō"}}},12463:{12527:{None:"ka",12454:{None:"kō"}}},12464:{12527:{None:"ga",12454:{None:"gō"}}}}
