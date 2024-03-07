import regex as re

aliases = {
    "any_character": '.',
    "none": "",
    "space": " ",
    "whitespace": "[\\b \\t\\0\\r\\n]",
    "boundary": "\\b",
    "non_word_boundary": "\\B",
    "word": "[a-zA-Z0-9_]",
    "not_word": "[^a-zA-Z0-9_]",
    "alpha": "[a-zA-Z]",
    "not_alpha": "[^a-zA-Z]",
    "digit": "\\d",
    "not_digit": "\\D",
    "line_start": "^",
    "line_end": "$",
    "string_start": "\\A",
    "string_end": "\\z"
}

available_functions = [
    "title_case",
    "downcase",
    "compose",
    "decompose",
    "separate",
]

maps = {}

def define_map(map):
    maps[map] = {
        "name": map,
        "aliases": {},
        "aliases_re": {},
        "cache": {},
        "stages": {},
    }

def get_alias(map, alias):
    return maps[map]["aliases"][alias];

def get_alias_re(map, alias):
    return maps[map]["aliases_re"][alias];

def add_map_stage(map, stage, fun):
    maps[map]["stages"][stage] = fun

def add_map_alias(map, alias, aliased):
    maps[map]["aliases"][alias] = aliased

def add_map_alias_re(map, alias, aliased):
    maps[map]["aliases_re"][alias] = aliased


def parallel_replace_tree(str, tree):
    newstr = ""
    len_str = len(str)
    i = 0
    while i < len_str:
        c = str[i]

        sub = ""
        branch = tree
        match, repl = None, None

        j = 0
        while j < len_str - i:
            cc = str[i + j]
            if ord(cc) in branch:
                branch = branch[ord(cc)]
                sub += cc
                if None in branch:  # Check for None to find the terminal node
                    match = sub
                    repl = branch[None]
                j += 1
            else:
                break

        if match:
            i += len(match)
            newstr += repl
        else:
            newstr += c
            i += 1

    return newstr



def parallel_regexp_gsub(s, subs_regexp, subs_hash):
    # Compile the regular expression from the data[0] pattern
    subs_regexp = re.compile(subs_regexp, re.MULTILINE)

    # Define the replacement function
    def replacement(match):
        # Iterate through the named groups to find the matched one
        for name, value in match.groupdict().items():
            if value is not None:
                # Extract the numeric part of the name and convert it to an integer
                idx = int(name[1:])  # Assuming names are like "_1", "_2", etc.
                # Return the corresponding replacement from data[1]
                return subs_hash[idx]
        # If no named group was matched (which shouldn't happen), return the whole match
        return match.group(0)

    # Perform the substitution and return the result
    return subs_regexp.sub(replacement, s)

def upper(match):
    return match.group().upper()

def lower(match):
    return match.group().lower()
