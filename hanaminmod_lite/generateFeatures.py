from .constants import *
import re


def generateFeatures(
    prefix,
    locale,
    to_encode_list,
    no_corresponding_unicode_list,
    canonical_name_map,
):
    font_family = f"{prefix}{LOCALES[locale]['suffix']}"
    f = open(f"{font_family}.features", "w")
    f.write("languagesystem DFLT dflt;\n")
    for _locale in LOCALES:
        f.write(f"languagesystem hani {LOCALES[_locale]['tla']};\n")

    # basically the inverse of the cidmap
    glyphwiki_to_cid = {}

    combined_list = to_encode_list + no_corresponding_unicode_list

    for i in range(len(combined_list)):
        glyphwiki_to_cid[combined_list[i]] = i + 1

    substitution_rules = {}  # map of {g,t,h,j,k,v} to pairs (2-tuples) of CIDs

    for _locale in LOCALES:
        if _locale != locale:
            substitution_rules[_locale] = []

    for glyphwiki_code in to_encode_list:
        # extract the hex code
        _hex = re.search("[a-f0-9]+", glyphwiki_code).group()

        # for each possible variant
        for _locale in LOCALES:
            if _locale != locale:
                other_locale = f"u{_hex}-{_locale}"

                # resolve its canonical name if it exists
                resolved = (
                    canonical_name_map[other_locale]
                    if other_locale in canonical_name_map
                    else other_locale
                )

                # if its canonical name is not going to be accessible in the resulting font, continue
                if resolved not in glyphwiki_to_cid or glyphwiki_code == resolved:
                    continue

                substitution_rules[_locale].append(
                    (glyphwiki_to_cid[glyphwiki_code], glyphwiki_to_cid[resolved])
                )

    f.write("feature locl {\n")
    for _locale in LOCALES:
        if _locale != locale and len(substitution_rules[_locale]):
            f.write(f"""  script hani;\n  language {LOCALES[_locale]["tla"]};\n""")

            for (_from, _to) in substitution_rules[_locale]:
                f.write(f"""    substitute \{_from} by \{_to};\n""")

    f.write("} locl;\n")
    f.write(FEATURES_FOOTER_TEMPLATE())
    f.close()