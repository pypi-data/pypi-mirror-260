import interscript
import regex as re
interscript.load_map("odni-fas-Arab-Latn-2004")
interscript.stdlib.define_map("odni-prs-Arab-Latn-2004")
def _stage_main(s):
    s = interscript.stdlib.parallel_regexp_gsub(s, *_PRE_1579500474754569277)
    s = interscript.transliterate("odni-fas-Arab-Latn-2004", s, "main")
    return s

interscript.stdlib.add_map_stage("odni-prs-Arab-Latn-2004", "main", _stage_main)
_PRE_1579500474754569277 = ["(?P<_0>اي"+interscript.stdlib.aliases["boundary"]+")|(?P<_1>ای"+interscript.stdlib.aliases["boundary"]+")|(?P<_2>قّ)|(?P<_3>وّ)|(?P<_4>يي)|(?P<_5>یی)|(?P<_6>ُو)|(?P<_7>ئ)|(?P<_8>ؤ)|(?P<_9>ء)|(?P<_10>ع)|(?P<_11>ق)|(?P<_12>و)", ["i","i","qq","ww","i","i","u","","","","","q","w"]]
