import interscript
import regex as re
interscript.stdlib.define_map("var-hin-Deva-Latn-hunterian-1872")
def _stage_main(s):
    s = re.compile("आ(?="+interscript.stdlib.aliases["boundary"]+")", re.MULTILINE).sub("a", s)
    s = re.compile("ई(?="+interscript.stdlib.aliases["boundary"]+")", re.MULTILINE).sub("i", s)
    s = re.compile("ऊ(?="+interscript.stdlib.aliases["boundary"]+")", re.MULTILINE).sub("u", s)
    s = re.compile("व(?=[इई])", re.MULTILINE).sub("v", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2540449098995618647)
    return s

interscript.stdlib.add_map_stage("var-hin-Deva-Latn-hunterian-1872", "main", _stage_main)
_PTREE_2540449098995618647 = {2309:{None:"a"},2310:{None:"ā"},2311:{None:"i"},2312:{None:"ī"},2313:{None:"u"},2314:{None:"ū"},2315:{None:"ri"},2319:{None:"e"},2320:{None:"ai"},2323:{None:"o"},2324:{None:"au"},2325:{None:"ka",2364:{None:"qa",2381:{None:"q"}},2381:{None:"k"}},2326:{None:"kha",2364:{None:"kha",2381:{None:"kh"}},2381:{None:"kh"}},2327:{None:"ga",2364:{None:"ġa",2381:{None:"ġ"}},2381:{None:"g"}},2328:{None:"gha",2381:{None:"gh"}},2329:{None:"nga",2381:{None:"ng"}},2330:{None:"cha",2381:{None:"ch"}},2331:{None:"chha",2381:{None:"chh"}},2332:{None:"ja",2364:{None:"za",2381:{None:"z"}},2381:{2334:{None:"gy"},None:"j"}},2333:{None:"jha",2381:{None:"jh"}},2334:{None:"nya",2381:{None:"ny"}},2335:{None:"ta",2381:{None:"t"}},2336:{None:"tha",2381:{None:"th"}},2337:{None:"da",2364:{None:"ṙa",2381:{None:"ṙ"}},2381:{None:"d"}},2338:{None:"dha",2364:{None:"ṙha",2381:{None:"ṙh"}},2381:{None:"dh"}},2339:{None:"na",2381:{None:"n"}},2340:{None:"ta",2381:{None:"t"}},2341:{None:"tha",2381:{None:"th"}},2342:{None:"da",2381:{None:"d"}},2343:{None:"dha",2381:{None:"dh"}},2344:{None:"na",2381:{None:"n"}},2346:{None:"pa",2381:{None:"p"}},2347:{None:"pha",2364:{None:"fa",2381:{None:"f"}},2381:{None:"ph"}},2348:{None:"ba",2381:{None:"b"}},2349:{None:"bha",2381:{None:"bh"}},2350:{None:"ma",2381:{None:"m"}},2351:{None:"ya",2381:{None:"y"}},2352:{None:"ra",2381:{None:"r"}},2354:{None:"la",2381:{None:"l"}},2357:{None:"wa",2381:{None:"w"}},2358:{None:"sa",2381:{None:"s"}},2359:{None:"sha",2381:{None:"sh"}},2360:{None:"sa",2381:{None:"s"}},2361:{None:"ha",2381:{None:"h"}},2355:{None:"la",2381:{None:"l"}},2306:{None:"n"},2307:{None:"h"},2305:{None:"m"},2366:{None:"ā"},2367:{None:"i"},2368:{None:"ī"},2369:{None:"u"},2370:{None:"ū"},2371:{None:"ri"},2375:{None:"e"},2376:{None:"ai"},2379:{None:"o"},2380:{None:"au"},8205:{None:""}}
