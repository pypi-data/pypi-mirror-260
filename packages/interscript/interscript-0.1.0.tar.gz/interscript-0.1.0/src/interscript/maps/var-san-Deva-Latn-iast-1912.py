import interscript
import regex as re
interscript.stdlib.define_map("var-san-Deva-Latn-iast-1912")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2834615992258805243)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("var-san-Deva-Latn-iast-1912", "main", _stage_main)
_PTREE_2834615992258805243 = {2309:{None:"a",2306:{None:"ṃ"},2307:{None:"ḥ"},2305:{None:"m̐"}},2310:{None:"ā"},2311:{None:"i"},2312:{None:"ī"},2313:{None:"u"},2314:{None:"ū"},2315:{None:"ṛ"},2400:{None:"ṝ"},2316:{None:"ḷ"},2401:{None:"ḹ"},2319:{None:"e"},2320:{None:"ai"},2323:{None:"o"},2324:{None:"au"},2325:{None:"ka"},2326:{None:"kha"},2327:{None:"ga"},2328:{None:"gha"},2329:{None:"ṅa"},2330:{None:"ca"},2331:{None:"cha"},2332:{None:"ja"},2333:{None:"jha"},2334:{None:"ña"},2335:{None:"ṭa"},2336:{None:"ṭha"},2337:{None:"ḍa"},2338:{None:"ḍha"},2339:{None:"ṇa"},2340:{None:"ta"},2341:{None:"tha"},2342:{None:"da"},2343:{None:"dha"},2344:{None:"na"},2346:{None:"pa"},2347:{None:"pha"},2348:{None:"ba"},2349:{None:"bha"},2350:{None:"ma"},2351:{None:"ya"},2352:{None:"ra"},2354:{None:"la"},2357:{None:"va"},2358:{None:"śa"},2359:{None:"ṣa"},2360:{None:"sa"},2361:{None:"ha"},2306:{None:"ṃ"},2307:{None:"ḥ"},2305:{None:"m̐"},2365:{None:"’"},2366:{None:"ā"},2367:{None:"i"},2368:{None:"ī"},2369:{None:"u"},2370:{None:"ū"},2371:{None:"ṛ"},2372:{None:"ṝ"},2402:{None:"ḷ"},2403:{None:"ḹ"},2375:{None:"e"},2376:{None:"ai"},2379:{None:"o"},2380:{None:"au"},2381:{None:""},8205:{None:""}}
