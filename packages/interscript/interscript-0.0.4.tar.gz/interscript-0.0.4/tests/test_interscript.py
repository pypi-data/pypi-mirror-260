import interscript

def assert_transliteration(map, input, output):
    interscript.load_map(map)
    result = interscript.transliterate(map, input)
    assert result == output

def test_can_transliterate():
    assert_transliteration('bgnpcgn-ukr-Cyrl-Latn-2019', 'Антон', 'Anton')

def test_can_transliterate_maps_requiring_libraries():
    assert_transliteration('bgnpcgn-deu-Latn-Latn-2000', 'Tschüß!', 'Tschueß!')
