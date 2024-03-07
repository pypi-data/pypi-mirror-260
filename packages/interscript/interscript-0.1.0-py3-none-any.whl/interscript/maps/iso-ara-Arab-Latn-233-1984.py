import interscript
import regex as re
interscript.stdlib.define_map("iso-ara-Arab-Latn-233-1984")
def _stage_main(s):
    s = interscript.stdlib.parallel_regexp_gsub(s, *_PRE_835510530453525632)
    s = re.compile("(?<="+interscript.stdlib.aliases["boundary"]+")(?<!"+interscript.stdlib.aliases["boundary"]+"[‘’'])[a-￿]", re.MULTILINE).sub(interscript.stdlib.upper, s)
    s = re.compile("\\ At\\ T", re.MULTILINE).sub(" at T", s)
    s = re.compile("\\ Aṯ\\ Ṯ", re.MULTILINE).sub(" aṯ Ṯ", s)
    s = re.compile("\\ Ad\\ D", re.MULTILINE).sub(" ad D", s)
    s = re.compile("\\ Aḏ\\ Ḏ", re.MULTILINE).sub(" aḏ Ḏ", s)
    s = re.compile("\\ Ar\\ R", re.MULTILINE).sub(" ar R", s)
    s = re.compile("\\ Az\\ Z", re.MULTILINE).sub(" az Z", s)
    s = re.compile("\\ As\\ S", re.MULTILINE).sub(" as S", s)
    s = re.compile("\\ Aš\\ Š", re.MULTILINE).sub(" aš Š", s)
    s = re.compile("\\ Aṣ\\ Ṣ", re.MULTILINE).sub(" aṣ Ṣ", s)
    s = re.compile("\\ Aḍ\\ Ḍ", re.MULTILINE).sub(" aḍ Ḍ", s)
    s = re.compile("\\ Aṭ\\ Ṭ", re.MULTILINE).sub(" aṭ Ṭ", s)
    s = re.compile("\\ Aẓ\\ Ẓ", re.MULTILINE).sub(" aẓ Ẓ", s)
    s = re.compile("\\ Al\\ L", re.MULTILINE).sub(" al L", s)
    s = re.compile("\\ An\\ N", re.MULTILINE).sub(" an N", s)
    s = re.compile("\\ Al\\ ", re.MULTILINE).sub(" al ", s)
    return s

