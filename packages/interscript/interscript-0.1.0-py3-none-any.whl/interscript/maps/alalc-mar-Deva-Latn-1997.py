import interscript
import regex as re
interscript.stdlib.define_map("alalc-mar-Deva-Latn-1997")
def _stage_main(s):
    s = re.compile("ं(?=[कखगघङ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ं(?=[चछजझञ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ं(?=[टठडढण])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ं(?=[तथदधन])", re.MULTILINE).sub("n", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1955008619655739622)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("alalc-mar-Deva-Latn-1997", "main", _stage_main)
_PTREE_1955008619655739622 = {2309:{None:"a"},2310:{None:"ā"},2311:{None:"i"},2312:{None:"ī"},2313:{None:"u"},2314:{None:"ū"},2315:{None:"ṛ"},2400:{None:"ṝ"},2316:{None:"ḹ"},2319:{None:"e"},2418:{None:"ê"},2320:{None:"ai"},2323:{None:"o"},2321:{None:"ô"},2324:{None:"ău"},2325:{None:"ka"},2326:{None:"kha"},2327:{None:"ga"},2328:{None:"gha"},2329:{None:"ṅa"},2330:{None:"ca"},2331:{None:"cha"},2332:{None:"ja"},2333:{None:"jha"},2334:{None:"ña"},2335:{None:"ṭa"},2336:{None:"ṭha"},2337:{None:"ḍa"},2338:{None:"ḍha"},2339:{None:"ṇa"},2340:{None:"ta"},2341:{None:"tha"},2342:{None:"da"},2343:{None:"dha"},2344:{None:"na"},2346:{None:"pa"},2347:{None:"pha"},2348:{None:"ba"},2349:{None:"bha"},2350:{None:"ma"},2351:{None:"ya"},2352:{None:"ra"},2354:{None:"la"},2355:{None:"la"},2357:{None:"va"},2358:{None:"śa"},2359:{None:"sha"},2360:{None:"sa"},2361:{None:"ha"},2306:{None:"m"},2307:{32:{None:"ḥ"}},2365:{None:"’"},2366:{None:"ā"},2367:{None:"i"},2368:{None:"ī"},2369:{None:"u"},2370:{None:"ū"},2371:{None:"ṛi"},2372:{None:"rī"},2375:{None:"e"},2379:{None:"o"},2380:{None:"au"},2381:{None:""},2406:{None:"0"},2407:{None:"1"},2408:{None:"2"},2409:{None:"3"},2410:{None:"4"},2411:{None:"5"},2412:{None:"6"},2413:{None:"7"},2414:{None:"8"},2415:{None:"9"}}
