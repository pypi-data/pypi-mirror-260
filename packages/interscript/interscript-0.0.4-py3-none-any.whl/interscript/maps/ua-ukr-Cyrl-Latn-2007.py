import interscript
import regex as re
interscript.load_map("ua-ukr-Cyrl-Latn-1996")
interscript.stdlib.define_map("ua-ukr-Cyrl-Latn-2007")
def _stage_main(s):
    s = re.compile("'", re.MULTILINE).sub("", s)
    s = re.compile("’", re.MULTILINE).sub("", s)
    s = re.compile("(?<=[З])Г", re.MULTILINE).sub("GH", s)
    s = re.compile(""+interscript.stdlib.aliases["boundary"]+"Є", re.MULTILINE).sub("YE", s)
    s = re.compile(""+interscript.stdlib.aliases["boundary"]+"Ї", re.MULTILINE).sub("I", s)
    s = re.compile(""+interscript.stdlib.aliases["boundary"]+"Ю", re.MULTILINE).sub("YU", s)
    s = re.compile(""+interscript.stdlib.aliases["boundary"]+"Я", re.MULTILINE).sub("YA", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3380196949281173449)
    s = interscript.transliterate("ua-ukr-Cyrl-Latn-1996", s, "main")
    return s

interscript.stdlib.add_map_stage("ua-ukr-Cyrl-Latn-2007", "main", _stage_main)
_PTREE_3380196949281173449 = {1043:{None:"G"},1168:{None:"G"},1028:{None:"IE"},1046:{None:"ZH"},1061:{None:"KH"},1062:{None:"TS"},1063:{None:"CH"},1064:{None:"SH"},1065:{None:"SHCH"},1070:{None:"IU"},1071:{None:"IA"},1068:{None:""},1075:{None:"g"},1169:{None:"g"},1097:{None:"shch"},1102:{None:"iu"},1103:{None:"ia"},1100:{None:""},39:{None:""},8217:{None:""}}
