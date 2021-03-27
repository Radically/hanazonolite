cat fetch_dump.sh 
wget -q -nc http://glyphwiki.org/dump.tar.gz
rm -rf glyphwiki_dump && mkdir -p glyphwiki_dump
tar -xf dump.tar.gz --directory glyphwiki_dump