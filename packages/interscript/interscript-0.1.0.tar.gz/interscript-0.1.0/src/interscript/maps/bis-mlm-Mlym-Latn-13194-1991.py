import interscript
import regex as re
interscript.stdlib.define_map("bis-mlm-Mlym-Latn-13194-1991")
def _stage_main(s):
    s = re.compile("ം(?=[കൿഖഗഘങ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ം(?=[ചഛജഝഞ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ം(?=[ടഠഡഢണ])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ം(?=[തഥദധന])", re.MULTILINE).sub("n", s)
    s = re.compile("ം(?=[പഫബഭമ])", re.MULTILINE).sub("m", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4201623487446325839)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bis-mlm-Mlym-Latn-13194-1991", "main", _stage_main)
_PTREE_4201623487446325839 = {3333:{None:"a"},3334:{None:"ā"},3335:{None:"i"},3336:{None:"ī"},3337:{None:"u"},3338:{None:"ū"},3339:{None:"ṛ"},3340:{None:"ḻ"},3342:{None:"e"},3343:{None:"ē"},3344:{None:"ai"},3346:{None:"o"},3347:{None:"ŏ"},3348:{None:"au"},3349:{None:"k"},3455:{None:"k"},3350:{None:"kh"},3351:{None:"g"},3352:{None:"gh"},3353:{None:"ṅ"},3354:{None:"c"},3355:{None:"ch"},3356:{None:"j"},3357:{None:"jh"},3358:{None:"ñ"},3359:{None:"ṭ"},3360:{None:"ṭh"},3361:{None:"d̂"},3362:{None:"ḍh"},3363:{None:"ṇ"},3364:{None:"t"},3365:{None:"th"},3366:{None:"d"},3367:{None:"dh"},3368:{None:"n"},3370:{None:"p"},3371:{None:"ph"},3372:{None:"b"},3373:{None:"bh"},3374:{None:"m"},3375:{None:"y"},3376:{None:"r"},3452:{None:"r"},3377:{None:"ṟ"},3453:{None:"l"},3378:{None:"l"},3379:{None:"ḷ"},3454:{None:"ḷ"},3380:{None:"ẕ"},3381:{None:"v"},3382:{None:"ś"},3383:{None:"ṣ"},3384:{None:"s"},3385:{None:"h"},3329:{None:"m"},3331:{None:"ḥ"},3330:{None:"ṃ"},3390:{None:"ā"},3391:{None:"i"},3392:{None:"ī"},3393:{None:"u"},3394:{None:"ū"},3395:{None:"ṛ"},3396:{None:"ṝ"},3398:{None:"e"},3399:{None:"ē"},3400:{None:"ai"},3402:{None:"o"},3403:{None:"ō"},3404:{None:"au"},3450:{None:"n"},3451:{None:"ṇ"},2381:{None:""},3405:{None:""},2364:{None:""},3415:{None:""},8205:{None:""},8204:{None:""}}
