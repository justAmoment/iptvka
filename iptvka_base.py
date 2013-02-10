#!/bin/python

import ConfigParser, sys, os
from os.path import join

class iptvkaBase():
    """Class stores inner vars, functions to interact with file system and inner vars."""
    dir_from = "."
    dir_prov = "provider"
    dir_format = "format"
    dir_m3u = "m3u"
    f_cfg = "iptvka.cfg"
    tps = ["igmp", "udpxy"]
    h = "#EXTM3U"

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
            self.h = open(join(self.dir_from, self.dir_format, "head"), "r").read()
        except:
            pass
