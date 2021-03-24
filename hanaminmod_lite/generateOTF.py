from .constants import *
import subprocess
import os


def generateOTF(prefix, locale):
    font_family = f"{prefix}{LOCALES[locale]['suffix']}"
    subprocess.run(
        [
            "makeotf",
            "-newNameID4",
            "-cs",
            "1",
            "-ch",
            f"""{font_family}.optim.cmap""",
            "-f",
            f"""{font_family}.raw""",
            "-ff",
            f"""{font_family}.features""",
            "-o",
            f"""{font_family}.otf""",
        ]
    )
