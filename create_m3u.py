#!/bin/python
import os

def inTags(ta, ip):
	ret = ""
	for z in ta:
		if ip in ta[z]:
			ret += " -- " + str(z)
	return ret

from os.path import join
provider = "rtk"
dir_provider=join("provider", provider)
dir_format = "format"
dir_list = "list"
dir_tag = "tag"
h = open(join(dir_format, "head"), "r").read()
r = open(join(dir_format, "raw"), "r").read()
tps = ["igmp", "udpxy"]

# Fill tag array
tl = os.listdir(dir_tag)
tl.sort()
ta = {}
for t in tl:
	ta[t] = []
	for tt in [x.strip() for x in open(join(dir_tag, t), "r").readlines()]:
		if tt:
			ta[t].append(tt)

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
				ip1234 = str(y) + "." + str(i)
				f1 = open(join(dir_provider, port, y, i), "r")
				s1 = [x.strip() for x in f1.readlines()]
				f_m3u.write(str(r) + ", " + str(i) + " -- " + s1[0] + inTags(ta, ip1234) + "\n")
				f_m3u.write(str(p) + str(ip1234) + ":" + str(port) + "\n")
	f_m3u.close()

	# Generate special lists
	lists = os.listdir(dir_list)
	lists.sort()
	for lst in lists:
		target_m3u = join("m3u", "iptv_" + provider + "_" + tp + "_" + lst + ".m3u")
		f_m3u = open(target_m3u, "w")
		f_m3u.write(h)
		for la in [x.strip() for x in open(join(dir_list,lst), "r").readlines()]:
			ary = la.split(".")
			ip123 = str(ary[0]) + "." + str(ary[1]) + "." + str(ary[2])
			ip4 = str(ary[3])
			ip1234 = ip123 + "." + ip4
			port = str(ary[4])
			f1 = open(join(dir_provider, port, ip123, ip4), "r")
			s1 = [x.strip() for x in f1.readlines()]
			f_m3u.write(str(r) + ", " + str(ip4) + " -- " + s1[0] + inTags(ta, ip1234) + "\n")
			f_m3u.write(str(p) + str(ip1234) + ":" + str(port) + "\n")
		f_m3u.close()
