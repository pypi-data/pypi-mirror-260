import interscript
import regex as re
interscript.stdlib.define_map("var-mon-Mong-Latn-lessing")
def _stage_main(s):
    s = re.compile("ᠬ(?=[ᠡᠢᠥᠦ])", re.MULTILINE).sub("k", s)
    s = re.compile("ᠭ(?=[ᠡᠢᠥᠦ])", re.MULTILINE).sub("g", s)
    s = re.compile("ᠠᠶᠢ", re.MULTILINE).sub("ai", s)
    s = re.compile("ᠡᠶᠢ", re.MULTILINE).sub("ei", s)
    s = re.compile("ᠣᠶᠢ", re.MULTILINE).sub("oi", s)
    s = re.compile("ᠤᠶᠢ", re.MULTILINE).sub("ui", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_57027324334165702)
    return s

interscript.stdlib.add_map_stage("var-mon-Mong-Latn-lessing", "main", _stage_main)
_PTREE_57027324334165702 = {6176:{None:"a"},6177:{None:"e"},6178:{None:"i"},6179:{None:"o"},6180:{None:"u"},6181:{None:"ø"},6182:{None:"y"},6184:{None:"n"},6185:{None:"ng"},6188:{None:"x"},6189:{None:"γ"},6186:{None:"b"},6187:{None:"p"},6201:{None:"f"},6192:{None:"s"},6193:{None:"š"},6194:{None:"t"},6195:{None:"d"},6191:{None:"l"},6190:{None:"m"},6196:{None:"c"},6197:{None:"z"},6198:{None:"j"},6202:{None:"k"},6199:{None:"r"},6200:{None:"v"},6206:{None:"h"},6145:{None:"..."},6146:{None:","},6147:{None:"."},6148:{None:":"},6158:{None:"-"},8239:{None:"-"}}
