#!/bin/python

from gi.repository import Gtk, Gdk
from iptvka_gui import iptvkaWindow

dir_from = "."

window = iptvkaWindow(dir_from = dir_from)
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()