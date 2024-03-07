import interscript
import regex as re
interscript.stdlib.define_map("alalc-ell-Grek-Latn-1997")
interscript.stdlib.add_map_alias("alalc-ell-Grek-Latn-1997", "greek_upper", "Ά")
interscript.stdlib.add_map_alias_re("alalc-ell-Grek-Latn-1997", "greek_upper", "[ΆΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΈΉΊΌΏΪΫ]")
def _stage_main(s):
    s = re.compile("(?<=[ΑαΕεΟοΗηΩω])Υ", re.MULTILINE).sub("U", s)
    s = re.compile("(?<=[ΑαΕεΟοΗηΩω])υ", re.MULTILINE).sub("u", s)
    s = re.compile("(?<=[ΑαΕεΟοΗηΩω])ύ", re.MULTILINE).sub("u", s)
    s = re.compile("Υ(?=[Ιιί])", re.MULTILINE).sub("U", s)
    s = re.compile("υ(?=[Ιιί])", re.MULTILINE).sub("u", s)
    s = re.compile("Γ(?=[γΓκΚξΞχΧ])", re.MULTILINE).sub("N", s)
    s = re.compile("γ(?=[γΓκΚξΞχΧ])", re.MULTILINE).sub("n", s)
    s = re.compile("(?<="+interscript.stdlib.aliases["boundary"]+")ΝΤ", re.MULTILINE).sub("Ḏ", s)
    s = re.compile("(?<="+interscript.stdlib.aliases["boundary"]+")Ντ", re.MULTILINE).sub("Ḏ", s)
    s = re.compile("(?<="+interscript.stdlib.aliases["boundary"]+")ντ", re.MULTILINE).sub("ḏ", s)
    s = re.compile("(?<="+interscript.stdlib.aliases["boundary"]+")ΜΠ", re.MULTILINE).sub("B", s)
    s = re.compile("(?<="+interscript.stdlib.aliases["boundary"]+")Μπ", re.MULTILINE).sub("B", s)
    s = re.compile("(?<="+interscript.stdlib.aliases["boundary"]+")μπ", re.MULTILINE).sub("b", s)
    s = re.compile(";", re.MULTILINE).sub("?", s)
    s = re.compile(";", re.MULTILINE).sub("?", s)
    s = interscript.stdlib.parallel_regexp_gsub(s, *_PRE_2441572244976208456)
    return s

interscript.stdlib.add_map_stage("alalc-ell-Grek-Latn-1997", "main", _stage_main)
_PRE_2441572244976208456 = ["(?P<_0>Θ(?=[ΆΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΈΉΊΌΏΪΫ]))|(?P<_1>(?<=[ΆΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΈΉΊΌΏΪΫ])Θ)|(?P<_2>Φ(?=[ΆΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΈΉΊΌΏΪΫ]))|(?P<_3>(?<=[ΆΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΈΉΊΌΏΪΫ])Φ)|(?P<_4>Χ(?=[ΆΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΈΉΊΌΏΪΫ]))|(?P<_5>(?<=[ΆΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΈΉΊΌΏΪΫ])Χ)|(?P<_6>Ψ(?=[ΆΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΈΉΊΌΏΪΫ]))|(?P<_7>(?<=[ΆΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΈΉΊΌΏΪΫ])Ψ)|(?P<_8>')|(?P<_9>Ά)|(?P<_10>Α)|(?P<_11>Β)|(?P<_12>Γ)|(?P<_13>Δ)|(?P<_14>Ε)|(?P<_15>Ζ)|(?P<_16>Η)|(?P<_17>Θ)|(?P<_18>Ι)|(?P<_19>Κ)|(?P<_20>Λ)|(?P<_21>Μ)|(?P<_22>Ν)|(?P<_23>Ξ)|(?P<_24>Ο)|(?P<_25>Π)|(?P<_26>Ρ)|(?P<_27>Σ)|(?P<_28>Τ)|(?P<_29>Υ)|(?P<_30>Φ)|(?P<_31>Χ)|(?P<_32>Ψ)|(?P<_33>Ω)|(?P<_34>Έ)|(?P<_35>Ή)|(?P<_36>Ί)|(?P<_37>Ό)|(?P<_38>Ύ)|(?P<_39>Ώ)|(?P<_40>Ϊ)|(?P<_41>Ϋ)|(?P<_42>ά)|(?P<_43>α)|(?P<_44>β)|(?P<_45>γ)|(?P<_46>δ)|(?P<_47>ε)|(?P<_48>ζ)|(?P<_49>η)|(?P<_50>θ)|(?P<_51>ι)|(?P<_52>κ)|(?P<_53>λ)|(?P<_54>μ)|(?P<_55>ν)|(?P<_56>ξ)|(?P<_57>ο)|(?P<_58>π)|(?P<_59>ρ)|(?P<_60>σ)|(?P<_61>ς)|(?P<_62>τ)|(?P<_63>υ)|(?P<_64>φ)|(?P<_65>χ)|(?P<_66>ψ)|(?P<_67>ω)|(?P<_68>έ)|(?P<_69>ή)|(?P<_70>ί)|(?P<_71>ό)|(?P<_72>ύ)|(?P<_73>ώ)|(?P<_74>ϊ)|(?P<_75>ϋ)|(?P<_76>ΐ)|(?P<_77>ΰ)|(?P<_78>·)|(?P<_79>·)", ["TH","TH","PH","PH","CH","CH","PS","PS","","A","A","V","G","D","E","Z","Ē","Th","I","K","L","M","N","X","O","P","R","S","T","Y","Ph","Ch","Ps","Ō","E","Ē","I","O","Y","Ō","I","Y","a","a","v","g","d","e","z","ē","th","i","k","l","m","n","x","o","p","r","s","s","t","y","ph","ch","ps","ō","e","ē","i","o","y","ō","i","y","i","y",";",";"]]
