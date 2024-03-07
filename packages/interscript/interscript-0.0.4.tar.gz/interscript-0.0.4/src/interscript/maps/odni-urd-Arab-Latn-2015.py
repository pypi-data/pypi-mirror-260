import interscript
import regex as re
interscript.stdlib.define_map("odni-urd-Arab-Latn-2015")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4290943649338950483)
    return s

interscript.stdlib.add_map_stage("odni-urd-Arab-Latn-2015", "main", _stage_main)
_PTREE_4290943649338950483 = {1570:{None:"a"},1575:{None:"a",1616:{None:"i"}},1740:{None:"i"},1608:{None:"i",1648:{None:"a"}},1746:{None:"e"},1616:{None:"e"},1593:{None:"e",1616:{None:"i"}},1729:{None:"ah",1616:{None:"o"}},1581:{None:"ha"},1648:{None:"a"},1615:{None:"i"},1747:{None:"i"},1730:{None:"-e"},1572:{None:"au"},1705:{None:"k"},1602:{None:"q"},1582:{None:"kh"},1711:{None:"g"},1594:{None:"gh"},1670:{None:"ch"},1580:{None:"j"},1586:{None:"z"},1584:{None:"z"},1590:{None:"z"},1592:{None:"z"},1688:{None:"zh"},1657:{None:"t"},1672:{None:"d"},1583:{None:"d"},1681:{None:"r"},1578:{None:"t"},1591:{None:"t"},1606:{None:"n"},1722:{None:"n"},1662:{None:"p"},1601:{None:"f"},1576:{None:"b"},1605:{None:"m"},1585:{None:"r"},1604:{None:"l"},1588:{None:"sh"},1587:{None:"s"},1579:{None:"s"},1589:{None:"s"},1569:{None:""},1726:{None:"s"},1611:{None:"n"},1614:{None:"n"},1618:{None:""},1617:{None:""}}
