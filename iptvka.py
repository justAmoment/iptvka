#!/bin/python

from gi.repository import Gtk, Gdk
import iptvka_gui


window = iptvka_gui.iptvkaWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()