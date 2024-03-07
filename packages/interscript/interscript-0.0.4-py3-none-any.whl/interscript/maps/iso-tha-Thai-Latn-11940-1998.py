import interscript
import regex as re
interscript.stdlib.define_map("iso-tha-Thai-Latn-11940-1998")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3346412124062405419)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("iso-tha-Thai-Latn-11940-1998", "main", _stage_main)
_PTREE_3346412124062405419 = {3585:{None:"k"},3586:{None:"k̄h"},3587:{None:"ḳ̄h"},3588:{None:"kh"},3589:{None:"k̛h"},3590:{None:"ḳh"},3591:{None:"ng"},3592:{None:"c"},3593:{None:"c̄h"},3594:{None:"ch"},3595:{None:"s"},3596:{None:"c̣h"},3597:{None:"ỵ"},3598:{None:"ḍ"},3599:{None:"ṭ"},3600:{None:"ṭ̄h"},3601:{None:"ṯh"},3602:{None:"t̛h"},3603:{None:"ṇ"},3604:{None:"d"},3605:{None:"t"},3606:{None:"t̄h"},3607:{None:"th"},3608:{None:"ṭh"},3609:{None:"n"},3610:{None:"b"},3611:{None:"p"},3612:{None:"p̄h"},3613:{None:"f̄"},3614:{None:"ph"},3615:{None:"f"},3616:{None:"p̣h"},3617:{None:"m"},3618:{None:"y"},3619:{None:"r"},3620:{None:"v"},3621:{None:"l"},3622:{None:"ł"},3623:{None:"w"},3624:{None:"ṣ̄"},3625:{None:"s̛̄"},3626:{None:"s̄"},3627:{None:"h̄"},3628:{None:"ḷ"},3629:{None:"x"},3630:{None:"ḥ"},3631:{None:"ǂ"},3632:{None:"a"},3633:{None:"ạ"},3634:{None:"ā"},3635:{None:"å"},3636:{None:"i"},3637:{None:"ī"},3638:{None:"ụ"},3639:{None:"ụ̄"},3640:{None:"u"},3641:{None:"ū"},3642:{None:"–̥"},3648:{None:"e"},3649:{None:"æ"},3650:{None:"o"},3651:{None:"ı"},3652:{None:"ị"},3653:{None:"ɨ"},3654:{None:"«"},3655:{None:"̆"},3656:{None:"̀"},3657:{None:"̂"},3658:{None:"́"},3659:{None:"̌"},3660:{None:"̒"},3661:{None:"̊"},3662:{None:"~"},3663:{None:"§"},3664:{None:"0"},3665:{None:"1"},3666:{None:"2"},3667:{None:"3"},3668:{None:"4"},3669:{None:"5"},3670:{None:"6"},3671:{None:"7"},3672:{None:"8"},3673:{None:"9"},3674:{None:"ǁ"},3675:{None:"»"}}
