import interscript
import regex as re
interscript.stdlib.define_map("bis-guj-Gujr-Latn-13194-1991")
def _stage_main(s):
    s = re.compile("ં(?=[કખગઘઙ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ં(?=[ચછજઝઞ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ં(?=[ટઠડઢણ])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ં(?=[તથદધન])", re.MULTILINE).sub("n", s)
    s = re.compile("ં(?=[પફબભમ])", re.MULTILINE).sub("m", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_819540647467973255)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bis-guj-Gujr-Latn-13194-1991", "main", _stage_main)
_PTREE_819540647467973255 = {2693:{None:"a"},2694:{None:"ā"},2695:{None:"i"},2696:{None:"ī"},2697:{None:"u"},2698:{None:"ū"},2700:{None:"ḻ"},2701:{None:"e"},2703:{None:"ē"},2704:{None:"ai"},2705:{None:"o"},2707:{None:"ŏ"},2708:{None:"au"},2709:{None:"k"},2710:{None:"kh"},2711:{None:"g"},2712:{None:"gh"},2713:{None:"ṅ"},2714:{None:"c"},2715:{None:"ch"},2716:{None:"j"},2717:{None:"jh"},2718:{None:"ñ"},2719:{None:"ṭ"},2720:{None:"ṭh"},2721:{None:"ḍ"},2722:{None:"ḍh"},2723:{None:"ṇ"},2724:{None:"t"},2725:{None:"th"},2726:{None:"d"},2727:{None:"dh"},2728:{None:"n"},2730:{None:"p"},2731:{None:"ph"},2732:{None:"b"},2733:{None:"bh"},2734:{None:"m"},2735:{None:"y"},2736:{None:"r"},2738:{None:"l"},2739:{None:"ḷ"},2741:{None:"v"},2742:{None:"ś"},2743:{None:"ṣ"},2744:{None:"s"},2745:{None:"h"},2689:{None:"m"},2691:{None:"ḥ"},2690:{None:"ṃ"},2750:{None:"ā"},2751:{None:"i"},2752:{None:"ī"},2753:{None:"u"},2754:{None:"ū"},2755:{None:"ṛ"},2757:{None:"e"},2759:{None:"ē"},2760:{None:"ai"},2761:{None:"o"},2763:{None:"ŏ"},2764:{None:"au"},2509:{None:""},2765:{None:""},2748:{None:""},2404:{None:"."},8205:{None:""},2790:{None:"0"},2791:{None:"1"},2792:{None:"2"},2793:{None:"3"},2794:{None:"4"},2795:{None:"5"},2796:{None:"6"},2797:{None:"7"},2798:{None:"8"},2799:{None:"9"}}
