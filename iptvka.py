#!/bin/python

import ConfigParser, sys, os
from gi.repository import Gtk, Gdk
from iptvka_gui import iptvkaWindow

dir_from = os.path.dirname(__file__)

if len(sys.argv) > 1:
    f_cfg = sys.argv[1]
else:
    f_cfg = os.path.join(dir_from, "iptvka.cfg")

config = ConfigParser.ConfigParser()
try:
    config.readfp(open(f_cfg))
    dir_from = str(config.get("general", "dir_from"))
    if dir_from == ".":
        dir_from = os.path.dirname(__file__)
except:
    pass

try:
    window = iptvkaWindow(dir_from = dir_from)
except:
    print "'dir_from' has a wrong value = '%s'. Please check the config file '%s'. Now 'dir_from' set to the current directory." % (dir_from, f_cfg)
    window = iptvkaWindow(dir_from = dir_from)
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()