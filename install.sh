#!/bin/sh

i="iptvka.desktop"
src=$(pwd)
dst=$HOME"/.local/share/applications"
y=`pwd | sed 's%\/%\\\/%g'`"\/iptvka.py"
sed -i "s/^Exec=.*/Exec=${y}/" ${i}
echo "Create softlink to '${i}' in applications"
echo ${src}"/"${i}" ---> "${dst}"/"${i}
ln -s ${src}"/"${i} ${dst}"/"${i}
