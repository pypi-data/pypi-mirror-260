import interscript
import regex as re
interscript.stdlib.define_map("bis-dev-Deva-Latn-13194-1991")
def _stage_main(s):
    s = re.compile("ं(?=[कखगघङ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ं(?=[चछजझञ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ं(?=[टठडढण])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ं(?=[तथदधन])", re.MULTILINE).sub("n", s)
    s = re.compile("ं(?=[पफबभम])", re.MULTILINE).sub("m", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3893657775439397268)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bis-dev-Deva-Latn-13194-1991", "main", _stage_main)
_PTREE_3893657775439397268 = {2309:{None:"a"},2310:{None:"ā"},2311:{None:"i"},2312:{None:"ī"},2313:{None:"u"},2314:{None:"ū"},2315:{None:"ṛ"},2400:{None:"ṝ"},2316:{None:"ḻ"},2401:{None:"ḹ"},2319:{None:"ē"},2320:{None:"ai"},2317:{None:"ê"},2322:{None:"o"},2323:{None:"ŏ"},2324:{None:"au"},2321:{None:"ô"},2325:{None:"k"},2326:{None:"kh"},2327:{None:"g"},2328:{None:"gh"},2329:{None:"ṅ"},2330:{None:"c"},2331:{None:"ch"},2332:{None:"j"},2333:{None:"jh"},2334:{None:"ñ"},2335:{None:"ṭ"},2336:{None:"ṭh"},2337:{None:"ḍ"},2338:{None:"ḍh"},2339:{None:"ṇ"},2340:{None:"t"},2341:{None:"th"},2342:{None:"d"},2343:{None:"dh"},2344:{None:"n"},2345:{None:"ṉ"},2346:{None:"p"},2347:{None:"ph"},2348:{None:"b"},2349:{None:"bh"},2350:{None:"m"},2351:{None:"y"},2399:{None:"ẏ"},2352:{None:"r"},2353:{None:"ṟ"},2354:{None:"l"},2355:{None:"ḷ"},2356:{None:"ẕ"},2357:{None:"v"},2358:{None:"ś"},2359:{None:"ṣ"},2360:{None:"s"},2361:{None:"h"},2392:{None:"q"},2393:{None:"ḵẖ"},2394:{None:"gẖ"},2395:{None:"z"},2396:{None:"d̂"},2397:{None:"d̂h"},2398:{None:"f"},2305:{None:"m"},2307:{32:{None:"ḥ"}},2306:{None:"ṃ"},2366:{None:"ā"},2367:{None:"i"},2368:{None:"ī"},2369:{None:"u"},2370:{None:"ū"},2371:{None:"ṛ"},2374:{None:"e"},2375:{None:"ē"},2376:{None:"ai"},2373:{None:"ê"},2378:{None:"o"},2379:{None:"ō"},2380:{None:"au"},2377:{None:"ô"},2381:{None:""},2364:{None:""},2404:{None:"."},8205:{None:""}}
