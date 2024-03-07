import interscript
import regex as re
interscript.stdlib.define_map("din-kat-Geor-Latn-32707-2010")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1352607572037391602)
    return s

interscript.stdlib.add_map_stage("din-kat-Geor-Latn-32707-2010", "main", _stage_main)
_PTREE_1352607572037391602 = {4304:{None:"a"},4305:{None:"b"},4306:{None:"g"},4307:{None:"d"},4308:{None:"e"},4309:{None:"v"},4310:{None:"z"},4337:{None:"ê"},4311:{None:"t̕"},4312:{None:"i"},4313:{None:"k"},4314:{None:"l"},4315:{None:"m"},4316:{None:"n"},4338:{None:"y"},4317:{None:"o"},4318:{None:"p"},4319:{None:"ž"},4320:{None:"r"},4321:{None:"s"},4322:{None:"t"},4339:{None:"w"},4323:{None:"u"},4324:{None:"p̕"},4325:{None:"k̕"},4326:{None:"ġ"},4327:{None:"q"},4328:{None:"š"},4329:{None:"č̕"},4330:{None:"c̕"},4331:{None:"j"},4332:{None:"c"},4333:{None:"č"},4334:{None:"x"},4340:{None:"q̕"},4335:{None:"ǰ"},4336:{None:"h"},4341:{None:"ô"},4342:{None:"f"},4343:{None:"ẹ"},4344:{None:"ʼ"}}
