import interscript
import regex as re
interscript.stdlib.define_map("alalc-kat-Geok-Latn-1997")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_2053127662427638207)
    return s

interscript.stdlib.add_map_stage("alalc-kat-Geok-Latn-1997", "main", _stage_main)
_PTREE_2053127662427638207 = {4256:{None:"A"},4257:{None:"B"},4258:{None:"G"},4259:{None:"D"},4260:{None:"E"},4261:{None:"V"},4262:{None:"Z"},4263:{None:"Tʻ"},4264:{None:"I"},4265:{None:"K"},4266:{None:"L"},4267:{None:"M"},4268:{None:"N"},4269:{None:"O"},4270:{None:"P"},4271:{None:"Ž"},4272:{None:"R"},4273:{None:"S"},4274:{None:"T"},4275:{None:"U"},4276:{None:"Pʻ"},4277:{None:"Kʻ"},4278:{None:"Ġ"},4279:{None:"Q"},4280:{None:"Š"},4281:{None:"Čʻ"},4282:{None:"Cʻ"},4283:{None:"Ż"},4284:{None:"C"},4285:{None:"Č"},4286:{None:"X"},4287:{None:"J"},4288:{None:"H"},4289:{None:"Ē"},4290:{None:"Y"},4291:{None:"W"},4292:{None:"X̣"},4293:{None:"Ō"},11520:{None:"a"},11521:{None:"b"},11522:{None:"g"},11523:{None:"d"},11524:{None:"e"},11525:{None:"v"},11526:{None:"z"},11527:{None:"tʻ"},11528:{None:"i"},11529:{None:"k"},11530:{None:"l"},11531:{None:"m"},11532:{None:"n"},11533:{None:"o"},11534:{None:"p"},11535:{None:"ž"},11536:{None:"r"},11537:{None:"s"},11538:{None:"t"},11539:{None:"u"},11540:{None:"pʻ"},11541:{None:"kʻ"},11542:{None:"ġ"},11543:{None:"q"},11544:{None:"š"},11545:{None:"čʻ"},11546:{None:"cʻ"},11547:{None:"ż"},11548:{None:"c"},11549:{None:"č"},11550:{None:"x"},11551:{None:"j"},11552:{None:"h"},11553:{None:"ē"},11554:{None:"y"},11555:{None:"w"},11556:{None:"x̣"},11557:{None:"ō"}}
