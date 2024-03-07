import interscript
import regex as re
interscript.load_map("posix")
interscript.stdlib.define_map("bgnpcgn-deu-Latn-Latn-2000")
def _stage_main(s):
    s = re.compile("β("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("SS"+"\\1", s)
    s = re.compile("Ä("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("AE"+"\\1", s)
    s = re.compile("Ö("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("OE"+"\\1", s)
    s = re.compile("Ü("+interscript.stdlib.get_alias_re("posix", "upper")+")", re.MULTILINE).sub("UE"+"\\1", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1442259840949177577)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-deu-Latn-Latn-2000", "main", _stage_main)
_PTREE_1442259840949177577 = {196:{None:"Ae"},214:{None:"Oe"},220:{None:"Ue"},228:{None:"ae"},246:{None:"oe"},252:{None:"ue"},946:{None:"ss"}}
