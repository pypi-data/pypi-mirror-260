import interscript
import regex as re
interscript.stdlib.define_map("iso-guj-Gujr-Latn-15919-2001")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_688321765408719538)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("iso-guj-Gujr-Latn-15919-2001", "main", _stage_main)
_PTREE_688321765408719538 = {2693:{None:"a"},2694:{None:"ā"},2695:{None:"i"},2696:{None:"ī"},2697:{None:"u"},2698:{None:"ū"},2699:{None:"ṛ"},2784:{None:"ṝ"},2700:{None:"ḷ"},2785:{None:"ḹ"},2701:{None:"ê"},2703:{None:"e"},2704:{None:"ai"},2705:{None:"ô"},2707:{None:"o"},2708:{None:"au"},2709:{None:"ka",2748:{None:"qa"}},2710:{None:"kha",2748:{None:"ḵẖa"}},2711:{None:"ga",2748:{None:"ġa"}},2712:{None:"gha"},2713:{None:"ṅa"},2714:{None:"ca"},2715:{None:"cha"},2716:{None:"ja",2748:{None:"za"}},2717:{None:"jha"},2718:{None:"ña"},2719:{None:"tạ"},2720:{None:"ṭha"},2721:{None:"ḍa"},2722:{None:"ḍha"},2723:{None:"ṇa"},2724:{None:"ta"},2725:{None:"tha"},2726:{None:"da"},2727:{None:"dha"},2728:{None:"na"},2730:{None:"pa"},2731:{None:"pha",2748:{None:"fa"}},2732:{None:"ba"},2733:{None:"bha"},2734:{None:"ma"},2735:{None:"ya",2689:{None:"m̐ya"}},2736:{None:"ra",2689:{None:"m̐ra"}},2738:{None:"la",2689:{None:"m̐la"}},2739:{None:"ḷa",2689:{None:"m̐ḷa"}},2741:{None:"va",2689:{None:"m̐va"}},2742:{None:"śa"},2743:{None:"ṣa"},2744:{None:"sa"},2745:{None:"ha"},2689:{None:"m̐"},2691:{None:"ḥ"},2690:{None:"ṁ"},2750:{None:"ā"},2751:{None:"i"},2752:{None:"ī"},2753:{None:"u"},2754:{None:"ū"},2755:{None:"ṛ"},2756:{None:"ṝ"},2786:{None:"ḷ"},2787:{None:"ḹ"},2757:{None:"ê"},2761:{None:"ô"},2759:{None:"e"},2760:{None:"ai"},2763:{None:"o"},2764:{None:"au"},2365:{None:":’"},2509:{None:""},2765:{None:""},2748:{None:""},2404:{None:"."},8205:{None:""},2790:{None:"0"},2791:{None:"1"},2792:{None:"2"},2793:{None:"3"},2794:{None:"4"},2795:{None:"5"},2796:{None:"6"},2797:{None:"7"},2798:{None:"8"},2799:{None:"9"}}
