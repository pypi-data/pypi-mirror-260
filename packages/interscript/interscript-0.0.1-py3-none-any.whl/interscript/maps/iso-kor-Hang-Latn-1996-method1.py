import interscript
import regex as re
interscript.load_map("var-kor")
interscript.load_map("var-kor-Hang-Hang-jamo")
interscript.stdlib.define_map("iso-kor-Hang-Latn-1996-method1")
def _stage_main(s):
    s = interscript.transliterate("var-kor-Hang-Hang-jamo", s, "main")
    s = re.compile("(?<!"+interscript.stdlib.get_alias_re("var-kor", "jamo")+")ᄋ", re.MULTILINE).sub("", s)
    s = re.compile("ᄋ", re.MULTILINE).sub("'", s)
    s = re.compile("ᆼ", re.MULTILINE).sub("ng", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-kor", "jamo")+")"+interscript.stdlib.aliases["none"]+"(?="+interscript.stdlib.get_alias_re("var-kor", "double_cons_jamo")+")", re.MULTILINE).sub("'", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-kor", "jamo")+")"+interscript.stdlib.aliases["none"]+"(?="+interscript.stdlib.get_alias_re("var-kor", "aspirated_cons_jamo")+")", re.MULTILINE).sub("'", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2409707295534499398)
    return s

interscript.stdlib.add_map_stage("iso-kor-Hang-Latn-1996-method1", "main", _stage_main)
_PTREE_2409707295534499398 = {4352:{None:"k"},4520:{None:"k"},4367:{None:"kh"},4543:{None:"kh"},4353:{None:"kk"},4521:{None:"kk"},4355:{None:"t"},4526:{None:"t"},4368:{None:"th"},4544:{None:"th"},4356:{None:"tt"},55245:{None:"tt"},4359:{None:"p"},4536:{None:"p"},4369:{None:"ph"},4545:{None:"ph"},4360:{None:"pp"},55270:{None:"pp"},4364:{None:"c"},4541:{None:"c"},4366:{None:"ch"},4542:{None:"ch"},4365:{None:"cc"},55289:{None:"cc"},4522:{None:"ks"},43364:{None:"rk"},4528:{None:"lk"},4532:{None:"lth"},43369:{None:"rp"},4530:{None:"lp"},4533:{None:"lph"},4444:{None:"nc"},4524:{None:"nc"},4385:{None:"ps"},4537:{None:"ps"},4361:{None:"s"},4538:{None:"s"},4362:{None:"ss"},4539:{None:"ss"},4370:{None:"h"},4546:{None:"h"},4354:{None:"n"},4523:{None:"n"},4357:{None:"r"},4527:{None:"l"},4358:{None:"m"},4535:{None:"m"},43372:{None:"rs"},4531:{None:"ls"},43368:{None:"rm"},4529:{None:"lm"},4378:{None:"rh"},4534:{None:"lh"},4445:{None:"nh"},4525:{None:"nh"},4449:{None:"a"},4453:{None:"eo"},4457:{None:"o"},4462:{None:"u"},4467:{None:"eu"},4469:{None:"i"},4450:{None:"ae"},4454:{None:"e"},4460:{None:"oe"},4451:{None:"ya"},4455:{None:"yeo"},4461:{None:"yo"},4466:{None:"yu"},4452:{None:"yae"},4456:{None:"ye"},4458:{None:"wa"},4463:{None:"weo"},4465:{None:"wi"},4459:{None:"wae"},4464:{None:"we"},4468:{None:"yi"}}
