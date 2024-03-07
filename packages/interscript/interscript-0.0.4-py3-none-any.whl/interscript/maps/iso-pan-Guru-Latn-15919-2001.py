import interscript
import regex as re
interscript.stdlib.define_map("iso-pan-Guru-Latn-15919-2001")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3464582987820025643)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("iso-pan-Guru-Latn-15919-2001", "main", _stage_main)
_PTREE_3464582987820025643 = {2565:{None:"a"},2566:{None:"ā"},2567:{None:"i"},2568:{None:"ī"},2569:{None:"u"},2570:{None:"ū"},2575:{None:"e"},2576:{None:"ai"},2579:{None:"o"},2580:{None:"au"},2581:{None:"ka",2620:{None:"qa"}},2582:{None:"kha",2620:{None:"ḵẖa"}},2583:{None:"ga",2620:{None:"ġa"}},2584:{None:"gha"},2585:{None:"ṅa"},2586:{None:"ca"},2587:{None:"cha"},2588:{None:"ja",2620:{None:"za"}},2589:{None:"jha"},2590:{None:"ña"},2591:{None:"ṭa"},2592:{None:"ṭha"},2593:{None:"ḍa"},2594:{None:"ḍha"},2595:{None:"ṇa"},2596:{None:"ta"},2597:{None:"tha"},2598:{None:"da"},2599:{None:"dha"},2600:{None:"na"},2602:{None:"pa"},2603:{None:"pha",2620:{None:"fa"}},2604:{None:"ba"},2605:{None:"bha"},2606:{None:"ma"},2607:{None:"ya"},2608:{None:"ra"},2610:{None:"la",2620:{None:"ḷa"}},2613:{None:"va"},2652:{None:"ṛa"},2616:{None:"sa",2620:{None:"śa"}},2617:{None:"ha"},2562:{None:"ṃ",2568:{None:"ī:ṃ"}},2672:{None:"ṁ",2568:{None:"ī:ṁ"}},2563:{None:"ḥ"},2561:{None:"m̐"},2622:{None:"ā"},2623:{None:"i"},2624:{None:"ī"},2625:{None:"u"},2626:{None:"ū"},2631:{None:"e"},2632:{None:"ai"},2635:{None:"o"},2636:{None:"au"},2673:{None:"",2565:{None:":a"},2566:{None:":ā"},2567:{None:":i"},2568:{None:":ī"},2569:{None:":u"},2570:{None:":ū"},2575:{None:":e"},2576:{None:":ai"},2579:{None:":o"},2580:{None:":au"},2622:{None:":ā"},2623:{None:":i"},2624:{None:":ī"},2625:{None:":u"},2626:{None:":ū"},2631:{None:":e"},2632:{None:":ai"},2635:{None:":o"},2636:{None:":au"}},2662:{None:"0"},2663:{None:"1"},2664:{None:"2"},2665:{None:"3"},2666:{None:"4"},2667:{None:"5"},2668:{None:"6"},2669:{None:"7"},2670:{None:"8"},2671:{None:"9"}}
