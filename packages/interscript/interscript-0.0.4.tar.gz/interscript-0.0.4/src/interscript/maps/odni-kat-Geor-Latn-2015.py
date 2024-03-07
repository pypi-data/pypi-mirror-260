import interscript
import regex as re
interscript.stdlib.define_map("odni-kat-Geor-Latn-2015")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3924595623280772356)
    return s

interscript.stdlib.add_map_stage("odni-kat-Geor-Latn-2015", "main", _stage_main)
_PTREE_3924595623280772356 = {4304:{None:"a"},4305:{None:"b"},4306:{None:"g"},4307:{None:"d"},4308:{None:"e"},4309:{None:"v"},4310:{None:"z"},4311:{None:"t"},4312:{None:"i"},4313:{None:"k"},4314:{None:"l"},4315:{None:"m"},4316:{None:"n"},4317:{None:"o"},4318:{None:"p"},4319:{None:"zh"},4320:{None:"r"},4321:{None:"s"},4322:{None:"t"},4323:{None:"u"},4324:{None:"p"},4325:{None:"k"},4326:{None:"gh"},4327:{None:"q"},4328:{None:"sh"},4329:{None:"ch"},4330:{None:"ts"},4331:{None:"dz"},4332:{None:"ts"},4333:{None:"ch"},4334:{None:"kh"},4335:{None:"j"},4336:{None:"h"}}
