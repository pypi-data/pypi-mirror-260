import interscript
import regex as re
interscript.stdlib.define_map("masm-mon-Latn-Cyrl-5217-2012")
def _stage_main(s):
    s = re.compile("ii", re.MULTILINE).sub("ий", s)
    s = re.compile("Ii", re.MULTILINE).sub("Ий", s)
    s = re.compile("ai", re.MULTILINE).sub("ай", s)
    s = re.compile("Ai", re.MULTILINE).sub("Ай", s)
    s = re.compile("ei", re.MULTILINE).sub("эй", s)
    s = re.compile("Ei", re.MULTILINE).sub("Эй", s)
    s = re.compile("oi", re.MULTILINE).sub("ой", s)
    s = re.compile("Oi", re.MULTILINE).sub("Ой", s)
    s = re.compile("üi", re.MULTILINE).sub("үй", s)
    s = re.compile("Üi", re.MULTILINE).sub("Үй", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2588710492218605820)
    return s

interscript.stdlib.add_map_stage("masm-mon-Latn-Cyrl-5217-2012", "main", _stage_main)
_PTREE_2588710492218605820 = {65:{None:"А"},66:{None:"Б"},86:{None:"В"},71:{None:"Г"},68:{None:"Д"},89:{101:{None:"Е"},111:{None:"Ё"},None:"Ы",117:{None:"Ю"},97:{None:"Я"}},74:{None:"Ж"},90:{None:"З"},73:{None:"И"},75:{None:"К",104:{None:"Х"}},76:{None:"Л"},77:{None:"М"},78:{None:"Н"},79:{None:"О"},214:{None:"Ө"},80:{None:"П"},82:{None:"Р"},83:{None:"С",104:{None:"Ш"}},84:{None:"Т",115:{None:"Ц"}},85:{None:"У"},220:{None:"Ү"},70:{None:"Ф"},67:{104:{None:"Ч"}},69:{None:"Э"},97:{None:"а"},98:{None:"б"},118:{None:"в"},103:{None:"г"},100:{None:"д"},121:{101:{None:"е"},111:{None:"ё"},None:"ы",117:{None:"ю"},97:{None:"я"}},106:{None:"ж"},122:{None:"з"},105:{None:"и"},107:{None:"к",104:{None:"х"}},108:{None:"л"},109:{None:"м"},110:{None:"н"},111:{None:"о"},246:{None:"ө"},112:{None:"п"},114:{None:"р"},115:{None:"с",104:{None:"ш"}},116:{None:"т",115:{None:"ц"}},117:{None:"у"},252:{None:"ү"},102:{None:"ф"},99:{104:{None:"ч"}},101:{None:"э"}}
