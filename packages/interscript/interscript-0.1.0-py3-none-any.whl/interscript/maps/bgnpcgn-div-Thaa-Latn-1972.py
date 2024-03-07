import interscript
import regex as re
interscript.stdlib.define_map("bgnpcgn-div-Thaa-Latn-1972")
def _stage_main(s):
    s = re.compile("އ(?!=[ަާިީުޫެޭޮޯް])", re.MULTILINE).sub("’", s)
    s = re.compile("ނ(?=[ބދޑގ])", re.MULTILINE).sub("ň", s)
    s = re.compile("ސ(?=[ހ])", re.MULTILINE).sub("s·", s)
    s = re.compile("ނ(?=[ޔ])", re.MULTILINE).sub("n·", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_3798936920671260257)
    s = interscript.functions.compose(s, {})
    return s

interscript.stdlib.add_map_stage("bgnpcgn-div-Thaa-Latn-1972", "main", _stage_main)
_PTREE_3798936920671260257 = {1958:{None:"a"},1959:{None:"ā"},1964:{None:"e"},1965:{None:"ē"},1960:{None:"i"},1961:{None:"ī"},1962:{None:"u"},1963:{None:"ū"},1966:{None:"o"},1967:{None:"ō"},1968:{None:""},1920:{None:"h"},1921:{None:"sh"},1922:{None:"n"},1923:{None:"r"},1924:{None:"b"},1925:{None:"l̦"},1926:{None:"k"},1927:{None:""},1928:{None:"v"},1929:{None:"m"},1930:{None:"f"},1931:{None:"d"},1932:{None:"t"},1933:{None:"l"},1934:{None:"g"},1935:{None:"ny"},1936:{None:"s"},1949:{None:"sh"},1937:{None:"d̦"},1938:{None:"z"},1939:{None:"ț"},1940:{None:"y"},1941:{None:"p"},1942:{None:"j"},1943:{None:"ch"}}
