import interscript
import regex as re
interscript.stdlib.define_map("alalc-pli-Deva-Latn-2012")
def _stage_main(s):
    s = re.compile("ं(?=[कखगघङ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ं(?=[चछजझञ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ं(?=[टठडढण])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ं(?=[तथदधन])", re.MULTILINE).sub("n", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1305616817846916826)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("alalc-pli-Deva-Latn-2012", "main", _stage_main)
_PTREE_1305616817846916826 = {2309:{None:"a"},2310:{None:"ā"},2311:{None:"i"},2312:{None:"ī"},2313:{None:"u"},2314:{None:"ū"},2319:{None:"e"},2323:{None:"o"},2325:{None:"ka"},2326:{None:"kha"},2327:{None:"ga"},2328:{None:"gha"},2329:{None:"ṅa"},2330:{None:"ca"},2331:{None:"cha"},2332:{None:"ja"},2333:{None:"jha"},2334:{None:"ña"},2335:{None:"ṭa"},2336:{None:"ṭha"},2337:{None:"ḍa"},2338:{None:"ḍha"},2339:{None:"ṇa"},2340:{None:"ta"},2341:{None:"tha"},2342:{None:"da"},2343:{None:"dha"},2344:{None:"na"},2346:{None:"pa"},2347:{None:"pha"},2348:{None:"ba"},2349:{None:"bha"},2350:{None:"ma"},2351:{None:"ya"},2352:{None:"ra"},2354:{None:"la"},2355:{None:"ḻa"},2357:{None:"va"},2358:{None:"śa"},2359:{None:"ṣa"},2360:{None:"sa"},2361:{None:"ha"},2307:{None:"ḥ"},2306:{None:"ṃ"},2366:{None:"ā"},2367:{None:"i"},2368:{None:"ī"},2369:{None:"u"},2370:{None:"ū"},2375:{None:"e"},2379:{None:"o"},2381:{None:""},8205:{None:""}}
