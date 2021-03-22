x=$1
tx -t1 $1 ${x%%.*}.pfa && tx -dump ${x%%.*}.pfa > ${x%%.*}.dump