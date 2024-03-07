import interscript
import regex as re
interscript.load_map("iso-ben-Beng-Latn-15919-2001")
interscript.stdlib.define_map("iso-asm-Beng-Latn-15919-2001")
def _stage_main(s):
    s = interscript.transliterate("iso-ben-Beng-Latn-15919-2001", s, "main")
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4609760250285123348)
    return s

interscript.stdlib.add_map_stage("iso-asm-Beng-Latn-15919-2001", "main", _stage_main)
_PTREE_4609760250285123348 = {2544:{None:"va"},2545:{None:"ra"}}
