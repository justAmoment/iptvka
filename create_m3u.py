#!/bin/python
import os
from os.path import join

def inTags(tl, ta, ip, t_pre, t_post):
    ret = ""
    for z in tl:
        if ip in ta[z]:
            ret += t_pre + str(z) + t_post
    return ret

provider     = "rtk"
dir_provider = join("provider", provider)
dir_format   = "format"
dir_list     = "list"
dir_tag      = "tag"
need_n_lines = 3
h      = open(join(dir_format, "head"),        "r").read()
t_pre  = open(join(dir_format, "tag_prefix"),  "r").read()
t_post = open(join(dir_format, "tag_postfix"), "r").read()
r = [x.strip() for x in open(join(dir_format, "raw"), "r").readlines() if not x.isspace()]
tps = ["igmp", "udpxy"]

# Fill tag array
tl = os.listdir(dir_tag)
tl.sort()
ta = {}
for t in tl:
    ta[t] = []
    for tt in [x.strip() for x in open(join(dir_tag, t), "r").readlines() if not x.isspace()]:
        if tt:
            ta[t].append(tt)
for tp in tps:
    # ma[] store all records for all IP
    ma = {}
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
                if len(s1) < need_n_lines:
                    for x in range(len(s1), need_n_lines):
                        s1.append("")
                # add demux module name s1[1]. Example "http:" --> "http/ffmpeg:"
                s_prefix = p
                if s1[2]:
                    s_prefix = s_prefix.replace(":", "/" + s1[2] + ":", 1)
                # add #EXTINF:
                zx = provider + "." + port + "." + ip1234
                ma[zx] = []
                ma[zx] = str(r[0]) + ", " + str(i) + " -- " + s1[0] + inTags(tl, ta, zx, t_pre, t_post) + "\n"
                # add #EXTVLCOPT:
                if (len(r) > 1) and s1[1]:
                    for x in s1[1].split():
                        ma[zx] += str(r[1]) + x + "\n"
                # add IP:port
                ma[zx] += str(s_prefix) + str(ip1234) + ":" + str(port) + "\n"
                f_m3u.write(ma[zx])
                f1.close()
    f_m3u.close()

    # Generate special lists
    lists = os.listdir(dir_list)
    lists.sort()
    for lst in lists:
        target_m3u = join("m3u", "iptv_" + provider + "_" + tp + "_" + lst + ".m3u")
        f_m3u = open(target_m3u, "w")
        f_m3u.write(h)
        for la in [x.strip() for x in open(join(dir_list,lst), "r").readlines() if not x.isspace()]:
            f_m3u.write(ma[la])
        f_m3u.close()
