import interscript
import regex as re
interscript.load_map("bgnpcgn-prs-Arab-Latn-2007")
interscript.stdlib.define_map("bgnpcgn-pus-Arab-Latn-1968")
def _stage_main(s):
    s = interscript.transliterate("bgnpcgn-prs-Arab-Latn-2007", s, "main")
    s = interscript.stdlib.parallel_regexp_gsub(s, *_PRE_4078874602888190925)
    s = re.compile("(?<="+interscript.stdlib.aliases["boundary"]+")(?<!"+interscript.stdlib.aliases["boundary"]+"[‘’'\\-])[a-￿]", re.MULTILINE).sub(interscript.stdlib.upper, s)
    s = re.compile("\\ Ut\\ T", re.MULTILINE).sub(" ut T", s)
    s = re.compile("\\ Us̄\\ S̄", re.MULTILINE).sub(" us̄ S̄", s)
    s = re.compile("\\ Ud\\ D", re.MULTILINE).sub(" ud D", s)
    s = re.compile("\\ Uz̄\\ Z̄", re.MULTILINE).sub(" uz̄ Z̄", s)
    s = re.compile("\\ Ur\\ R", re.MULTILINE).sub(" ur R", s)
    s = re.compile("\\ Uz\\ Z", re.MULTILINE).sub(" uz Z", s)
    s = re.compile("\\ Us\\ S", re.MULTILINE).sub(" us S", s)
    s = re.compile("\\ As\\ S", re.MULTILINE).sub(" us S", s)
    s = re.compile("\\ Ush\\ Sh", re.MULTILINE).sub(" ush Sh", s)
    s = re.compile("\\ Uş\\ Ş", re.MULTILINE).sub(" uş Ş", s)
    s = re.compile("\\ Uẕ\\ Ẕ", re.MULTILINE).sub(" uẕ Ẕ", s)
    s = re.compile("\\ Uţ\\ Ţ", re.MULTILINE).sub(" uţ Ţ", s)
    s = re.compile("\\ Uz̧\\ Z̧", re.MULTILINE).sub(" uz̧ Z̧", s)
    s = re.compile("\\ Ul\\ L", re.MULTILINE).sub(" ul L", s)
    s = re.compile("\\ Un\\ n", re.MULTILINE).sub(" un N", s)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bgnpcgn-pus-Arab-Latn-1968", "main", _stage_main)
_PRE_4078874602888190925 = ["(?P<_0>"+interscript.stdlib.aliases["space"]+"اللَّه)|(?P<_1>"+interscript.stdlib.aliases["space"]+"شَهر)|(?P<_2>"+interscript.stdlib.aliases["space"]+"زادة)|(?P<_3>"+interscript.stdlib.aliases["boundary"]+"التّ?)|(?P<_4>"+interscript.stdlib.aliases["boundary"]+"الثّ?)|(?P<_5>"+interscript.stdlib.aliases["boundary"]+"الدّ?)|(?P<_6>"+interscript.stdlib.aliases["boundary"]+"الذّ?)|(?P<_7>"+interscript.stdlib.aliases["boundary"]+"الرّ?)|(?P<_8>"+interscript.stdlib.aliases["boundary"]+"الزّ?)|(?P<_9>"+interscript.stdlib.aliases["boundary"]+"السّ?)|(?P<_10>"+interscript.stdlib.aliases["boundary"]+"الشّ?)|(?P<_11>"+interscript.stdlib.aliases["boundary"]+"الصّ?)|(?P<_12>"+interscript.stdlib.aliases["boundary"]+"الضّ?)|(?P<_13>"+interscript.stdlib.aliases["boundary"]+"الطّ?)|(?P<_14>"+interscript.stdlib.aliases["boundary"]+"الظّ?)|(?P<_15>"+interscript.stdlib.aliases["boundary"]+"اللّ?)|(?P<_16>"+interscript.stdlib.aliases["boundary"]+"النّ?)|(?P<_17>"+interscript.stdlib.aliases["space"]+"خوا)|(?P<_18>"+interscript.stdlib.aliases["space"]+"زَي)|(?P<_19>ِ"+interscript.stdlib.aliases["boundary"]+")|(?P<_20>ِ)|(?P<_21>ُ)|(?P<_22>ْ)|(?P<_23>ٙ)|(?P<_24>ئ)", ["ullāh","shahr","zādah","ut t","us̄ s̄","ud d","uz̄ z̄","ur r","uz z","us s","ush sh","uş ş","uẕ ẕ","uţ ţ","uz̧ z̧","ul l","un n","khwā","zay","-e","i","u","","ê","êy"]]
