#!/bin/python

from gi.repository import Gtk, Gdk

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileRefresh' />
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='ActionMenu'>
      <menuitem action='CreateAllM3U' />
    </menu>
    <separator />
    <separator />
    <separator />
    <menu action='HelpMenu'>
      <menuitem action='Docum'/>
      <separator />
      <menuitem action='About'/>
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='FileRefresh' />
    <separator />
    <toolitem action='CreateAllM3U' />
    <separator />
    <toolitem action='Docum' />
    <toolitem action='About' />
  </toolbar>
</ui>
"""

class iptvkaWindow(Gtk.Window):
    dir_from = "."
    def __init__(self, dir_from = "."):
        self.dir_from = dir_from
        Gtk.Window.__init__(self, title="iptvka")

        self.set_default_size(750, 550)
        
        action_group = Gtk.ActionGroup("my_actions")

        self.add_file_menu_actions(action_group)
        #self.add_edit_menu_actions(action_group)
        #self.add_choices_menu_actions(action_group)

        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)

        toolbar = uimanager.get_widget("/ToolBar")
        box.pack_start(toolbar, False, False, 0)
        
        lsts = Gtk.ListStore(str, str, str, str)
        treeview = Gtk.TreeView(model=lsts)
        for x_raw in range(2):
            lsts.append(["rtk", "", "", ""])

        x_title = ["provider", "ip", "port", "name"]

        for x_col in range(len(x_title)):
            column_text = Gtk.TreeViewColumn(x_title[x_col], Gtk.CellRendererText(), text=x_col)
            treeview.append_column(column_text)
            print x_col, x_title[x_col]

        #renderer_pixbuf = Gtk.CellRendererPixbuf()
        #column_pixbuf = Gtk.TreeViewColumn("Image", renderer_pixbuf, stock_id=1)
        #treeview.append_column(column_pixbuf)
        
        box.pack_start(treeview, False, False, 0)

        #eventbox = Gtk.EventBox()
        #eventbox.connect("button-press-event", self.on_button_press_event)
        #box.pack_start(eventbox, True, True, 0)

        label = Gtk.Label("Right-click to see the popup menu.")
        #eventbox.add(label)

        self.popup = uimanager.get_widget("/PopupMenu")

        self.add(box)

    def add_file_menu_actions(self, action_group):
        # menu 1
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filerefresh = Gtk.Action("FileRefresh", None, None, Gtk.STOCK_REFRESH)
        action_filerefresh.connect("activate", self.on_menu_def)
        action_group.add_action(action_filerefresh)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_filequit)
        action_group.add_action(action_filequit)

        # menu 2
        action_actionmenu = Gtk.Action("ActionMenu", "Action", None, None)
        action_group.add_action(action_actionmenu)

        action_createallm3u = Gtk.Action("CreateAllM3U", None, None, Gtk.STOCK_CONVERT)
        action_createallm3u.connect("activate", self.on_menu_def)
        action_group.add_action(action_createallm3u)

        # menu 3
        action_helpmenu = Gtk.Action("HelpMenu", "Help", None, None)
        action_group.add_action(action_helpmenu)

        action_docum = Gtk.Action("Docum", None, None, Gtk.STOCK_HELP)
        action_docum.connect("activate", self.on_menu_def)
        action_group.add_action(action_docum)

        action_about = Gtk.Action("About", None, None, Gtk.STOCK_ABOUT)
        action_about.connect("activate", self.on_menu_about)
        action_group.add_action(action_about)


    def create_ui_manager(self):
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    def on_menu_def(self, widget):
        print "def item"

    def on_menu_filequit(self, widget):
        Gtk.main_quit()

    def on_menu_about(self, widget):
        abtd = Gtk.AboutDialog()
        abtd.set_version("version 0.1")
        abtd.set_program_name("iptvka")
        abtd.set_authors(["justAmoment"])
        abtd.set_comments("This program generate m3u playlists for iptv.")
        abtd.set_website("https://github.com/justAmoment/iptvka")
        abtd.set_website_label("https://github.com/justAmoment/iptvka")
        abtd.set_transient_for(self)
        abtd.run()
        abtd.hide()
