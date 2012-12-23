#!/bin/python
import os
from os.path import join
provider = "rtk"
dir_provider=join("provider", provider)
dir_format = "format"
dir_list = "list"
h = open(join(dir_format, "head"), "r").read()
r = open(join(dir_format, "raw"), "r").read()
tps = ["igmp", "udpxy"]
for tp in tps:
	p = open(join(dir_format, "prefix_ip_" + tp), "r").read()

	# Generate all lists
	target_m3u = join("m3u", "iptv_" + provider + "_" + tp + "_all.m3u")
	f_m3u = open(target_m3u, "w")
	f_m3u.write(h)
	ports = os.listdir(dir_provider)
	ports.sort(key=int)
	for port in ports:
		yy = os.listdir(join(dir_provider, port))
		yy.sort()
		for y in yy:
			ii = os.listdir(join(dir_provider, port, y))
			ii.sort(key=int)
			for i in ii:
				f1 = open(join(dir_provider, port, y, i), "r")
				s1 = [x.strip() for x in f1.readlines()]
				f_m3u.write(str(r) + ", " + str(i) + " -- " + s1[0] + "\n")
				f_m3u.write(str(p) + str(y) + "." + str(i) + ":" + str(port) + "\n")
	f_m3u.close()

	# Generate special lists
	lists = os.listdir(dir_list)
	lists.sort()
	for list in lists:
		target_m3u = join("m3u", "iptv_" + provider + "_" + tp + "_" + list + ".m3u")
		f_m3u = open(target_m3u, "w")
		f_m3u.write(h)
		for la in [x.strip() for x in open(join(dir_list,list), "r").readlines()]:
			ary = la.split(".")
			ip123 = str(ary[0]) + "." + str(ary[1]) + "." + str(ary[2])
			ip4 = str(ary[3])
			port = str(ary[4])
			f1 = open(join(dir_provider, port, ip123, ip4), "r")
			s1 = [x.strip() for x in f1.readlines()]
			f_m3u.write(str(r) + ", " + str(ip4) + " -- " + s1[0] + "\n")
			f_m3u.write(str(p) + str(y) + "." + str(ip4) + ":" + str(port) + "\n")
		f_m3u.close()