import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-kat-Geor-Latn-1981")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1190961300543838527)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-kat-Geor-Latn-1981", "main", _stage_main)
_PTREE_1190961300543838527 = {4304:{None:"a"},4305:{None:"b"},4306:{None:"g"},4307:{None:"d"},4308:{None:"e"},4309:{None:"v"},4310:{None:"z"},4337:{None:"ey"},4311:{None:"t’"},4312:{None:"i"},4313:{None:"k’"},4314:{None:"l"},4315:{None:"m"},4316:{None:"n"},4338:{None:"j"},4317:{None:"o"},4318:{None:"p"},4319:{None:"zh"},4320:{None:"r"},4321:{None:"s"},4322:{None:"t"},4323:{None:"u"},4324:{None:"p’"},4325:{None:"k’"},4326:{None:"gh"},4327:{None:"q"},4328:{None:"sh"},4329:{None:"ch’"},4330:{None:"ts’"},4331:{None:"dz"},4332:{None:"ts"},4333:{None:"ch"},4334:{None:"kh"},4340:{None:"q’"},4335:{None:"j"},4336:{None:"h"}}
