import interscript
import regex as re
interscript.load_map("var-jpn-Hrkt-Latn-hepburn-1954")
interscript.stdlib.define_map("bgnpcgn-jpn-Hrkt-Latn-1976")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1450046899098863745)
    s = interscript.transliterate("var-jpn-Hrkt-Latn-hepburn-1954", s, "main")
    s = interscript.functions.title_case(s, {})
    return s

interscript.stdlib.add_map_stage("bgnpcgn-jpn-Hrkt-Latn-1976", "main", _stage_main)
_PTREE_1450046899098863745 = {12367:{12353:{None:"kwa"},12355:{None:"kwi"},12359:{None:"kwe"},12361:{None:"kwo"}},12463:{12449:{None:"kwa"},12451:{None:"kwi"},12455:{None:"kwe"},12457:{None:"kwo"}},12368:{12353:{None:"gwa"},12355:{None:"gwa"},12359:{None:"gwe"},12361:{None:"gwo"}},12464:{12449:{None:"gwa"},12451:{None:"gwa"},12455:{None:"gwe"},12457:{None:"gwo"}},12365:{12359:{None:"kye"}},12461:{12455:{None:"kye"}},12366:{12359:{None:"gye"}},12462:{12455:{None:"gye"}},12375:{12359:{None:"she"}},12471:{12455:{None:"she"}},12376:{12359:{None:"je"}},12472:{12455:{None:"je"}},12388:{12353:{None:"tsa"},12359:{None:"tse"},12361:{None:"tso"}},12484:{12449:{None:"tsa"},12455:{None:"tse"},12457:{None:"tso"}},12390:{12355:{None:"ti"},12421:{None:"tyu"}},12486:{12451:{None:"ti"},12517:{None:"tyu"}},12391:{12355:{None:"di"},12421:{None:"dyu"}},12487:{12451:{None:"di"},12517:{None:"dyu"}},12392:{12421:{None:"tu"}},12488:{12517:{None:"tu"}},12393:{12421:{None:"du"}},12489:{12517:{None:"du"}},12385:{12359:{None:"che"}},12481:{12455:{None:"che"}},12386:{12359:{None:"je"}},12482:{12455:{None:"je"}},12395:{12359:{None:"nye"}},12491:{12455:{None:"nye"}},12405:{12353:{None:"fa"},12355:{None:"fi"},12359:{None:"fe"},12361:{None:"fo"}},12501:{12449:{None:"fa"},12451:{None:"fi"},12455:{None:"fe"},12457:{None:"fo"}},12415:{12359:{None:"mye"}},12511:{12455:{None:"mye"}},12355:{12359:{None:"ye"}},12451:{12455:{None:"ye"}},12426:{12359:{None:"rye"}},12522:{12455:{None:"rye"}},12436:{12353:{None:"va"},12355:{None:"vi"},12359:{None:"ve"},12361:{None:"vo"},None:"vu"},12532:{12449:{None:"va"},12451:{None:"vi"},12455:{None:"ve"},12457:{None:"vo"},None:"vu"},12358:{12355:{None:"wi"},12359:{None:"we"},12361:{None:"wo"}},12454:{12451:{None:"wi"},12455:{None:"we"},12457:{None:"wo"}}}
