import interscript
import regex as re
interscript.stdlib.define_map("bis-kan-Kana-Latn-13194-1991")
def _stage_main(s):
    s = re.compile("ಂ(?=[ಕಖಗಘಙ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ಂ(?=[ಚಛಜಝಞ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ಂ(?=[ಟಠಡಢಣ])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ಂ(?=[ತಥದಧನ])", re.MULTILINE).sub("n", s)
    s = re.compile("ಂ(?=[ಪಫಬಭಮ])", re.MULTILINE).sub("m", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2269037585828049628)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bis-kan-Kana-Latn-13194-1991", "main", _stage_main)
_PTREE_2269037585828049628 = {3205:{None:"a"},3206:{None:"ā"},3207:{None:"i"},3208:{None:"ī"},3209:{None:"u"},3210:{None:"ū"},3211:{None:"ṛ"},3212:{None:"ḻ"},3214:{None:"e"},3215:{None:"ē"},3216:{None:"ai"},3218:{None:"o"},3219:{None:"ŏ"},3220:{None:"au"},3221:{None:"k"},3222:{None:"kh"},3223:{None:"g"},3224:{None:"gh"},3225:{None:"ṅ"},3226:{None:"c"},3227:{None:"ch"},3228:{None:"j"},3229:{None:"jh"},3230:{None:"ñ"},3231:{None:"ṭ"},3232:{None:"ṭh"},3233:{None:"ḍ"},3234:{None:"ḍh"},3235:{None:"ṇ"},3236:{None:"t"},3237:{None:"th"},3238:{None:"d"},3239:{None:"dh"},3240:{None:"n"},3242:{None:"p"},3243:{None:"ph"},3244:{None:"b"},3245:{None:"bh"},3246:{None:"m"},3247:{None:"y"},3248:{None:"r"},3249:{None:"ṟ"},3250:{None:"l"},3251:{None:"ḷ"},3253:{None:"v"},3254:{None:"ś"},3255:{None:"ṣ"},3256:{None:"s"},3257:{None:"h"},3200:{None:"m"},3201:{None:"m"},3203:{None:"ḥ"},3202:{None:"ṃ"},36:{3260:{None:""}},3262:{None:"ā"},3263:{None:"i"},3264:{None:"ī"},3265:{None:"u"},3266:{None:"ū"},3267:{None:"ṛ"},3268:{None:"ṛr"},3270:{None:"e"},3271:{None:"ē"},3272:{None:"ai"},3274:{None:"o"},3275:{None:"ō"},3276:{None:"au"},2381:{None:""},2364:{None:""},3277:{None:""},8205:{None:""},8204:{None:""}}
