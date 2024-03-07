import interscript
import regex as re
interscript.load_map("var-kor")
interscript.load_map("var-kor-Hang-Hang-jamo")
interscript.stdlib.define_map("iso-kor-Hang-Latn-1996-method2")
def _stage_main(s):
    s = interscript.transliterate("var-kor-Hang-Hang-jamo", s, "main")
    s = re.compile("(?<!"+interscript.stdlib.get_alias_re("var-kor", "jamo")+")ᄋ", re.MULTILINE).sub("", s)
    s = re.compile("ᄋ", re.MULTILINE).sub("'", s)
    s = re.compile("ᆼ", re.MULTILINE).sub("ng", s)
    s = re.compile("(?<="+interscript.stdlib.get_alias_re("var-kor", "jamo")+")"+interscript.stdlib.aliases["none"]+"(?="+interscript.stdlib.get_alias_re("var-kor", "double_cons_jamo")+")", re.MULTILINE).sub("'", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3695565539050243121)
    return s

interscript.stdlib.add_map_stage("iso-kor-Hang-Latn-1996-method2", "main", _stage_main)
_PTREE_3695565539050243121 = {4352:{None:"g"},4520:{None:"g"},4367:{None:"k"},4543:{None:"k"},4353:{None:"gg"},4521:{None:"gg"},4355:{None:"d"},4526:{None:"d"},4368:{None:"t"},4544:{None:"t"},4356:{None:"dd"},55245:{None:"dd"},4359:{None:"b"},4536:{None:"b"},4369:{None:"p"},4545:{None:"p"},4360:{None:"bb"},55270:{None:"bb"},4364:{None:"j"},4541:{None:"j"},4366:{None:"c"},4542:{None:"c"},4365:{None:"jj"},55289:{None:"jj"},4522:{None:"gs"},43364:{None:"rg"},4528:{None:"lg"},4532:{None:"lt"},43369:{None:"rb"},4530:{None:"lb"},4533:{None:"lp"},4444:{None:"nj"},4524:{None:"nj"},4385:{None:"bs"},4537:{None:"bs"},4361:{None:"s"},4538:{None:"s"},4362:{None:"ss"},4539:{None:"ss"},4370:{None:"h"},4546:{None:"h"},4354:{None:"n"},4523:{None:"n"},4357:{None:"r"},4527:{None:"l"},4358:{None:"m"},4535:{None:"m"},43372:{None:"rs"},4531:{None:"ls"},43368:{None:"rm"},4529:{None:"lm"},4378:{None:"rh"},4534:{None:"lh"},4445:{None:"nh"},4525:{None:"nh"},4449:{None:"a"},4453:{None:"eo"},4457:{None:"o"},4462:{None:"u"},4467:{None:"eu"},4469:{None:"i"},4450:{None:"ae"},4454:{None:"e"},4460:{None:"oe"},4451:{None:"ya"},4455:{None:"yeo"},4461:{None:"yo"},4466:{None:"yu"},4452:{None:"yae"},4456:{None:"ye"},4458:{None:"wa"},4463:{None:"weo"},4465:{None:"wi"},4459:{None:"wae"},4464:{None:"we"},4468:{None:"yi"}}
