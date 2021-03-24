from .constants import *
import subprocess
import os


def generateRaw(prefix, locale, adobe_perl_scripts):
    font_family = f"{prefix}{LOCALES[locale]['suffix']}"
    subprocess.run(
        [
            "mergefonts",
            "-cid",
            f"{font_family}.cidinfo",
            f"{font_family}.raw",
            f"{font_family}.cidmap",
            f"{font_family}.pfa",
        ]
    )

    # subprocess.run(
    #     f"""{adobe_perl_scripts}/hintcidfont.pl hintparam.txt < {font_family}.raw > {font_family}.hinted.raw""",
    #     shell=True,
    # )

    # subprocess.run(f"""psautohint {font_family}.hinted.raw""", shell=True)
