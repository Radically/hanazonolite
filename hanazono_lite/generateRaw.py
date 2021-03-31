from .config import Config
from .constants import *
import subprocess
import os


def generateRaw(prefix, locale, adobe_perl_scripts):
    config = Config.getInstance()
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

    # seems to be ineffective, keeping here for future reference
    # restore ascent details
    # subprocess.run(
    #     f"""sed "s/FontInfo 7 dict dup begin/FontInfo 7 dict dup begin\\n\/ascent 100 def/g" {font_family}.raw > {font_family}.tmp.raw""",
    #     shell=True,
    # )

    # shift glyphs downward
    subprocess.run(
        f"rotatefont -t1 -matrix 1 0 0 1.1 0 -150 {font_family}.raw > {font_family}.tmp.raw",
        shell=True,
    )

    subprocess.run(["mv", f"{font_family}.tmp.raw", f"{font_family}.raw"])

    if config["hinted"]:
        subprocess.run(
            # /BlueValues [-250 -250 1100 1100] def
            # /StdHW [20] def
            # /StdVW [60] def
            # sed must be used to avoid messing up the binary data of the raw font
            # f"""sed "s/\[0 0\] def/\[-250 -250 1100 1100\] def\\n\/StdHW \[20\] def\\n\/StdVW \[60\] def/g" {font_family}.raw | sed "s/Private 7/Private 10/g" > {font_family}.hinted.raw""",
            f"""sed "s/\[0 0\] def/\[-250 -250 1100 1100\] def/g" {font_family}.raw | sed "s/Private 7/Private 10/g" > {font_family}.hinted.raw""",
            shell=True,
        )

        subprocess.run(["psautohint", f"""{font_family}.hinted.raw"""])

    # subprocess.run(
    #     f"""{adobe_perl_scripts}/hintcidfont.pl hintparam.txt < {font_family}.raw > {font_family}.hinted.raw""",
    #     shell=True,
    # )

    # subprocess.run(f"""psautohint {font_family}.hinted.raw""", shell=True)
