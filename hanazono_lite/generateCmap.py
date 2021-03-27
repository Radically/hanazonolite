import re

from .constants import *

CMAP_BEGINNING = """
%!PS-Adobe-3.0 Resource-CMap
%%DocumentNeededResources: ProcSet (CIDInit)
%%IncludeResource: ProcSet (CIDInit)
%%BeginResource: CMap (GlyphWiki-UTF32-H)
%%Title: (GlyphWiki-UTF32-H Adobe Identity 0)
%%Version: 1.000
%%Copyright: -----------------------------------------------------------
%%Copyright: Copyright 1990-2021 Adobe. All rights reserved.
%%Copyright:
%%Copyright: Redistribution and use in source and binary forms, with or
%%Copyright: without modification, are permitted provided that the
%%Copyright: following conditions are met:
%%Copyright:
%%Copyright: Redistributions of source code must retain the above
%%Copyright: copyright notice, this list of conditions and the following
%%Copyright: disclaimer.
%%Copyright:
%%Copyright: Redistributions in binary form must reproduce the above
%%Copyright: copyright notice, this list of conditions and the following
%%Copyright: disclaimer in the documentation and/or other materials
%%Copyright: provided with the distribution. 
%%Copyright:
%%Copyright: Neither the name of Adobe nor the names of its contributors
%%Copyright: may be used to endorse or promote products derived from this
%%Copyright: software without specific prior written permission. 
%%Copyright:
%%Copyright: THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
%%Copyright: CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
%%Copyright: INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
%%Copyright: MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
%%Copyright: DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
%%Copyright: CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
%%Copyright: SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
%%Copyright: NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
%%Copyright: LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
%%Copyright: HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
%%Copyright: CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
%%Copyright: OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
%%Copyright: SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
%%Copyright: -----------------------------------------------------------
%%EndComments

/CIDInit /ProcSet findresource begin

12 dict begin

begincmap

/CIDSystemInfo 3 dict dup begin
  /Registry (Adobe) def
  /Ordering (Identity) def
  /Supplement 0 def
end def

/CMapName /GlyphWiki-UTF32-H def
/CMapVersion 1.000 def
/CMapType 1 def

/WMode 0 def

1 begincodespacerange
  <00000000> <0010FFFF>
endcodespacerange

1 beginnotdefrange
<00000000> <0000001f> 1
endnotdefrange
"""

CMAP_ENDING = """
endcmap
CMapName currentdict /CMap defineresource pop
end
end

%%EndResource
%%EOF
"""

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def generateCmap(prefix, locale, to_encode_list):
    font_family = f"{prefix}{LOCALES[locale]['suffix']}"
    f = open(f"{font_family}.cmap", "w")

    f.write(CMAP_BEGINNING)
    f.write('\n')

    i = 1
    # chunk to_encode_list into chunks of 100
    for chunk in chunks(to_encode_list, 100):
        f.write(f"{len(chunk)} begincidchar\n")
        for char in chunk:
            cp = re.search("[a-f0-9]+", char).group()
            cp = "0"*(8-len(cp)) + cp
            f.write(f"<{cp}> {i}\n")
            i+=1
        f.write("endcidchar\n")
    f.write(CMAP_ENDING)
    f.close()

    # optimize the cmap