import interscript
import regex as re
interscript.load_map("un-hin-Deva-Latn-2016")
interscript.stdlib.define_map("un-mar-Deva-Latn-2016")
def _stage_main(s):
    s = interscript.transliterate("un-hin-Deva-Latn-2016", s, "main")
    s = re.compile("(?<=)U+0939(?="+interscript.stdlib.aliases["boundary"]+")", re.MULTILINE).sub("h", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4277993349087493236)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("un-mar-Deva-Latn-2016", "main", _stage_main)
_PTREE_4277993349087493236 = {2355:{None:"ḷa"},2317:{None:"ă"},2353:{None:"r"},2309:{2367:{None:"i"},2368:{None:"ī"},2369:{None:"u"},2370:{None:"ū"},2375:{None:"e"},2376:{None:"ai"}},2418:{None:"ê"},2321:{None:"ô"}}
