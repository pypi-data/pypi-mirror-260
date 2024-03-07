import interscript
import regex as re
interscript.stdlib.define_map("alalc-pan-Guru-Latn-1997")
def _stage_main(s):
    s = re.compile("ਂ(?=[ਕਖਖ਼ਗਗ਼ਘਙ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ਂ(?=[ਚਛਜਜ਼ਝਞ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ਂ(?=[ਟਠਡਢਣ])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ਂ(?=[ਤਥਦਧਨ])", re.MULTILINE).sub("n", s)
    s = re.compile("ੰ(?=[ਕਖਖ਼ਗਗ਼ਘਙ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ੰ(?=[ਚਛਜਜ਼ਝਞ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ੰ(?=[ਟਠਡਢਣ])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ੰ(?=[ਤਥਦਧਨ])", re.MULTILINE).sub("n", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_869816490270329571)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("alalc-pan-Guru-Latn-1997", "main", _stage_main)
_PTREE_869816490270329571 = {2565:{None:"a"},2566:{None:"ā"},2567:{None:"i"},2568:{None:"ī"},2569:{None:"u"},2570:{None:"ū"},2575:{None:"e"},2576:{None:"ai"},2579:{None:"o"},2580:{None:"au"},2581:{None:"ka"},2582:{None:"kha",2620:{None:"kha"}},2583:{None:"ga",2620:{None:"gha"}},2584:{None:"gha"},2585:{None:"ṅa"},2586:{None:"ca"},2587:{None:"cha"},2588:{2620:{None:"za"},None:"ja"},2589:{None:"jha"},2590:{None:"ña"},2591:{None:"ṭa"},2592:{None:"ṭha"},2593:{None:"ḍa"},2594:{None:"ḍha"},2595:{None:"ṇa"},2596:{None:"ta"},2597:{None:"tha"},2598:{None:"da"},2599:{None:"dha"},2600:{None:"na"},2602:{None:"pa"},2603:{None:"pha",2620:{None:"fa"}},2604:{None:"ba"},2605:{None:"bha"},2606:{None:"ma"},2607:{None:"ya"},2608:{None:"ra"},2610:{None:"la",2677:{None:"ḷa"},2620:{None:"ḷa"}},2613:{None:"wa"},2652:{None:"ṛa"},2616:{None:"sa",2620:{None:"sha"}},2617:{None:"ha"},2562:{None:"ṃ"},2672:{None:"m̆̐"},2622:{None:"ā"},2623:{None:"i"},2624:{None:"ī"},2625:{None:"u"},2626:{None:"ū"},2631:{None:"e"},2632:{None:"ai"},2635:{None:"o"},2636:{None:"au"},2673:{2581:{None:"kka"},2582:{None:"kkha"},2649:{None:"kkha"},2583:{None:"gga"},2650:{None:"ggha"},2584:{None:"ggha"},2585:{None:"ṅṅa"},2586:{None:"cca"},2587:{None:"ccha"},2588:{None:"jja"},2651:{None:"zza"},2589:{None:"jjha"},2590:{None:"ñña"},2591:{None:"ṭṭa"},2592:{None:"ṭṭha"},2593:{None:"ḍḍa"},2594:{None:"ḍḍha"},2595:{None:"ṇṇa"},2596:{None:"tta"},2597:{None:"ttha"},2598:{None:"dda"},2599:{None:"ddha"},2600:{None:"nna"},2602:{None:"ppa"},2603:{None:"ppha"},2654:{None:"ffa"},2604:{None:"bba"},2605:{None:"bbha"},2606:{None:"mma"},2607:{None:"yya"},2608:{None:"rra"},2610:{None:"lla",2677:{None:"ḷḷa"}},2613:{None:"wwa"},2652:{None:"ṛṛa"},2616:{None:"ssa"},2614:{None:"ssha"},2617:{None:"hha"}},2662:{None:"0"},2663:{None:"1"},2664:{None:"2"},2665:{None:"3"},2666:{None:"4"},2667:{None:"5"},2668:{None:"6"},2669:{None:"7"},2670:{None:"8"},2671:{None:"9"}}
