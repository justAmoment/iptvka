#!/bin/python

import ConfigParser, sys
from gi.repository import Gtk, Gdk
from iptvka_gui import iptvkaWindow

if len(sys.argv) > 1:
    f_cfg = sys.argv[1]
else:
    f_cfg = 'iptvka.cfg'

config = ConfigParser.ConfigParser()
try:
    config.readfp(open(f_cfg))
    dir_from = str(config.get("general", "dir_from"))
except:
    dir_from = "."

try:
    window = iptvkaWindow(dir_from = dir_from)
except:
    print "'dir_from' has a wrong value = '%s'. Please check the config file '%s'. Now 'dir_from' set to the current directory." % (dir_from, f_cfg)
    dir_from = "."
    window = iptvkaWindow(dir_from = dir_from)
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()