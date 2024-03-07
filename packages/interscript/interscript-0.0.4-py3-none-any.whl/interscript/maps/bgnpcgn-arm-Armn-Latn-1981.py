import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-arm-Armn-Latn-1981")
def _stage_main(s):
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_581906204803071130)
    return s

interscript.stdlib.add_map_stage("bgnpcgn-arm-Armn-Latn-1981", "main", _stage_main)
_PTREE_581906204803071130 = {1329:{None:"A"},1330:{None:"B"},1331:{None:"G"},1332:{None:"D"},1333:{None:"Ye"},1334:{None:"Z"},1335:{None:"E"},1336:{None:"Y"},1337:{None:"T’"},1338:{None:"Zh"},1339:{None:"I"},1340:{None:"L"},1341:{None:"Kh"},1342:{None:"Ts"},1343:{None:"K"},1344:{None:"H"},1345:{None:"Dz"},1346:{None:"Gh"},1347:{None:"Ch"},1348:{None:"M"},1349:{None:"Y"},1350:{None:"N"},1351:{None:"Sh"},1352:{None:"O",1362:{None:"U"},1410:{None:"U"}},1353:{None:"u'Ch’'"},1354:{None:"P"},1355:{None:"J"},1356:{None:"Rr"},1357:{None:"S"},1358:{None:"V"},1359:{None:"T"},1360:{None:"R"},1361:{None:"Ts’"},1363:{None:"P’"},1364:{None:"K’"},1365:{None:"O"},1366:{None:"F"},1377:{None:"a"},1378:{None:"b"},1379:{None:"g"},1380:{None:"d"},1381:{None:"e"},1382:{None:"z"},1383:{None:"e"},1384:{None:"y"},1385:{None:"u't’'"},1386:{None:"zh"},1387:{None:"i"},1388:{None:"l"},1389:{None:"kh"},1390:{None:"ts"},1391:{None:"k"},1392:{None:"h"},1393:{None:"dz"},1394:{None:"gh"},1395:{None:"ch"},1396:{None:"m"},1397:{None:"y"},1398:{None:"n"},1399:{None:"sh"},1400:{None:"o",1410:{None:"u"}},1401:{None:"ch’"},1402:{None:"p"},1403:{None:"j"},1404:{None:"rr"},1405:{None:"s"},1406:{None:"v"},1407:{None:"t"},1408:{None:"r"},1409:{None:"ts’"},1411:{None:"p’"},1412:{None:"k’"},1413:{None:"o"},1414:{None:"f"},1415:{None:"ev"}}
