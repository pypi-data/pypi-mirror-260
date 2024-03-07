import interscript
import regex as re
interscript.load_map("odni-fas-Arab-Latn-2015")
interscript.stdlib.define_map("odni-prs-Arab-Latn-2015")
def _stage_main(s):
    s = interscript.stdlib.parallel_regexp_gsub(s, *_PRE_427215755699347617)
    s = interscript.transliterate("odni-fas-Arab-Latn-2015", s, "main")
    return s

interscript.stdlib.add_map_stage("odni-prs-Arab-Latn-2015", "main", _stage_main)
_PRE_427215755699347617 = ["(?P<_0>اي"+interscript.stdlib.aliases["boundary"]+")|(?P<_1>ای"+interscript.stdlib.aliases["boundary"]+")|(?P<_2>قّ)|(?P<_3>وّ)|(?P<_4>يي)|(?P<_5>یی)|(?P<_6>ُو)|(?P<_7>ة)|(?P<_8>ئ)|(?P<_9>ؤ)|(?P<_10>ء)|(?P<_11>ع)|(?P<_12>ق)|(?P<_13>و)", ["i","i","qq","ww","i","i","u","ah","","","","","q","w"]]
