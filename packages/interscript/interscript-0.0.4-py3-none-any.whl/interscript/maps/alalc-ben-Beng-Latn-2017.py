import interscript
import regex as re
interscript.load_map("un-ben-Beng-Latn-2016")
interscript.stdlib.define_map("alalc-ben-Beng-Latn-2017")
def _stage_main(s):
    s = interscript.transliterate("un-ben-Beng-Latn-2016", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1635467436814373435)
    return s

interscript.stdlib.add_map_stage("alalc-ben-Beng-Latn-2017", "main", _stage_main)
_PTREE_1635467436814373435 = {2437:{None:"a"},2528:{None:"ṝ"},2438:{None:"ā"},2444:{None:"ḹ"},2439:{None:"I"},2447:{None:"e"},2440:{None:"ī"},2448:{None:"ai"},2441:{None:"u"},2451:{None:"o"},2442:{None:"ū"},2452:{None:"au"},2443:{None:"ṛ"},2453:{None:"ka"},2454:{None:"kha"},2455:{None:"ga"},2456:{None:"gha"},2457:{None:"ṅa"},2458:{None:"ca"},2459:{None:"cha"},2460:{None:"ja"},2461:{None:"jha"},2462:{None:"ña"},2463:{None:"ṭa"},2464:{None:"ṭha"},2465:{None:"ḍa",2492:{None:"ṛa"}},2466:{None:"ḍha",2492:{None:"ṛha"}},2467:{None:"ṇa"},2468:{None:"ta"},2510:{None:"t"},2469:{None:"tha"},2470:{None:"da"},2471:{None:"dha"},2472:{None:"na"},2474:{None:"pa"},2475:{None:"pha"},2476:{None:"ba"},2477:{None:"bha"},2478:{None:"ma"},2479:{None:"ya",2492:{None:"ẏa"}},2480:{None:"ra"},2482:{None:"la"},2486:{None:"śa"},2487:{None:"sha"},2488:{None:"sa"},2489:{None:"ha"},32:{2434:{None:"ṃ"},2435:{None:"ḥ"}},2433:{None:"n̐"},2365:{None:"’"}}
