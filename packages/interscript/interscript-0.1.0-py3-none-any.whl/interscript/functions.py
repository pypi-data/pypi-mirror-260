import regex as re
import unicodedata

def title_case(output, opts):
    if 'word_separator' not in opts:
        opts['word_separator'] = " "
    output = re.sub(r'(^|\n)(.)', lambda a: a.group(0).upper(), output)
    if opts['word_separator'] != "":
        sep = re.escape(opts['word_separator'])
        output = re.sub(sep + r'(.)', lambda a: a.group(0).upper(), output)
    return output

def downcase(output, opts):
    return output.lower()

def compose(output, opts):
    return unicodedata.normalize("NFC", output)

def decompose(output, opts):
    return unicodedata.normalize("NFD", output)

def separate(output, opts):
    if 'separator' not in opts:
        opts['separator'] = " "
    return opts['separator'].join(list(output))
