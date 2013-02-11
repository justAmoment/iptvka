#!/bin/python

import ConfigParser, sys, os
from os.path import join

class iptvkaBase():
    """Class stores inner vars, functions to interact with file system and inner vars."""
    dir_from = "."
    dir_prov = "provider"
    dir_format = "format"
    dir_m3u = "m3u"
    dir_tag = "tag"
    f_cfg = "iptvka.cfg"
    tps = ["igmp", "udpxy"]
    h = "#EXTM3U"
    tl = []
    ta = {}
    t_pre = "_"
    t_post = "_"

    def __init__(self, dir_from):
        self.dir_from = dir_from
        if len(sys.argv) > 1:
            self.f_cfg = sys.argv[1]
        else:
            self.f_cfg = join(self.dir_from, "iptvka.cfg")

        config = ConfigParser.ConfigParser()
        try:
            config.readfp(open(self.f_cfg))
            self.dir_from = str(config.get("general", "dir_from"))
            if self.dir_from == ".":
                self.dir_from = os.path.realpath(os.path.dirname(__file__))
            self.dir_prov = str(config.get("general", "dir_prov"))
            self.dir_format = str(config.get("general", "dir_format"))
            self.dir_m3u = str(config.get("general", "dir_m3u"))
        except:
            pass
        try: self.dir_tag = str(config.get("general", "dir_tag"))
        except: pass
        try: self.h = open(join(self.dir_from, self.dir_format, "head"), "r").read()
        except: pass
        try: self.t_pre = open(join(self.dir_from, self.dir_format, "tag_prefix"), "r").read()
        except: pass
        try: self.t_post = open(join(self.dir_from, self.dir_format, "tag_postfix"), "r").read()
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
        except:
            pass

    def in_tags(self, ip):
        """Return string of {tags} where 'ip' is in 'ta'.
        'ta' - dict with key='tag', val = list of 'ip'.
        ta = {tag1: [ip1, ip2], tag2: [ip1, ip3]}"""
        ret = ""
        for z in self.tl:
            if ip in self.ta[z]:
                ret += self.t_pre + str(z) + self.t_post
        return ret
