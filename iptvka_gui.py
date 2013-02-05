#!/bin/python

import os, subprocess
from gi.repository import Gtk, Gdk
from os.path import join

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileRefresh' />
      <menuitem action='FileClear' />
      <separator />
      <menuitem action='FileSave' />
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
    <toolitem action='FileClear' />
    <separator />
    <toolitem action='FileSave' />
    <separator />
    <toolitem action='CreateAllM3U' />
    <separator />
    <toolitem action='Docum' />
    <toolitem action='About' />
  </toolbar>
</ui>
"""

class iptvkaWindow(Gtk.Window):
    lsts = Gtk.ListStore(str, str, str, str, str, str, str, str)
    x_title = ["#", "provider", "ip", "port", "name", "#EXTVLCOPT", "demux", "#STB"]
    trvw1 = Gtk.TreeView(model=lsts)
    swnd1 = Gtk.ScrolledWindow()
    swnd1.add(trvw1)
    sbar = Gtk.Statusbar()
    sbar_id = sbar.get_context_id("sbar1")

    def __init__(self, dir_from):
        self.dir_from = dir_from
        Gtk.Window.__init__(self, title="iptvka")

        self.set_default_size(Gdk.Screen.width()*3/4, Gdk.Screen.height()*3/4)

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

        for x_col in range(len(self.x_title)):
            column_text = Gtk.TreeViewColumn(self.x_title[x_col], Gtk.CellRendererText(), text=x_col)
            self.trvw1.append_column(column_text)

        self.reload_ip_from_dir()
        self.update_sbar("stat")

        #renderer_pixbuf = Gtk.CellRendererPixbuf()
        #column_pixbuf = Gtk.TreeViewColumn("Image", renderer_pixbuf, stock_id=1)
        #trvw1.append_column(column_pixbuf)

        box.pack_start(self.swnd1, True, True, 0)
        box.pack_start(self.sbar, False, False, 0)

        #eventbox = Gtk.EventBox()
        #eventbox.connect("button-press-event", self.on_button_press_event)
        #box.pack_start(eventbox, True, True, 0)

        #label = Gtk.Label("Right-click to see the popup menu.")
        #eventbox.add(label)

        #self.popup = uimanager.get_widget("/PopupMenu")

        self.add(box)

    def add_file_menu_actions(self, action_group):
        # menu 1
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filerefresh = Gtk.Action("FileRefresh", None, None, Gtk.STOCK_REFRESH)
        action_filerefresh.connect("activate", self.on_menu_filerefresh)
        action_group.add_action(action_filerefresh)

        action_fileclear = Gtk.Action("FileClear", None, None, Gtk.STOCK_CLEAR)
        action_fileclear.connect("activate", self.on_menu_fileclear)
        action_group.add_action(action_fileclear)

        action_filesave = Gtk.Action("FileSave", None, None, Gtk.STOCK_SAVE)
        action_filesave.connect("activate", self.on_menu_filesave)
        action_group.add_action(action_filesave)

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

        action_help = Gtk.Action("Docum", None, None, Gtk.STOCK_HELP)
        action_help.connect("activate", self.on_menu_help)
        action_group.add_action(action_help)

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

    def on_menu_help(self, widget):
        url_wiki = "https://github.com/justAmoment/iptvka/wiki"
        try:
            subprocess.call(('xdg-open', url_wiki))
        except:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Additional info and help you can find on the wiki")
            dialog.format_secondary_text(url_wiki)
            dialog.run()
            dialog.hide()
    
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

    def on_menu_filerefresh(self, widget):
        self.lsts.clear()
        self.reload_ip_from_dir()
        self.update_sbar("stat")

    def on_menu_fileclear(self, widget):
        self.lsts.clear()
        self.update_sbar("stat")

    def on_menu_filesave(self, widget):
        print "save item"

    def reload_ip_from_dir(self):
        dir_prov = "provider"
        dir_format = "format"
        #dir_list = "list"
        #dir_tag = "tag"
        need_n_lines = 4
        h      = open(join(self.dir_from, dir_format, "head"),        "r").read()
        t_pre  = open(join(self.dir_from, dir_format, "tag_prefix"),  "r").read()
        t_post = open(join(self.dir_from, dir_format, "tag_postfix"), "r").read()
        provs = os.listdir(join(self.dir_from, dir_prov))
        provs.sort()
        for prov in provs:
            #print "=", prov
            ports = os.listdir(join(self.dir_from, dir_prov, prov))
            ports.sort(key=int)
            for port in ports:
                #print "=", port
                yy = os.listdir(join(self.dir_from, dir_prov, prov, port))
                yy.sort()
                #print yy
                for y in yy:
                    #print "==", y
                    ii = os.listdir(join(self.dir_from, dir_prov, prov, port, y))
                    ii.sort(key=int)
                    #print ii
                    for i in ii:
                        ip1234 = str(y) + "." + str(i)
                        #print ip1234

                        f1 = open(join(self.dir_from, dir_prov, prov, port, y, i), "r")
                        s1 = [x.strip() for x in f1.readlines()]
                        if len(s1) < need_n_lines:
                            for x in range(len(s1), need_n_lines):
                                s1.append("")
                        self.lsts.append([str(len(self.lsts) + 1), prov, ip1234, port, s1[0], s1[1], s1[2], s1[3]])

    def update_sbar(self, act = "clear"):
        L = self.lsts
        Lnc = L.get_n_columns()
        Lnr = len(L)
        S = self.sbar
        S_id = self.sbar_id
        u = "Uniq values:   "
        if act == "clear":
            S.push(S_id, "")
        elif act == "stat":
            for c in range(Lnc):
                d = len(list(set([L[r][c] for r in range(Lnr) if L[r][c]])))
                u += self.x_title[c] + " = " + str(d) + "   |   "
        S.push(S_id, u)


