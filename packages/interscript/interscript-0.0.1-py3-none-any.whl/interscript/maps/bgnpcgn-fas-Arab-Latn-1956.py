import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-fas-Arab-Latn-1956")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_752593786099991680)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-fas-Arab-Latn-1956", "main", _stage_main)
_PTREE_752593786099991680 = {1575:{None:"a"},1576:{None:"b"},1662:{None:"p"},1578:{None:"t"},1579:{None:"s"},1580:{None:"j"},1581:{None:"h"},1670:{None:"ch"},1582:{None:"kh"},1583:{None:"d"},1584:{None:"z"},1585:{None:"r"},1586:{None:"z"},1587:{None:"s"},1588:{None:"sh"},1589:{None:"s"},1590:{None:"z"},1591:{None:"t"},1592:{None:"z"},1593:{None:"‘"},1594:{None:"gh"},1601:{None:"f"},1602:{None:"q"},1603:{None:"k"},1604:{None:"l"},1605:{None:"m"},1606:{None:"n"},1607:{None:"h"},1608:{None:"v"},1609:{None:"y"}}
