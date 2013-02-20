#!/bin/python

import ConfigParser, sys, os
from os.path import join
from gi.repository import Gtk

class iptvkaCore():
    """Class stores inner vars, functions to interact with file system and inner vars."""
    dir_from = "."
    dir_prov = "provider"
    dir_format = "format"
    dir_m3u = "m3u"
    dir_tag = "tag"
    dir_list = "list"
    f_cfg = "iptvka.cfg"
    tps = ["igmp", "udpxy"]
    ip_pre = {}
    h = "#EXTM3U"
    need_raw_lines = 2
    raw = ["#EXTINF:-1", "#EXTVLCOPT:"]
    tl = []
    ta = {}
    t_pre = "_"
    t_post = "_"
    ll = []
    la = {}
    l_pre = "_"
    l_post = "_"

    lsts = Gtk.ListStore(str, str, str, str, str, str, str, str, str, str)
    x_title = ["#", "provider", "ip", "port", "tag", "list", "name", "demux", "#STB", "#EXTVLCOPT"]
    x_title_sort_val = {
                    "#" : "int",
             "provider" : "str",
                   "ip" : "ip4",
                 "port" : "int",
                  "tag" : "str",
                 "list" : "str",
                 "name" : "str",
                "demux" : "str",
                 "#STB" : "str",
           "#EXTVLCOPT" : "str",
                        }

    def __init__(self, dir_from):
        self.dir_from = dir_from
        if len(sys.argv) > 1:
            self.f_cfg = sys.argv[1]
        else:
            self.f_cfg = join(self.dir_from, "iptvka.cfg")

        config = ConfigParser.ConfigParser()
        try:
            config.readfp(open(self.f_cfg))
            try:
                self.dir_from = str(config.get("general", "dir_from"))
                if self.dir_from == ".":
                    self.dir_from = os.path.realpath(os.path.dirname(__file__))
            except: pass
            try: self.dir_prov = str(config.get("general", "dir_prov"))
            except: pass
            try: self.dir_format = str(config.get("general", "dir_format"))
            except: pass
            try: self.dir_m3u = str(config.get("general", "dir_m3u"))
            except: pass
            try: self.dir_tag = str(config.get("general", "dir_tag"))
            except: pass
            try: self.dir_list = str(config.get("general", "dir_list"))
            except: pass
            try:
                tps_x = str(config.get("general", "tps"))
                tps_x = [x for x in tps_x.split("\n") if x]
                self.tps = tps_x
            except: pass
        except: pass
        try: self.h = open(join(self.dir_from, self.dir_format, "head"), "r").read()
        except: pass
        try:
            raw_x = [x.strip("\n") for x in open(join(self.dir_from, self.dir_format, "raw"), "r").readlines()]
            for i in range(min(self.need_raw_lines, len(raw_x))):
                self.raw[i] = raw_x[i]
        except: pass
        try: self.t_pre = open(join(self.dir_from, self.dir_format, "tag_prefix"), "r").read()
        except: pass
        try: self.t_post = open(join(self.dir_from, self.dir_format, "tag_postfix"), "r").read()
        except: pass
        try:
            for tp in self.tps:
                self.ip_pre[tp] = open(join(self.dir_from, self.dir_format, "prefix_ip_" + tp), "r").read()
        except: pass
        try:
            # Fill tag array
            self.tl = os.listdir(join(self.dir_from, self.dir_tag))
            self.tl.sort()
            for t in self.tl:
                self.ta[t] = []
                for tt in [x.strip() for x in open(join(self.dir_from, self.dir_tag, t), "r").readlines() if not x.isspace()]:
                    if tt:
                        self.ta[t].append(tt)
        except: pass
        try:
            # Fill list array
            self.ll = os.listdir(join(self.dir_from, self.dir_list))
            self.ll.sort()
            for l in self.ll:
                self.la[l] = []
                for i in [x.strip() for x in open(join(self.dir_from, self.dir_list, l), "r").readlines() if not x.isspace()]:
                    if i:
                        self.la[l].append(i)
        except: pass

    def in_tags(self, ip):
        """Return string of {tags} where 'ip' is in 'ta'.
        'ta' - dict with key='tag', val = list of 'ip'.
        ta = {tag1: [ip1, ip2], tag2: [ip1, ip3]}"""
        ret = ""
        for z in self.tl:
            if ip in self.ta[z]:
                ret += self.t_pre + str(z) + self.t_post
        return ret

    def in_lists(self, ip):
        """Return string of lists where 'ip' is in 'la'.
        'la' - dict with key='list', val = list of 'ip'.
        la = {list1: [ip1, ip2], list2: [ip1, ip3]}"""
        ret = ""
        for z in self.ll:
            if ip in self.la[z]:
                ret += self.l_pre + str(z) + self.l_post
        return ret

    def reload_ip_from_dir(self):
        """Get ip/port/name/params from source dirs and set it to listview."""
        dir_from = self.dir_from
        dir_prov = self.dir_prov
        dir_format = self.dir_format
        L = self.lsts
        need_n_lines = 4
        h      = open(join(dir_from, dir_format, "head"),        "r").read()
        t_pre  = open(join(dir_from, dir_format, "tag_prefix"),  "r").read()
        t_post = open(join(dir_from, dir_format, "tag_postfix"), "r").read()
        provs = os.listdir(join(dir_from, dir_prov))
        provs.sort()
        for prov in provs:
            ports = os.listdir(join(dir_from, dir_prov, prov))
            ports.sort(key=int)
            for port in ports:
                yy = os.listdir(join(dir_from, dir_prov, prov, port))
                yy.sort()
                for y in yy:
                    ii = os.listdir(join(dir_from, dir_prov, prov, port, y))
                    ii.sort(key=int)
                    for i in ii:
                        ip1234 = str(y) + "." + str(i)

                        f1 = open(join(dir_from, dir_prov, prov, port, y, i), "r")
                        s1 = [x.strip() for x in f1.readlines()]
                        if len(s1) < need_n_lines:
                            for x in range(len(s1), need_n_lines):
                                s1.append("")
                        tag_x = self.in_tags(prov + "." + port + "." + ip1234)
                        list_x = self.in_lists(prov + "." + port + "." + ip1234)
                        L.append([str(len(L) + 1), prov, ip1234, port, tag_x, list_x, s1[0], s1[1], s1[2], s1[3]])

    def compare(self, model, row1, row2, sort_val):
        """Function is sorting rows in listview."""
        ret = 0
        try:
            sort_column = model.get_sort_column_id()[0]
            if sort_val == "int":
                val1 = int(model.get_value(row1, sort_column))
                val2 = int(model.get_value(row2, sort_column))
                if   val1 < val2:   ret = -1
                elif val1 > val2:   ret = 1

            elif sort_val == "str":
                val1 = model.get_value(row1, sort_column)
                val2 = model.get_value(row2, sort_column)
                if   val1 < val2:   ret = -1
                elif val1 > val2:   ret = 1

            elif sort_val == "ip4":
                val1 = model.get_value(row1, sort_column)
                val1 = [int(x) for x in val1.split(".")]
                val2 = model.get_value(row2, sort_column)
                val2 = [int(x) for x in val2.split(".")]
                if   val1 < val2:   ret = -1
                elif val1 > val2:   ret = 1
        except:
            pass

        return ret
