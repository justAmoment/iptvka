#!/bin/sh
provider="rtk"
dir_provider="provider/"$provider
dir_format="format"
x_i=`cat $dir_format"/prefix_ip_igmp"`
x_u=`cat $dir_format"/prefix_ip_udpxy"`
r=`cat $dir_format"/raw"`
port_iptv=`cat $dir_format"/port"`
target_m3u_i="m3u/iptv_"$provider"_igmp_all.m3u"
target_m3u_u="m3u/iptv_"$provider"_udpxy_all.m3u"

cat $dir_format"/head" > $target_m3u_i
cat $dir_format"/head" > $target_m3u_u
for y in `ls $dir_provider | sort -n`
do
 for i in `ls $dir_provider/$y | sort -n`
 do
 echo $r" "$i" -- "`head -1 $dir_provider/$y/$i` >> $target_m3u_i
 echo $r" "$i" -- "`head -1 $dir_provider/$y/$i` >> $target_m3u_u
 echo ${x_i}$y.$i":"$port_iptv >> $target_m3u_i
 echo ${x_u}$y.$i":"$port_iptv >> $target_m3u_u
 done;
done;