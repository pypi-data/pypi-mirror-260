import interscript
import regex as re
interscript.stdlib.define_map("bis-pnj-Guru-Latn-13194-1991")
def _stage_main(s):
    s = re.compile("ੰ(?=[ਕਖਖ਼ਗਗ਼ਘਙ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ੰ(?=[ਚਛਜਜ਼ਝਞ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ੰ(?=[ਟਠਡਢਣ])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ੰ(?=[ਤਥਦਧਨ])", re.MULTILINE).sub("n", s)
    s = re.compile("ੰ(?=[ਪਫਬਭਮ])", re.MULTILINE).sub("m", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1128270096558505675)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bis-pnj-Guru-Latn-13194-1991", "main", _stage_main)
_PTREE_1128270096558505675 = {2565:{None:"a"},2566:{None:"ā"},2567:{None:"i"},2568:{None:"ī"},2569:{None:"u"},2570:{None:"ū"},2674:{None:"ṛ"},2675:{None:"ṝ"},2575:{None:"ē"},2576:{None:"ai"},2579:{None:"ŏ"},2580:{None:"au"},2581:{None:"k"},2582:{None:"kh"},2583:{None:"g"},2584:{None:"gh"},2585:{None:"ṅ"},2586:{None:"c"},2587:{None:"ch"},2588:{None:"j"},2589:{None:"jh"},2590:{None:"ñ"},2591:{None:"ṭ"},2592:{None:"ṭh"},2593:{None:"ḍ"},2594:{None:"ḍh"},2595:{None:"ṇ"},2596:{None:"t"},2597:{None:"th"},2598:{None:"d"},2652:{None:"ṛa"},2599:{None:"dh"},2600:{None:"ṉ"},2602:{None:"p"},2603:{None:"ph"},2604:{None:"b"},2605:{None:"bh"},2606:{None:"m"},2607:{None:"y"},2608:{None:"r"},2610:{None:"l"},2611:{None:"ḷ"},2613:{None:"v"},2614:{None:"ś"},2616:{None:"s"},2617:{None:"h"},2392:{None:"q"},2649:{None:"ḵẖ"},2650:{None:"gẖ"},2651:{None:"z"},2654:{None:"f"},2305:{None:"m"},2307:{32:{None:"ḥ"}},2562:{None:"n"},2672:{None:"ṃ"},2622:{None:"ā"},2623:{None:"i"},2624:{None:"ī"},2625:{None:"u"},2626:{None:"ū"},2371:{None:"ṛ"},2631:{None:"ē"},2632:{None:"ai"},2635:{None:"ō"},2636:{None:"au"},2637:{None:""},2620:{None:""},2673:{None:""},2404:{None:"."},8205:{None:""}}
