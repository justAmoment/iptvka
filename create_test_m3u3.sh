#!/bin/sh
provider="rtk"
dir_provider="provider/"$provider
dir_format="format"
dir_list="list"
x_i=`cat $dir_format"/prefix_ip_igmp"`
x_u=`cat $dir_format"/prefix_ip_udpxy"`
r=`cat $dir_format"/raw"`

# Generate all lists
target_m3u_i="m3u/iptv_"$provider"_igmp_all.m3u"
target_m3u_u="m3u/iptv_"$provider"_udpxy_all.m3u"

cat $dir_format"/head" > $target_m3u_i
cat $dir_format"/head" > $target_m3u_u
for port in `ls $dir_provider | sort -n`
do
 for y in `ls $dir_provider"/"$port | sort -n`
 do
  for i in `ls $dir_provider"/"$port"/"$y | sort -n`
  do
   echo $r" "`sed -n 3,3p $dir_provider"/"$port"/"$y"/"$i`", "$i" -- "`sed -n 1,1p $dir_provider"/"$port"/"$y"/"$i` >> $target_m3u_i
   echo $r" "`sed -n 3,3p $dir_provider"/"$port"/"$y"/"$i`", "$i" -- "`sed -n 1,1p $dir_provider"/"$port"/"$y"/"$i` >> $target_m3u_u
   echo ${x_i}$y.$i":"$port >> $target_m3u_i
   echo ${x_u}$y.$i":"$port >> $target_m3u_u
  done
 done
done
# Generate special lists
for list in `ls $dir_list`
do
 target_m3u_i="m3u/iptv_"$provider"_igmp_"$list".m3u"
 target_m3u_u="m3u/iptv_"$provider"_udpxy_"$list".m3u"
 cat $dir_format"/head" > $target_m3u_i
 cat $dir_format"/head" > $target_m3u_u

 for x in `cat $dir_list"/"$list`
 do
  ary=(${x//./ })

  ip123=${ary[0]}"."${ary[1]}"."${ary[2]}
  ip4=${ary[3]}
  port=${ary[4]}
  echo $r" "`sed -n 3,3p $dir_provider"/"$port"/"$ip123/$ip4`", "$ip4" -- "`sed -n 1,1p $dir_provider"/"$port"/"$ip123/$ip4` >> $target_m3u_i
  echo $r" "`sed -n 3,3p $dir_provider"/"$port"/"$ip123/$ip4`", "$ip4" -- "`sed -n 1,1p $dir_provider"/"$port"/"$ip123/$ip4` >> $target_m3u_u
  echo ${x_i}$ip123"."$ip4":"$port >> $target_m3u_i
  echo ${x_u}$ip123"."$ip4":"$port >> $target_m3u_u

 done
done
