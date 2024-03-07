import interscript
import regex as re
interscript.stdlib.define_map("bis-ori-Orya-Latn-13194-1991")
def _stage_main(s):
    s = re.compile("ଂ(?=[କଖଗଘଙ])", re.MULTILINE).sub("ṅ", s)
    s = re.compile("ଂ(?=[ଚଛଜଝଞ])", re.MULTILINE).sub("ñ", s)
    s = re.compile("ଂ(?=[ଟଠଡଡ଼ଢଣଢ଼])", re.MULTILINE).sub("ṇ", s)
    s = re.compile("ଂ(?=[ତଥଦଧନ])", re.MULTILINE).sub("n", s)
    s = re.compile("ଂ(?=[ପଫବଭମ])", re.MULTILINE).sub("m", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1181297132528457633)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bis-ori-Orya-Latn-13194-1991", "main", _stage_main)
_PTREE_1181297132528457633 = {2821:{None:"a"},2822:{None:"ā"},2823:{None:"i"},2824:{None:"ī"},2825:{None:"u"},2826:{None:"ū"},2827:{None:"ṛ"},2828:{None:"ḻ"},2831:{None:"ē"},2832:{None:"ai"},2835:{None:"ŏ"},2836:{None:"au"},2837:{None:"k"},2838:{None:"kh"},2839:{None:"g"},2840:{None:"gh"},2841:{None:"ṅ"},2842:{None:"c"},2843:{None:"ch"},2844:{None:"j"},2845:{None:"jh"},2846:{None:"ñ"},2847:{None:"ṭ"},2848:{None:"ṭh"},2849:{None:"ḍ"},2908:{None:"d̂"},2850:{None:"ḍh"},2909:{None:"d̂h"},2851:{None:"ṇ"},2852:{None:"t"},2853:{None:"th"},2854:{None:"d"},2855:{None:"dh"},2856:{None:"n"},2858:{None:"p"},2859:{None:"ph"},2860:{None:"b"},2861:{None:"bh"},2862:{None:"m"},2863:{None:"y"},2911:{None:"ẏ"},2864:{None:"r"},2866:{None:"l"},2867:{None:"ḷ"},2869:{None:"v"},2870:{None:"ś"},2871:{None:"ṣ"},2872:{None:"s"},2873:{None:"h"},2817:{None:"m"},2819:{None:"ḥ"},2818:{None:"ṃ"},2878:{None:"ā"},2879:{None:"i"},2880:{None:"ī"},2881:{None:"u"},2882:{None:"ū"},2883:{None:"ṛ"},2887:{None:"ē"},2888:{None:"ai"},2891:{None:"ŏ"},2892:{None:"au"},2381:{None:""},2893:{None:""},2364:{None:""},2876:{None:""},2404:{None:"."},8205:{None:""},8204:{None:""},2918:{None:"0"},2919:{None:"1"},2920:{None:"2"},2921:{None:"3"},2922:{None:"4"},2923:{None:"5"},2924:{None:"6"},2925:{None:"7"},2926:{None:"8"},2927:{None:"9"}}
