#!/bin/sh
dir_base="base"
dir_format="format"
x=`cat $dir_format"/prefix_ip"`
port_iptv=`cat $dir_format"/port"`
cat $dir_format"/head" > m3u/all.m3u
for y in `ls $dir_base | sort -n`
do
 for i in `ls $dir_base/$y | sort -n`
 do
 echo "#EXTINF:-1, "$i" -- "`head -1 $dir_base/$y/$i` >> m3u/all.m3u
 echo $x$y.$i":"$port_iptv >> m3u/all.m3u
 done;
done;