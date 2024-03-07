import interscript
import regex as re
interscript.stdlib.define_map("iso-ori-Orya-Latn-15919-2001")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3986905591181394299)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("iso-ori-Orya-Latn-15919-2001", "main", _stage_main)
_PTREE_3986905591181394299 = {2821:{None:"a"},2822:{None:"ā"},2823:{None:"i"},2824:{None:"ī"},2825:{None:"u"},2826:{None:"ū"},2827:{None:"ṛ"},2912:{None:"ṝ"},2828:{None:"ḷ"},2913:{None:"ḹ"},2831:{None:"e"},2832:{None:"ai"},2835:{None:"o"},2836:{None:"au"},2837:{None:"ka"},2838:{None:"kha"},2839:{None:"ga"},2840:{None:"gha"},2841:{None:"ṅa"},2842:{None:"ca"},2843:{None:"cha"},2844:{None:"ja"},2845:{None:"jha"},2846:{None:"ña"},2847:{None:"ṭa"},2848:{None:"ṭha"},2849:{None:"ḍa"},2908:{None:"ṛa"},2850:{None:"ḍha"},2909:{None:"ṛha"},2851:{None:"ṇa"},2852:{None:"ta"},2853:{None:"tha"},2854:{None:"da"},2855:{None:"dha"},2856:{None:"na"},2858:{None:"pa"},2859:{None:"pha"},2860:{None:"ba"},2861:{None:"bha"},2862:{None:"ma"},2863:{None:"ya",2817:{None:"m̐ya"}},2911:{None:"ẏa",2817:{None:"m̐ẏa"}},2864:{None:"ra",2817:{None:"m̐ra"}},2866:{None:"la",2817:{None:"m̐la"}},2867:{None:"ḷa",2817:{None:"m̐ḷa"}},2869:{None:"va",2817:{None:"m̐va"}},2870:{None:"śa"},2871:{None:"ṣa"},2872:{None:"sa"},2929:{None:"wa"},2873:{None:"ha"},2817:{None:"m̐"},2819:{None:"ḥ"},2818:{None:"ṁ"},2878:{None:"ā"},2879:{None:"i"},2880:{None:"ī"},2881:{None:"u"},2882:{None:"ū"},2883:{None:"ṛ"},2884:{None:"ṝ"},2914:{None:"ḷ"},2915:{None:"ḹ"},2887:{None:"e"},2888:{None:"ai"},2891:{None:"o"},2892:{None:"au"},2877:{None:":’"},2381:{None:""},2893:{None:""},2364:{None:""},2876:{None:""},2404:{None:"."},8205:{None:""},8204:{None:""}}
