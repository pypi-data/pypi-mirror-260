import interscript
import regex as re
interscript.stdlib.define_map("var-Cyrl")
interscript.stdlib.add_map_alias("var-Cyrl", "bel_consonant", "Б")
interscript.stdlib.add_map_alias_re("var-Cyrl", "bel_consonant", "[БбВвГгДдЖжЗзЙйКкЛлМмНнПпРрСсТтФфХхЦцЧчШш]")
interscript.stdlib.add_map_alias("var-Cyrl", "cyrl_upper", "A")
interscript.stdlib.add_map_alias_re("var-Cyrl", "cyrl_upper", "[AБBГДЕЁЖЗИЙКЛМНОПРСТУЎФХЦЧШЩЪЫЬЭЮЯІ]")
