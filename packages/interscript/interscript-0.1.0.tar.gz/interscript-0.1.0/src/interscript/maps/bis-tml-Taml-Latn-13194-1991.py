import interscript
import regex as re
interscript.stdlib.define_map("bis-tml-Taml-Latn-13194-1991")
def _stage_main(s):
    s = re.compile("ஂ(?=[கங])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ஂ(?=[சஜஞ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ஂ(?=[டண])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ஂ(?=[தநன])", re.MULTILINE).sub("n", s)
    s = re.compile("ஂ(?=[பம])", re.MULTILINE).sub("m", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2704324928500048417)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bis-tml-Taml-Latn-13194-1991", "main", _stage_main)
_PTREE_2704324928500048417 = {2949:{None:"a"},2950:{None:"ā"},2951:{None:"i"},2952:{None:"ī"},2953:{None:"u"},2954:{None:"ū"},2958:{None:"e"},2959:{None:"ē"},2960:{None:"ai"},2962:{None:"o"},2963:{None:"ŏ"},2964:{None:"au"},2965:{None:"k"},2969:{None:"ṅ"},2970:{None:"c"},2972:{None:"j"},2974:{None:"ñ"},2975:{None:"ṭ"},2979:{None:"ṇ"},2980:{None:"t"},2984:{None:"n"},2985:{None:"ṉ"},2986:{None:"p"},2990:{None:"m"},2991:{None:"y"},2992:{None:"r"},2993:{None:"ṟ"},2994:{None:"l"},2995:{None:"ḷ"},2996:{None:"ẕ"},2997:{None:"v"},2998:{None:"ś"},2999:{None:"ṣ"},3000:{None:"s"},3001:{None:"h"},2947:{None:"ḥ"},2946:{None:"ṃ"},3006:{None:"ā"},3007:{None:"i"},3008:{None:"ī"},3009:{None:"u"},3010:{None:"ū"},3395:{None:"ṛ"},3396:{None:"ṝ"},3014:{None:"e"},3015:{None:"ē"},3016:{None:"ai"},3018:{None:"o"},3019:{None:"ō"},3020:{None:"au"},3450:{None:"n"},3451:{None:"ṇ"},2381:{None:""},3405:{None:""},3021:{None:""},3415:{None:""},8205:{None:""},8204:{None:""}}