interscript.stdlib.add_map_stage("iso-ara-Arab-Latn-233-1984", "main", _stage_main)
_PRE_835510530453525632 = ["(?P<_0>"+interscript.stdlib.aliases["boundary"]+"التّ?)|(?P<_1>"+interscript.stdlib.aliases["boundary"]+"الثّ?)|(?P<_2>"+interscript.stdlib.aliases["boundary"]+"الدّ?)|(?P<_3>"+interscript.stdlib.aliases["boundary"]+"الذّ?)|(?P<_4>"+interscript.stdlib.aliases["boundary"]+"الرّ?)|(?P<_5>"+interscript.stdlib.aliases["boundary"]+"الزّ?)|(?P<_6>"+interscript.stdlib.aliases["boundary"]+"السّ?)|(?P<_7>"+interscript.stdlib.aliases["boundary"]+"الشّ?)|(?P<_8>"+interscript.stdlib.aliases["boundary"]+"الصّ?)|(?P<_9>"+interscript.stdlib.aliases["boundary"]+"الضّ?)|(?P<_10>"+interscript.stdlib.aliases["boundary"]+"الطّ?)|(?P<_11>"+interscript.stdlib.aliases["boundary"]+"الظّ?)|(?P<_12>"+interscript.stdlib.aliases["boundary"]+"اللّ?)|(?P<_13>"+interscript.stdlib.aliases["boundary"]+"النّ?)|(?P<_14>ِيَّ)|(?P<_15>عُو)|(?P<_16>ِي(?=[َُ]))|(?P<_17>َوْ)|(?P<_18>َيْ)|(?P<_19>"+interscript.stdlib.aliases["boundary"]+"ال)|(?P<_20>َ(?=ة))|(?P<_21>عَ)|(?P<_22>عِ)|(?P<_23>عُ)|(?P<_24>ِي)|(?P<_25>َا)|(?P<_26>َى)|(?P<_27>ُو)|(?P<_28>بّ)|(?P<_29>تّ)|(?P<_30>ثّ)|(?P<_31>جّ)|(?P<_32>حّ)|(?P<_33>خّ)|(?P<_34>دّ)|(?P<_35>ذّ)|(?P<_36>رّ)|(?P<_37>زّ)|(?P<_38>سّ)|(?P<_39>شّ)|(?P<_40>صّ)|(?P<_41>ضّ)|(?P<_42>طّ)|(?P<_43>ظّ)|(?P<_44>غّ)|(?P<_45>فّ)|(?P<_46>قّ)|(?P<_47>كّ)|(?P<_48>لّ)|(?P<_49>مّ)|(?P<_50>نّ)|(?P<_51>هّ)|(?P<_52>وّ)|(?P<_53>يّ)|(?P<_54>َ)|(?P<_55>ِ)|(?P<_56>ُ)|(?P<_57>ْ)|(?P<_58>ة)|(?P<_59>آ)|(?P<_60>ا)|(?P<_61>ى)|(?P<_62>ئ)|(?P<_63>ء)|(?P<_64>أ)|(?P<_65>ب)|(?P<_66>ﺑ)|(?P<_67>ﺒ)|(?P<_68>ﺐ)|(?P<_69>ت)|(?P<_70>ﺗ)|(?P<_71>ﺘ)|(?P<_72>ﺖ)|(?P<_73>ث)|(?P<_74>ﺛ)|(?P<_75>ﺜ)|(?P<_76>ﺚ)|(?P<_77>ج)|(?P<_78>ﺟ)|(?P<_79>ﺠ)|(?P<_80>ﺞ)|(?P<_81>ح)|(?P<_82>ﺣ)|(?P<_83>ﺤ)|(?P<_84>ﺢ)|(?P<_85>خ)|(?P<_86>ﺧ)|(?P<_87>ﺨ)|(?P<_88>ﺦ)|(?P<_89>د)|(?P<_90>ﺪ)|(?P<_91>ذ)|(?P<_92>ﺬ)|(?P<_93>ر)|(?P<_94>ﺮ)|(?P<_95>ز)|(?P<_96>ﺰ)|(?P<_97>س)|(?P<_98>ﺳ)|(?P<_99>ﺴ)|(?P<_100>ﺲ)|(?P<_101>ش)|(?P<_102>ﺷ)|(?P<_103>ﺸ)|(?P<_104>ﺶ)|(?P<_105>ص)|(?P<_106>ﺻ)|(?P<_107>ﺼ)|(?P<_108>ﺺ)|(?P<_109>ض)|(?P<_110>ﺿ)|(?P<_111>ﻀ)|(?P<_112>ﺾ)|(?P<_113>ط)|(?P<_114>ﻃ)|(?P<_115>ﻄ)|(?P<_116>ﻂ)|(?P<_117>ظ)|(?P<_118>ﻇ)|(?P<_119>ﻈ)|(?P<_120>ﻆ)|(?P<_121>ع)|(?P<_122>ﻋ)|(?P<_123>ﻌ)|(?P<_124>ﻊ)|(?P<_125>غ)|(?P<_126>ﻏ)|(?P<_127>ﻐ)|(?P<_128>ﻎ)|(?P<_129>ف)|(?P<_130>ﻓ)|(?P<_131>ﻔ)|(?P<_132>ﻒ)|(?P<_133>ق)|(?P<_134>ﻗ)|(?P<_135>ﻘ)|(?P<_136>ﻖ)|(?P<_137>ك)|(?P<_138>ﻛ)|(?P<_139>ﻜ)|(?P<_140>ﻚ)|(?P<_141>ل)|(?P<_142>ﻟ)|(?P<_143>ﻠ)|(?P<_144>ﻞ)|(?P<_145>م)|(?P<_146>ﻣ)|(?P<_147>ﻤ)|(?P<_148>ﻢ)|(?P<_149>ن)|(?P<_150>ﻧ)|(?P<_151>ﻨ)|(?P<_152>ﻦ)|(?P<_153>ه)|(?P<_154>ﻫ)|(?P<_155>ﻬ)|(?P<_156>ﻪ)|(?P<_157>و)|(?P<_158>ﻮ)|(?P<_159>ي)|(?P<_160>ﻳ)|(?P<_161>ﻴ)|(?P<_162>ﻱ)", ["at t","aṯ ṯ","ad d","aḏ ḏ","ar r","az z","as s","aš š","aṣ ṣ","aḍ ḍ","aṭ ṭ","aẓ ẓ","al l","an n","iy","‘ū","iy","aw","ay","al ","","‘a","‘i","‘ū","iy","a’","aỳ","uw","bb","tt","ṯṯ","ǧǧ","ḥḥ","ẖẖ","dd","ḏḏ","rr","zz","ss","šš","ṣṣ","ḍḍ","ṭṭ","ẓẓ","ġġ","ff","qq","kk","ll","mm","nn","hh","ww","yy","a","i","u","","aẗ","’â","â","ỳ","'","’","a","b","b","b","b","t","t","t","t","ṯ","ṯ","ṯ","ṯ","ǧ","ǧ","ǧ","ǧ","ḥ","ḥ","ḥ","ḥ","ẖ","ẖ","ẖ","ẖ","d","d","ḏ","ḏ","r","r","z","z","s","s","s","s","š","š","š","š","ṣ","ṣ","ṣ","ṣ","ḍ","ḍ","ḍ","ḍ","ṭ","ṭ","ṭ","ṭ","ẓ","ẓ","ẓ","ẓ","‘","‘","‘","‘","ġ","ġ","ġ","ġ","f","f","f","f","q","q","q","q","k","k","k","k","l","l","l","l","m","m","m","m","n","n","n","n","h","h","h","h","w","w","y","y","y","y"]]
