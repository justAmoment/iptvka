#!/bin/sh
dir_base="base"
dir_format="format"
x=`cat $dir_format"/prefix_ip"`
r=`cat $dir_format"/raw"`
port_iptv=`cat $dir_format"/port"`
target_m3u="m3u/all.m3u"

cat $dir_format"/head" > $target_m3u
for y in `ls $dir_base | sort -n`
do
 for i in `ls $dir_base/$y | sort -n`
 do
 echo $r" "$i" -- "`head -1 $dir_base/$y/$i` >> $target_m3u
 echo $x$y.$i":"$port_iptv >> $target_m3u
 done;
done;