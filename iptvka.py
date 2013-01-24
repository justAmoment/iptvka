#!/bin/python

from gi.repository import Gtk, Gdk
from iptvka_gui import iptvkaWindow


window = iptvkaWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()