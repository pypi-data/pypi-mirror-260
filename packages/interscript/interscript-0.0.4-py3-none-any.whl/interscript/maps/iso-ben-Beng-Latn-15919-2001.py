import interscript
import regex as re
interscript.stdlib.define_map("iso-ben-Beng-Latn-15919-2001")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_325318916615415300)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("iso-ben-Beng-Latn-15919-2001", "main", _stage_main)
_PTREE_325318916615415300 = {2437:{None:"a"},2438:{None:"ā"},2439:{None:"i"},2440:{None:"ī"},2441:{None:"u"},2442:{None:"ū"},2443:{None:"ṛ"},2528:{None:"ṝ"},2444:{None:"ḻ"},2529:{None:"ḹ"},2447:{None:"e"},2448:{None:"ai"},2451:{None:"o"},2452:{None:"au"},2494:{None:"ā"},2495:{None:"i"},2496:{None:"ī"},2497:{None:"u"},2498:{None:"ū"},2499:{None:"ṛ"},2500:{None:"ṝ"},2530:{None:"ḻ"},2531:{None:"ḹ"},2503:{None:"e"},2504:{None:"ai"},2507:{None:"o"},2508:{None:"au"},2434:{None:"ṁ"},2433:{None:"m̐"},2435:{None:"ḥ"},2453:{None:"ka"},2454:{None:"kha"},2455:{None:"ga"},2456:{None:"gha"},2457:{None:"ṅa"},2458:{None:"ca"},2459:{None:"cha"},2460:{None:"ja"},2461:{None:"jha"},2462:{None:"ña"},2463:{None:"ṭa"},2464:{None:"ṭha"},2465:{None:"ḍa"},2466:{None:"ḍha"},2467:{None:"ṇa"},2468:{None:"ta"},2469:{None:"tha"},2470:{None:"da"},2471:{None:"dha"},2472:{None:"na"},2474:{None:"pa"},2475:{None:"pha"},2476:{None:"ba",2433:{None:"m̐va"}},2477:{None:"bha"},2478:{None:"ma"},2479:{None:"ya",2433:{None:"m̐ya"}},2480:{None:"ra",2433:{None:"m̐ra"}},2482:{None:"la",2433:{None:"m̐la"}},2486:{None:"śa"},2487:{None:"ṣa"},2488:{None:"sa"},2489:{None:"ha"},2524:{None:"ṙa"},2525:{None:"ṙha"},2527:{None:"ẏa"},2510:{None:"t"},2509:{None:""},2535:{None:"1"},2536:{None:"2"},2537:{None:"3"},2538:{None:"4"},2539:{None:"5"},2540:{None:"6"},2541:{None:"7"},2542:{None:"8"},2543:{None:"9"},2534:{None:"0"}}
