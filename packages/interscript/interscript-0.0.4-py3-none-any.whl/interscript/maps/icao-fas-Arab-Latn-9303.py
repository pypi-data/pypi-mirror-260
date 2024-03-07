import interscript
import regex as re
interscript.stdlib.define_map("icao-fas-Arab-Latn-9303")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_1834347731906618414)
    return s

interscript.stdlib.add_map_stage("icao-fas-Arab-Latn-9303", "main", _stage_main)
_PTREE_1834347731906618414 = {39:{None:""},1569:{None:"XE"},1570:{None:"XAA"},1571:{None:"XAE"},1572:{None:"U"},1573:{None:"I"},1574:{None:"XI"},1575:{None:"A"},1576:{None:"B"},1577:{None:"P"},1578:{None:"T"},1579:{None:"XTH"},1580:{None:"J"},1581:{None:"XH"},1582:{None:"XKH"},1583:{None:"D"},1584:{None:"XDH"},1585:{None:"R"},1586:{None:"Z"},1587:{None:"S"},1588:{None:"XSH"},1589:{None:"XSS"},1590:{None:"XDZ"},1591:{None:"XTT"},1592:{None:"XZZ"},1593:{None:"E"},1594:{None:"G"},1601:{None:"F"},1602:{None:"Q"},1603:{None:"K"},1604:{None:"L"},1605:{None:"M"},1606:{None:"N"},1607:{None:"H"},1608:{None:"W"},1609:{None:"XAY"},1610:{None:"Y"},1611:{None:"F"},1612:{None:"N"},1613:{None:"K"},1614:{None:"A"},1615:{None:"U"},1616:{None:"I"},1618:{None:"O"},1648:{None:""},1649:{None:"XXA"},1657:{None:"XXT"},1660:{None:"XRT"},1662:{None:"P"},1665:{None:"XKE"},1669:{None:"XXH"},1670:{None:"XC"},1672:{None:"XXD"},1673:{None:"XDR"},1681:{None:"XXR"},1683:{None:"XRR"},1686:{None:"XRX"},1688:{None:"XJ"},1690:{None:"XXS"},1705:{None:"XKK"},1707:{None:"XXK"},1709:{None:"XNG"},1711:{None:"XGG"},1722:{None:"XNN"},1724:{None:"XXN"},1726:{None:"XDO"},1728:{None:"XYH"},1729:{None:"XXG"},1730:{None:"XGE"},1731:{None:"XTG"},1740:{None:"XYA"},1741:{None:"XXY"},1744:{None:"Y"},1746:{None:"XYB"},1747:{None:"XBE"}}
