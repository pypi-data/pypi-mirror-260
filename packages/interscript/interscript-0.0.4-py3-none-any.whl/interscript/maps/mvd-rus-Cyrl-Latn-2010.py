import interscript
import regex as re
interscript.load_map("mvd-rus-Cyrl-Latn-2008")
interscript.stdlib.define_map("mvd-rus-Cyrl-Latn-2010")
def _stage_main(s):
    s = interscript.transliterate("mvd-rus-Cyrl-Latn-2008", s, "translit")
    s = re.compile("́", re.MULTILINE).sub("", s)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("mvd-rus-Cyrl-Latn-2010", "main", _stage_main)
