import argparse
import json
import re
import functools

LOCALES = {
    "g": {"tla": "ZHS", "suffix": "SC"},
    "t": {"tla": "ZHT", "suffix": "TC"},
    "h": {"tla": "ZHH", "suffix": "HK"},
    "j": {"tla": "JAN", "suffix": "JP"},
    "k": {"tla": "KOR", "suffix": "KR"},
    "v": {"tla": "VIE", "suffix": "VN"},
}

parser = argparse.ArgumentParser()
# subparsers = parser.add_subparsers()
parser.add_argument("dump_newest_only", help="Path to dump_newest_only.txt")
parser.add_argument("gensvg_output", help="Path to gensvg_output.txt")
parser.add_argument("locale", help="g, t, h, j, k, or v")


def build_canonical_name_map(unicode_ranges, name_data_map):
    """E.g. the canonical name of u89d2-g is u2ec6
    Only taking u[a-f0-9]+(-[gthjkv])?\Z into account"""

    def resolve(_hex):
        alias = None
        if _hex not in name_data_map:
            return None
        data = name_data_map[_hex]
        while re.search("99:0:0:0:0:200:200:u[a-f0-9]+(-[gthjkv])?\Z", data):
            alias = data[len("99:0:0:0:0:200:200:") :]
            data = name_data_map[alias]
        return alias

    canonical_name_map = {}

    for [start, last] in unicode_ranges:
        begin = int(start, 16)
        end = int(last, 16)
        for i in range(begin, end + 1):
            _hex = format(i, "X")
            _hex = f"u{_hex.lower()}"

            for locale in list(map(lambda x: f"-{x}", LOCALES)) + [""]:
                resolved = resolve(_hex + locale)
                if resolved:
                    canonical_name_map[_hex + locale] = resolved

    return canonical_name_map


def generateSVGFont(
    prefix, locale, to_encode_list, glyphwiki_to_svg, no_corresponding_unicode_list
):
    font_family = f"{prefix} {LOCALES[locale]['suffix']}"
    f = open(f"{font_family}.svg", "w")
    f.write(
        f"""<font horiz-adv-x="1000">
<font-face font-family="{font_family}" units-per-em="1000" ascent="800" descent="120"/>
<missing-glyph/>
"""
    )

    combined_list = to_encode_list + no_corresponding_unicode_list
    for glyphwiki_code in combined_list:
        f.write(
            f"""<glyph glyph-name="{glyphwiki_code}" d="{glyphwiki_to_svg[glyphwiki_code]}" />\n"""
        )
    f.write("</font>\n")
    f.close()


def process(block, name_data_map, gensvg_output, locale):
    # print(name_data_map["u8e39"])

    prefix = block["prefix"]
    canonical_name_map = build_canonical_name_map(
        block["unicode_ranges"], name_data_map
    )

    characters_to_encode = set()
    no_corresponding_unicode = set()

    for [start, last] in block["unicode_ranges"]:
        begin = int(start, 16)
        end = int(last, 16)
        for i in range(begin, end + 1):
            _hex = format(i, "X")
            _hex = f"u{_hex.lower()}"

            # for each other locale
            for _locale in LOCALES:
                # if this locale has an alias
                if _locale != locale and f"{_hex}-{_locale}" in name_data_map:
                    if f"{_hex}-{_locale}" in canonical_name_map:
                        canonical_name = canonical_name_map[f"{_hex}-{_locale}"]
                        # and the alias is within the same locale or is otherwise
                        # bound to be assigned a unicode code
                        if re.search(f"u[a-f0-9]+(-[{locale}])?\Z", canonical_name):
                            characters_to_encode.add(canonical_name)
                        else:
                            # going to assign it a cid, but no corresponding unicode cp,
                            # only to be used with the locl feature
                            no_corresponding_unicode.add(canonical_name)
                    else:
                        no_corresponding_unicode.add(f"{_hex}-{_locale}")

    for [start, last] in block["unicode_ranges"]:
        begin = int(start, 16)
        end = int(last, 16)
        for i in range(begin, end + 1):
            _hex = format(i, "X")
            _hex = f"u{_hex.lower()}"

            if f"{_hex}-{locale}" in name_data_map:
                # cid_to_glyphwiki_name_map[j] = f"{_hex}-{locale}"
                # j += 1
                characters_to_encode.add(f"{_hex}-{locale}")
            elif _hex in name_data_map:
                # cid_to_glyphwiki_name_map[j] = _hex
                # j += 1
                characters_to_encode.add(_hex)

    to_encode_list = list(characters_to_encode)
    no_corresponding_unicode_list = list(no_corresponding_unicode)

    def comparator(x, y):
        # u89d4-j => 29224
        l = int(re.search("[a-f0-9]+", x).group(), 16)
        r = int(re.search("[a-f0-9]+", y).group(), 16)
        return l - r

    to_encode_list.sort(key=functools.cmp_to_key(comparator))
    no_corresponding_unicode_list.sort(key=functools.cmp_to_key(comparator))

    print(to_encode_list)
    print(no_corresponding_unicode_list)

    glyphwiki_to_svg = {}
    # read the output of gensvg...
    with open(gensvg_output) as f:
        for line in f:
            first_space = line.index(" ")
            letter = line[:first_space]
            if not (
                letter in characters_to_encode or letter in no_corresponding_unicode
            ):
                continue
            svg = line[first_space + 1 :]
            glyphwiki_to_svg[letter] = svg.strip()
    f.close()

    generateSVGFont(
        prefix, locale, to_encode_list, glyphwiki_to_svg, no_corresponding_unicode_list
    )


def cli(args=None):
    args = parser.parse_args()

    # print(args.dump_newest_only)
    with open("./config.json") as f:
        config = json.load(f)

    name_data_map = {}
    i = 0
    with open(args.dump_newest_only) as f:
        for line in f:
            if i < 2:
                i += 1
                continue
            elif (not line) or line[0] == "(":
                continue

            split = list(map(lambda x: x.strip(), line.split("|")))

            name_data_map[split[0]] = split[-1]
    f.close()

    for block in config["blocks"]:
        process(config["blocks"][block], name_data_map, args.gensvg_output, args.locale)
        break