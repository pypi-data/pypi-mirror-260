import interscript
import regex as re
interscript.stdlib.define_map("sasm-mon-Mong-Latn-general-1978")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3199683409319171947)
    return s

interscript.stdlib.add_map_stage("sasm-mon-Mong-Latn-general-1978", "main", _stage_main)
_PTREE_3199683409319171947 = {6176:{None:"a"},6186:{None:"b"},6204:{None:"c"},6195:{None:"d"},6177:{None:"e"},6201:{None:"f"},6189:{None:"g"},6188:{None:"h"},6206:{None:"h"},6178:{None:"i"},6197:{None:"j"},6202:{None:"k"},6191:{None:"l"},6190:{None:"m"},6184:{None:"n"},6181:{None:"o"},6187:{None:"p"},6196:{None:"q"},6199:{None:"r"},6192:{None:"s"},6194:{None:"t"},6182:{None:"u"},6200:{None:"w"},6193:{None:"x"},6198:{None:"y"},6205:{None:"z"},6179:{None:"o"},6180:{None:"u"},6183:{None:"e"},6185:{None:"ng"},6158:{None:"-"},8239:{None:"-"}}
