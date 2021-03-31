import datetime
import json
from .config import Config

# OUTPUT_DIR = "output"

LOCALES = {
    "g": {"tla": "ZHS", "suffix": "SC"},
    "t": {"tla": "ZHT", "suffix": "TC"},
    "h": {"tla": "ZHH", "suffix": "HK"},
    "j": {"tla": "JAN", "suffix": "JP"},
    "k": {"tla": "KOR", "suffix": "KR"},
    "v": {"tla": "VIT", "suffix": "VN"},
}

_CIDINFO_TEMPLATE = """FontName       ({FontName})
FullName       ({FullName})
FamilyName     ({FamilyName})
Weight         Regular
version        ({Version})
Registry       (Adobe)
Ordering       (Identity)
Supplement     0
AdobeCopyright (Copyright 2002-{Year} GlyphWiki PROJECT)

PreferOS/2TypoMetrics      true
IsOS/2WidthWeigthSlopeOnly true
IsOS/2OBLIQUE              false"""


def CIDINFO_TEMPLATE(FontName, FullName, FamilyName):
    config = Config.getInstance()

    return _CIDINFO_TEMPLATE.format(
        FontName=FontName,
        FullName=FullName,
        FamilyName=FamilyName,
        Version=config["version"],
        Year=datetime.datetime.now().year,
    )


_FEATURES_FOOTER_TEMPLATE = """table head {{
    FontRevision {Version};
}} head;

table OS/2 {{
  TypoAscender 880;
  TypoDescender -120;
  TypoLineGap 0;
  WeightClass 300;
  WidthClass 5;
  CodePageRange 1252 932;
  FSType 0;
}} OS/2;

table name {{
      nameid 0 "2007-{Year} GlyphWiki. All Rights Reserved.";
      nameid 0 3 1 0x411 "2007-{Year} GlyphWiki. All Rights Reserved.";
      nameid 7 "Hanazono Mincho is not yet a trademark of GlyphWiki. Hanazono Lite is a collection of UNOFFICIAL GPLv3 AFDKO-generated fonts created by Bryan Kok <bryan.wyern1@gmail.com> using GlyphWiki glyphs.";
      nameid 7 3 1 0x411 "Hanazono Mincho is not yet a trademark of GlyphWiki. Hanazono Lite is a collection of UNOFFICIAL GPLv3 AFDKO-generated fonts created by Bryan Kok <bryan.wyern1@gmail.com> using GlyphWiki glyphs.";
      nameid 9 "KAMICHI Koichi; KAWABATA Taichi; KOK Bryan";
      nameid 9 1 1 0x411 "\\4e0a\\5730 \\5b8f\\4e00, \\5ddd\\5e61 \\592a\\4e00";
      nameid 11 "https://github.com/Radically/HanazonoLite";
      nameid 11 3 1 0x411 "https://github.com/Radically/HanazonoLite";
      nameid 14 "http://glyphwiki.org/license.html";
      nameid 14 3 1 0x411 "http://glyphwiki.org/license.html";
}} name;

table hhea {{
  Ascender 880;
  Descender -120;
  LineGap 0;
}} hhea;

table vhea {{
  VertTypoLineGap 500;
}} vhea;
"""


def FEATURES_FOOTER_TEMPLATE():
    config = Config.getInstance()
    return _FEATURES_FOOTER_TEMPLATE.format(
        Version=config["version"], Year=datetime.datetime.now().year
    )
