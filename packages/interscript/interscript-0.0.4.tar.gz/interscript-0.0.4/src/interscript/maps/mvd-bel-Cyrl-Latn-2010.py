import interscript
import regex as re
interscript.load_map("mvd-bel-Cyrl-Latn-2008")
interscript.stdlib.define_map("mvd-bel-Cyrl-Latn-2010")
def _stage_main(s):
    s = re.compile("(?<=[ЕеЁёЫыЮюЯя])Й"+interscript.stdlib.aliases["line_end"]+"", re.MULTILINE).sub("", s)
    s = re.compile("(?<=[ЕеЁёЫыЮюЯя])й"+interscript.stdlib.aliases["line_end"]+"", re.MULTILINE).sub("", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_723840024589650447)
    s = interscript.transliterate("mvd-bel-Cyrl-Latn-2008", s, "main")
    return s

interscript.stdlib.add_map_stage("mvd-bel-Cyrl-Latn-2010", "main", _stage_main)
_PTREE_723840024589650447 = {1043:{None:"H"},1075:{None:"h"},1068:{None:""},1100:{None:""}}
