import interscript
import regex as re
interscript.stdlib.define_map("odni-hin-Deva-Latn-2015")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1335944438044259755)
    return s

interscript.stdlib.add_map_stage("odni-hin-Deva-Latn-2015", "main", _stage_main)
_PTREE_1335944438044259755 = {2309:{None:"a"},2310:{None:"a"},2311:{None:"i"},2312:{None:"i"},2313:{None:"u"},2314:{None:"u"},2315:{None:"ri"},2319:{None:"e"},2320:{None:"ai"},2321:{None:"o"},2323:{None:"au"},2325:{None:"k",2381:{2359:{None:"ksha"}},2364:{None:"q"}},2326:{None:"kh",2364:{None:"kh"}},2327:{None:"g",2364:{None:"gh"}},2328:{None:"gh"},2329:{None:"n"},2330:{None:"ch"},2331:{None:"ch"},2332:{None:"j",2364:{None:"z"}},2333:{None:"jh"},2334:{None:"n"},2335:{None:"t"},2336:{None:"th"},2337:{None:"d"},2396:{None:"r"},2338:{None:"dh"},2397:{None:"rh"},2339:{None:"n"},2340:{None:"t"},2341:{None:"th"},2342:{None:"d"},2343:{None:"dh"},2344:{None:"n"},2346:{None:"p"},2347:{None:"ph",2364:{None:"f"}},2348:{None:"b"},2349:{None:"bh"},2350:{None:"m"},2351:{None:"y"},2352:{None:"r"},2354:{None:"l"},2357:{None:"v"},2358:{None:"sh"},2359:{None:"sh"},2360:{None:"s"},2361:{None:"h"},2306:{None:"n"},2307:{32:{None:"h"}},2305:{None:"n"},2364:{None:""},2381:{None:""},2366:{None:"a"},2367:{None:"i"},2368:{None:"i"},2369:{None:"u"},2370:{None:"u"},2371:{None:"ri"},2375:{None:"e"},2376:{None:"ai"},2373:{None:"ai"},2378:{None:"o"},2379:{None:"o"},2380:{None:"au"},2377:{None:"au"}}
