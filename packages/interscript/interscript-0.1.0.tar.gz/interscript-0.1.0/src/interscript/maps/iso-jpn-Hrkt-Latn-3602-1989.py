import interscript
import regex as re
interscript.load_map("mext-jpn-Hrkt-Latn-1954")
interscript.stdlib.define_map("iso-jpn-Hrkt-Latn-3602-1989")
def _stage_main(s):
    s = re.compile("([っッ])•", re.MULTILINE).sub("\\1", s)
    s = interscript.transliterate("mext-jpn-Hrkt-Latn-1954", s, "main")
    s = re.compile("•", re.MULTILINE).sub("", s)
    s = re.compile("'", re.MULTILINE).sub("’", s)
    return s

interscript.stdlib.add_map_stage("iso-jpn-Hrkt-Latn-3602-1989", "main", _stage_main)
