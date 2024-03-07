import interscript
import regex as re
interscript.load_map("mv-div-Thaa-Latn-1987")
interscript.stdlib.define_map("bgnpcgn-div-Thaa-Latn-1988")
def _stage_main(s):
    s = interscript.transliterate("mv-div-Thaa-Latn-1987", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3844072565385466955)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-div-Thaa-Latn-1988", "main", _stage_main)
_PTREE_3844072565385466955 = {1944:{None:"th’"},1945:{None:"h’"},1946:{None:"kh"},1947:{None:"dh’"},1948:{None:"x"},1949:{None:"sh’"},1950:{None:"s’"},1951:{None:"l’"},1952:{None:"t’"},1953:{None:"z’"},1954:{None:"’"},1955:{None:"gh"},1956:{None:"q"},1957:{None:"w"}}
