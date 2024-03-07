import interscript
import regex as re
interscript.stdlib.define_map("bis-ben-Beng-Latn-13194-1991")
def _stage_main(s):
    s = re.compile("ং(?=[কখগঘঙ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ং(?=[চছজঝঞ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ং(?=[টঠডড়ঢঢ়ণ])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ং(?=[তৎথদধন])", re.MULTILINE).sub("n", s)
    s = re.compile("ং(?=[পফবভম])", re.MULTILINE).sub("m", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_8387657968579450)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bis-ben-Beng-Latn-13194-1991", "main", _stage_main)
_PTREE_8387657968579450 = {2437:{None:"a"},2438:{None:"ā"},2439:{None:"i"},2440:{None:"ī"},2441:{None:"u"},2442:{None:"ū"},2528:{None:"ṛ"},2444:{None:"ḻ"},2447:{None:"ē"},2448:{None:"ai"},2451:{None:"ŏ"},2452:{None:"au"},2453:{None:"k"},2454:{None:"kh"},2455:{None:"g"},2456:{None:"gh"},2457:{None:"ṅ"},2458:{None:"c"},2459:{None:"ch"},2460:{None:"j"},2461:{None:"jh"},2462:{None:"ñ"},2463:{None:"ṭ"},2464:{None:"ṭh"},2465:{None:"ḍ"},2524:{None:"d̂"},2466:{None:"ḍh"},2525:{None:"d̂h"},2467:{None:"ṇ"},2468:{None:"t"},2510:{None:"t"},2469:{None:"th"},2470:{None:"d"},2471:{None:"dh"},2472:{None:"n"},2474:{None:"p"},2475:{None:"ph"},2476:{None:"b"},2477:{None:"bh"},2478:{None:"m"},2479:{None:"y",2492:{None:"ẏ"}},2527:{None:"ẏ"},2480:{None:"r"},2482:{None:"l"},2486:{None:"ś"},2487:{None:"ṣ"},2488:{None:"s"},2489:{None:"h"},2433:{None:"m"},2435:{32:{None:"ḥ"}},2434:{None:"ṃ"},2494:{None:"ā"},2495:{None:"i"},2496:{None:"ī"},2497:{None:"u"},2498:{None:"ū"},2499:{None:"ṛ"},2503:{None:"ē"},2504:{None:"ai"},2507:{None:"ŏ"},2508:{None:"au"},2509:{None:""},2381:{None:""},2364:{None:""},2404:{None:"."},8205:{None:""}}
