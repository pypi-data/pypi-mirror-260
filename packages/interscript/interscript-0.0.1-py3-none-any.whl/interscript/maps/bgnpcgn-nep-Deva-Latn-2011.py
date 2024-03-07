import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-nep-Deva-Latn-2011")
def _stage_main(s):
    s = re.compile("ं(?=[कखगघ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ं(?=[चछजझ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ं(?=[टठडढ])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ं(?=[तथदध])", re.MULTILINE).sub("n", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4186510602234157683)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bgnpcgn-nep-Deva-Latn-2011", "main", _stage_main)
_PTREE_4186510602234157683 = {2309:{None:"a"},2310:{None:"ā"},2311:{None:"i"},2312:{None:"ī"},2313:{None:"u"},2314:{None:"ū"},2315:{None:"ṛi"},2400:{None:"rī"},2319:{None:"e"},2320:{None:"ai"},2323:{None:"o"},2324:{None:"au"},2366:{None:"ā"},2367:{None:"i"},2368:{None:"ī"},2369:{None:"u"},2370:{None:"ū"},2371:{None:"ṛi"},2372:{None:"rī"},2375:{None:"e"},2376:{None:"ai"},2379:{None:"o"},2380:{None:"au"},2325:{None:"k",2381:{2359:{None:"kṣ"}}},2326:{None:"kh"},2327:{None:"g"},2328:{None:"gh"},2329:{None:"ṅ"},2330:{None:"ch"},2331:{None:"chh"},2332:{None:"j",2381:{2334:{None:"jñ"}}},2333:{None:"jh"},2334:{None:"ñ"},2335:{None:"ṭ"},2336:{None:"ṭh"},2337:{None:"ḍ"},2338:{None:"ḍh"},2339:{None:"ṇ"},2340:{None:"t",2381:{2352:{None:"tr"}}},2341:{None:"th"},2342:{None:"d"},2343:{None:"dh"},2344:{None:"n"},2346:{None:"p"},2347:{None:"ph"},2348:{None:"b"},2349:{None:"bh"},2350:{None:"m"},2351:{None:"y"},2352:{None:"r"},2354:{None:"l"},2357:{None:"v"},2358:{None:"sh"},2359:{None:"ṣ"},2360:{None:"s"},2361:{None:"h"},2306:{None:"ṃ"},2307:{None:"ḥ"},2305:{None:"~"},2373:{None:"r"},2381:{None:"a"},2365:{None:"’"},2406:{None:"0"},2407:{None:"1"},2408:{None:"2"},2409:{None:"3"},2410:{None:"4"},2411:{None:"5"},2412:{None:"6"},2413:{None:"7"},2414:{None:"8"},2415:{None:"9"}}
