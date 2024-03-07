import interscript
import regex as re
interscript.stdlib.define_map("var-mon-Mong-Latn-1930")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_192718151970070456)
    return s

interscript.stdlib.add_map_stage("var-mon-Mong-Latn-1930", "main", _stage_main)
_PTREE_192718151970070456 = {6176:{None:"a"},6177:{None:"e"},6178:{None:"i"},6179:{None:"o"},6180:{None:"u"},6181:{None:"ө"},6182:{None:"y"},6184:{None:"n"},6190:{None:"m"},6191:{None:"l"},6186:{None:"b"},6187:{None:"p"},6201:{None:"f"},6203:{None:"k"},6188:{None:"k"},6189:{None:"g"},6192:{None:"s"},6193:{None:"ş"},6194:{None:"t"},6195:{None:"d"},6196:{None:"ç"},6197:{None:"ƶ"},6198:{None:"j"},6199:{None:"r"},6206:{None:"h"},6145:{None:"..."},6146:{None:","},6147:{None:"."},6158:{None:"-"},8239:{None:"-"}}
