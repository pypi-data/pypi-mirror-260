import interscript
import regex as re
interscript.stdlib.define_map("iso-ell-Grek-Latn-843-1997-t1")
def _stage_main(s):
    s = re.compile("(?<=[ΑαΕεΟο])Υ", re.MULTILINE).sub("U", s)
    s = re.compile("(?<=[ΑαΕεΟο])υ", re.MULTILINE).sub("u", s)
    s = re.compile("(?<=[ΑαΕεΟο])ύ", re.MULTILINE).sub("ú", s)
    s = re.compile(";", re.MULTILINE).sub("?", s)
    s = re.compile(";", re.MULTILINE).sub("?", s)
    s = interscript.stdlib.parallel_replace_tree(s, _PTREE_4596182846673929716)
    s = re.compile("(?<=[A-Z])(?:Th|Ch|Ps)", re.MULTILINE).sub(interscript.stdlib.upper, s)
    s = re.compile("(?:Th|Ch|Ps)(?=[A-Z])", re.MULTILINE).sub(interscript.stdlib.upper, s)
    return s

interscript.stdlib.add_map_stage("iso-ell-Grek-Latn-843-1997-t1", "main", _stage_main)
_PTREE_4596182846673929716 = {39:{None:""},902:{None:"Á"},913:{None:"A"},914:{None:"V"},915:{None:"G"},916:{None:"D"},917:{None:"E"},918:{None:"Z"},919:{None:"Ī"},920:{None:"Th"},921:{None:"I"},922:{None:"K"},923:{None:"L"},924:{None:"M"},925:{None:"N"},926:{None:"X"},927:{None:"O"},928:{None:"P"},929:{None:"R"},931:{None:"S"},932:{None:"T"},933:{None:"Y"},934:{None:"F"},935:{None:"Ch"},936:{None:"Ps"},937:{None:"Ō"},904:{None:"É"},905:{None:"Ī́"},906:{None:"Í"},908:{None:"Ó"},910:{None:"Ý"},911:{None:"Ṓ"},938:{None:"Ï"},939:{None:"Ÿ"},940:{None:"á"},945:{None:"a"},946:{None:"v"},947:{None:"g"},948:{None:"d"},949:{None:"e"},950:{None:"z"},951:{None:"ī"},952:{None:"th"},953:{None:"i"},954:{None:"k"},955:{None:"l"},956:{None:"m"},957:{None:"n"},958:{None:"x"},959:{None:"o"},960:{None:"p"},961:{None:"r"},963:{None:"s"},962:{None:"s"},964:{None:"t"},965:{None:"y"},966:{None:"f"},967:{None:"ch"},968:{None:"ps"},969:{None:"ō"},941:{None:"é"},942:{None:"ī́"},943:{None:"í"},972:{None:"ó"},973:{None:"ý"},974:{None:"ṓ"},970:{None:"ï"},971:{None:"ÿ"},912:{None:"ḯ"},944:{None:"ÿ́"},988:{None:"W"},989:{None:"w"},1010:{None:"s"},1017:{None:"S"},903:{None:";"},183:{None:";"}}
