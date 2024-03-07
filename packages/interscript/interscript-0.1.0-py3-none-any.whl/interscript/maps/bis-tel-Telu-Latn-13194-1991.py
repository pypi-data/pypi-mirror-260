import interscript
import regex as re
interscript.stdlib.define_map("bis-tel-Telu-Latn-13194-1991")
def _stage_main(s):
    s = re.compile("ం(?=[కఖగఘఙ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ం(?=[చఛజఝఞ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ం(?=[టఠడఢణ])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ం(?=[తథదధన])", re.MULTILINE).sub("n", s)
    s = re.compile("ం(?=[పఫబభమ])", re.MULTILINE).sub("m", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4521402273216017790)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bis-tel-Telu-Latn-13194-1991", "main", _stage_main)
_PTREE_4521402273216017790 = {3077:{None:"a"},3078:{None:"ā"},3079:{None:"i"},3080:{None:"ī"},3081:{None:"u"},3082:{None:"ū"},3083:{None:"ṛ"},3084:{None:"ḻ"},3169:{None:"ḻ"},3086:{None:"e"},3087:{None:"ē"},3088:{None:"ai"},3090:{None:"o"},3091:{None:"ŏ"},3092:{None:"au"},3093:{None:"k",3149:{3127:{None:"kṣa"}}},3094:{None:"kh"},3095:{None:"g"},3096:{None:"gh"},3097:{None:"ṅ"},3098:{None:"c"},3099:{None:"ch"},3100:{None:"j"},3101:{None:"jh"},3102:{None:"ñ"},3103:{None:"ṭ"},3104:{None:"ṭh"},3105:{None:"ḍ"},3106:{None:"ḍh"},3107:{None:"ṇ"},3108:{None:"t"},3109:{None:"th"},3110:{None:"d"},3111:{None:"dh"},3112:{None:"n"},3114:{None:"p"},3115:{None:"ph"},3116:{None:"b"},3117:{None:"bh"},3118:{None:"m"},3119:{None:"y"},3120:{None:"r"},3121:{None:"ṛ"},3122:{None:"l"},3123:{None:"ḷ"},3125:{None:"v"},3126:{None:"ś"},3127:{None:"ṣ"},3128:{None:"s"},3129:{None:"h"},2433:{None:"m"},3075:{None:"ḥ"},3074:{None:"ṃ"},3134:{None:"ā"},3135:{None:"i"},3136:{None:"ī"},3137:{None:"u"},3138:{None:"ū"},3139:{None:"ṛ"},3142:{None:"e"},3143:{None:"ē"},3144:{None:"ai"},3146:{None:"o"},3147:{None:"ŏ"},3148:{None:"au"},2509:{None:""},3149:{None:""},3157:{9:{None:""}},3158:{9:{None:""}},2381:{None:""},2364:{None:""},8205:{None:""},8204:{None:""}}
