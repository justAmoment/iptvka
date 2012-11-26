#!/bin/sh
provider="rtk"
dir_provider="provider/"${provider}
dir_format="format"
dir_list="list"
r=`cat ${dir_format}"/raw"`
types="igmp udpxy"

for type in ${types}
do
 x=`cat ${dir_format}"/prefix_ip_"${type}`

 # Generate all lists
 target_m3u="m3u/iptv_"${provider}"_"${type}"_all.m3u"
 cat ${dir_format}"/head" > ${target_m3u}
 for port in `ls ${dir_provider} | sort -n`
 do
  for y in `ls ${dir_provider}"/"${port} | sort -n`
  do
   for i in `ls ${dir_provider}"/"${port}"/"${y} | sort -n`
   do
    echo ${r}""`sed -n 3,3p ${dir_provider}"/"${port}"/"${y}"/"${i}`", "${i}" -- "`sed -n 1,1p ${dir_provider}"/"${port}"/"${y}"/"${i}` >> ${target_m3u}
    echo ${x}${y}"."${i}":"${port} >> ${target_m3u}
   done
  done
 done

 # Generate special lists
 for list in `ls ${dir_list}`
 do
  target_m3u="m3u/iptv_"${provider}"_"${type}"_"${list}".m3u"
  cat ${dir_format}"/head" > ${target_m3u}
  for la in `cat ${dir_list}"/"${list}`
  do
   ary=(${la//./ })
   ip123=${ary[0]}"."${ary[1]}"."${ary[2]}
   ip4=${ary[3]}
   port=${ary[4]}
   echo ${r}""`sed -n 3,3p ${dir_provider}"/"${port}"/"${ip123}/${ip4}`", "${ip4}" -- "`sed -n 1,1p ${dir_provider}"/"${port}"/"${ip123}/${ip4}` >> ${target_m3u}
   echo ${x}${ip123}"."${ip4}":"${port} >> ${target_m3u}
  done
 done
done
