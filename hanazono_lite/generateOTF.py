from .config import Config
from .constants import *
import subprocess
import os


def generateOTF(prefix, locale):
    config = Config.getInstance()
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
            f"""{font_family}.hinted.raw"""
            if config["hinted"]
            else f"""{font_family}.raw""",
        ]
        + (
            [
                "-ff",
                f"""{font_family}.features""",
            ]
            if config["cjk"]
            else []
        )
        + [
            "-o",
            f"""{font_family}.otf""",
        ]
    )
