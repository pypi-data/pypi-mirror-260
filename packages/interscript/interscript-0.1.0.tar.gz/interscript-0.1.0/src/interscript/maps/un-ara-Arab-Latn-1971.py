import interscript
import regex as re
interscript.load_map("un-ara-Arab-Latn-2017")
interscript.stdlib.define_map("un-ara-Arab-Latn-1971")
def _stage_main(s):
    s = interscript.stdlib.parallel_regexp_gsub(s, *_PRE_484464764295304069)
    s = interscript.transliterate("un-ara-Arab-Latn-2017", s, "main")
    s = re.compile("\\ At͟h\\ T͟h", re.MULTILINE).sub(" at͟h T͟h", s)
    s = re.compile("\\ Ad͟h\\ D͟h", re.MULTILINE).sub(" ad͟h D͟h", s)
    s = re.compile("\\ As͟h\\ S͟h", re.MULTILINE).sub(" as͟h S͟h", s)
    s = re.compile("\\ Az͟h\\ Z͟h", re.MULTILINE).sub(" az͟h Z͟h", s)
    return s

interscript.stdlib.add_map_stage("un-ara-Arab-Latn-1971", "main", _stage_main)
_PRE_484464764295304069 = ["(?P<_0>"+interscript.stdlib.aliases["boundary"]+"الثّ?)|(?P<_1>"+interscript.stdlib.aliases["boundary"]+"الذّ?)|(?P<_2>"+interscript.stdlib.aliases["boundary"]+"الشّ?)|(?P<_3>"+interscript.stdlib.aliases["boundary"]+"الظّ?)|(?P<_4>خّ)|(?P<_5>ذّ)|(?P<_6>شّ)|(?P<_7>ظّ)|(?P<_8>غّ)|(?P<_9>ث)|(?P<_10>ﺛ)|(?P<_11>ﺜ)|(?P<_12>ﺚ)|(?P<_13>خ)|(?P<_14>ﺧ)|(?P<_15>ﺨ)|(?P<_16>ﺦ)|(?P<_17>غ)|(?P<_18>ﻏ)|(?P<_19>ﻐ)|(?P<_20>ﻎ)|(?P<_21>ذ)|(?P<_22>ﺬ)|(?P<_23>ش)|(?P<_24>ﺷ)|(?P<_25>ﺸ)|(?P<_26>ﺶ)|(?P<_27>ظ)|(?P<_28>ﻇ)|(?P<_29>ﻈ)|(?P<_30>ﻆ)", ["at͟h t͟h","ad͟h d͟h","as͟h s͟h","az͟h z͟h","k͟hk͟h","d͟hd͟h","s͟h","z͟hz͟h","g͟hg͟h","t͟h","t͟h","t͟h","t͟h","k͟h","k͟h","k͟h","k͟h","g͟h","g͟h","g͟h","g͟h","d͟h","d͟h","s͟h","s͟h","s͟h","s͟h","z͟h","z͟h","z͟h","z͟h"]]
