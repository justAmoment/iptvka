#!/bin/sh
x="http://192.168.0.218:4022/udp/"
b="base"
cat format/head > m3u/all.m3u
for y in `ls $b | sort -n`
do
 for i in `ls $b/$y | sort -n`
 do
 echo "#EXTINF:-1, "$i" -- "`head -1 $b/$y/$i` >> m3u/all.m3u
 echo $x$y.$i":5000" >> m3u/all.m3u
 done;
done;