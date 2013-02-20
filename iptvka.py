#!/bin/python

import ConfigParser, sys, os
from gi.repository import Gtk, Gdk
from iptvka_gui import iptvkaWindow
from iptvka_core import iptvkaCore

dir_from = os.path.realpath(os.path.dirname(__file__))
iptvka = iptvkaCore(dir_from = dir_from)

try:
    window = iptvkaWindow(iptvka = iptvka)
except:
    print "Maybe 'dir_from' has a wrong value = '%s'. Please check the config file '%s'. Now 'dir_from' set to the current directory." % (dir_from, iptvka.f_cfg)
    dir_from = os.path.dirname(__file__)
    iptvka = iptvkaCore(dir_from = dir_from)
    window = iptvkaWindow(iptvka = iptvka)
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()
