import interscript
import regex as re
interscript.load_map("un-ara-Arab-Latn-2017")
interscript.stdlib.define_map("un-ara-Arab-Latn-1972")
def _stage_main(s):
    s = interscript.stdlib.parallel_regexp_gsub(s, *_PRE_3803399503150814000)
    s = interscript.transliterate("un-ara-Arab-Latn-2017", s, "main")
    s = re.compile("\\ Aş\\ Ş", re.MULTILINE).sub(" aş Ş", s)
    s = re.compile("\\ Aḑ\\ Ḑ", re.MULTILINE).sub(" aḑ Ḑ", s)
    s = re.compile("\\ Aţ\\ Ţ", re.MULTILINE).sub(" aţ Ţ", s)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("un-ara-Arab-Latn-1972", "main", _stage_main)
_PRE_3803399503150814000 = ["(?P<_0>"+interscript.stdlib.aliases["boundary"]+"الصّ?)|(?P<_1>"+interscript.stdlib.aliases["boundary"]+"الضّ?)|(?P<_2>"+interscript.stdlib.aliases["boundary"]+"الطّ?)|(?P<_3>حّ)|(?P<_4>صّ)|(?P<_5>ضّ)|(?P<_6>طّ)|(?P<_7>ظّ)|(?P<_8>ح)|(?P<_9>ﺣ)|(?P<_10>ﺤ)|(?P<_11>ﺢ)|(?P<_12>ص)|(?P<_13>ﺻ)|(?P<_14>ﺼ)|(?P<_15>ﺺ)|(?P<_16>ض)|(?P<_17>ﺿ)|(?P<_18>ﻀ)|(?P<_19>ﺾ)|(?P<_20>ط)|(?P<_21>ﻃ)|(?P<_22>ﻄ)|(?P<_23>ﻂ)|(?P<_24>ظ)|(?P<_25>ﻇ)|(?P<_26>ﻈ)|(?P<_27>ﻆ)", ["aş ş","aḑ ḑ","aţ ţ","ḩḩ","şş","ḑḑ","ţţ","z̧z̧","ḩ","ḩ","ḩ","ḩ","ş","ş","ş","ş","ḑ","ḑ","ḑ","ḑ","ţ","ţ","ţ","ţ","z̧","z̧","z̧","z̧"]]
