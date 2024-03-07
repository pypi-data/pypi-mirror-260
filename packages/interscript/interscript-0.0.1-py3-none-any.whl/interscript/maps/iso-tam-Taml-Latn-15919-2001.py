import interscript
import regex as re
interscript.stdlib.define_map("iso-tam-Taml-Latn-15919-2001")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4056452700323610813)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("iso-tam-Taml-Latn-15919-2001", "main", _stage_main)
_PTREE_4056452700323610813 = {2949:{None:"a"},2950:{None:"ā"},3006:{None:"ā"},2951:{None:"i"},3007:{None:"i"},2952:{None:"ī"},3008:{None:"ī"},2953:{None:"u"},3009:{None:"u"},2954:{None:"ū"},3010:{None:"ū"},3014:{None:"e"},2958:{None:"e"},3015:{None:"ē"},2959:{None:"ē"},2960:{None:"ai"},3016:{None:"ai"},2962:{None:"o"},3018:{None:"o"},3019:{None:"ō"},2963:{None:"ō"},2964:{None:"au"},3020:{None:"au"},2965:{None:"ka"},2969:{None:"ṅa"},2947:{None:"ḵ"},2970:{None:"ca"},2974:{None:"ña"},2975:{None:"ṭa"},2979:{None:"ṇa"},2980:{None:"ta"},2984:{None:"na"},2986:{None:"pa"},2990:{None:"ma"},2991:{None:"ya"},2992:{None:"ra"},2994:{None:"la"},2995:{None:"ḷa"},2996:{None:"ḻa"},2997:{None:"va"},2993:{None:"ṟa"},2985:{None:"ṉa"},2972:{None:"ja"},2998:{None:"śa"},2999:{None:"ṣa"},3000:{None:"sa"},3001:{None:"ha"},3047:{None:"1"},3048:{None:"2"},3049:{None:"3"},3050:{None:"4"},3051:{None:"5"},3052:{None:"6"},3053:{None:"7"},3054:{None:"8"},3055:{None:"9"},3056:{None:"10"},3057:{None:"100"},3058:{None:"1000"},3021:{None:""},8205:{None:""},8204:{None:""}}
