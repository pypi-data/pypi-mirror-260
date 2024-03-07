import interscript
import regex as re
interscript.stdlib.define_map("alalc-kat-Geor-Latn-1997")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1412188978599560833)
    return s

interscript.stdlib.add_map_stage("alalc-kat-Geor-Latn-1997", "main", _stage_main)
_PTREE_1412188978599560833 = {4304:{None:"a"},4305:{None:"b"},4306:{None:"g"},4307:{None:"d"},4308:{None:"e"},4309:{None:"v"},4310:{None:"z"},4337:{None:"ē"},4311:{None:"tʻ"},4312:{None:"i"},4313:{None:"k"},4314:{None:"l"},4315:{None:"m"},4316:{None:"n"},4338:{None:"y"},4317:{None:"o"},4318:{None:"p"},4319:{None:"ž"},4320:{None:"r"},4321:{None:"s"},4322:{None:"t"},4339:{None:"w"},4323:{None:"u"},4324:{None:"pʻ"},4325:{None:"kʻ"},4326:{None:"ġ"},4327:{None:"q"},4328:{None:"š"},4329:{None:"čʻ"},4330:{None:"cʻ"},4331:{None:"ż"},4332:{None:"c"},4333:{None:"č"},4334:{None:"x"},4340:{None:"x̣"},4335:{None:"j"},4336:{None:"h"},4341:{None:"ō"},4342:{None:"f"},4343:{None:"ĕ"},4344:{None:"ʻ"}}
