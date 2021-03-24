from .constants import *
import subprocess


def generatePFADump(prefix, locale, adobe_perl_scripts):
    font_family = f"{prefix}{LOCALES[locale]['suffix']}"
    subprocess.run(["tx", "-t1", f"{font_family}.svg", f"{font_family}.pfa"])

    # subprocess.run(
    #     f"""{adobe_perl_scripts}/hintcidfont.pl hintparam.txt < {font_family}.pfa > {font_family}.hinted.pfa""",
    #     shell=True,
    # )

    subprocess.run(["tx", "-dump", f"{font_family}.pfa", f"{font_family}.dump"])
    subprocess.run(
        f"{adobe_perl_scripts}/cmap-tool.pl < {font_family}.cmap > {font_family}.optim.cmap",
        shell=True,
    )
