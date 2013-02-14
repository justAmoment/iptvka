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
    """Class store functions to interract with user. GUI / GTK / ListView / TreeView."""
    sbar = Gtk.Statusbar()
    sbar_id = sbar.get_context_id("sbar1")

    def __init__(self, iptvka):
        self.iptvka = iptvka
        L = self.iptvka.lsts
        Gtk.Window.__init__(self, title="iptvka")
        new_w = int(Gdk.Screen.width() * 3/4)
        new_h = int(Gdk.Screen.height() * 3/4)
        new_x = int((Gdk.Screen.width() - new_w) / 2)
        new_y = int((Gdk.Screen.height() - new_h) / 2)
        self.set_default_size(new_w, new_h)
        self.move(new_x, new_y)

        self.trvw1 = Gtk.TreeView(model=L)
        self.swnd1 = Gtk.ScrolledWindow()
        self.swnd1.add(self.trvw1)

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

        for x_col in range(len(self.iptvka.x_title)):
            column = Gtk.TreeViewColumn(self.iptvka.x_title[x_col], Gtk.CellRendererText(), text=x_col)
            column.set_sort_column_id(x_col)
            self.trvw1.append_column(column)
            L.set_sort_func(x_col, self.iptvka.compare, self.iptvka.x_title_sort_val[self.iptvka.x_title[x_col]])

        self.iptvka.reload_ip_from_dir()
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
        action_createallm3u.connect("activate", self.on_menu_createallm3u)
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
        self.iptvka.lsts.clear()
        self.iptvka.reload_ip_from_dir()
        self.update_sbar("stat")

    def on_menu_fileclear(self, widget):
        self.iptvka.lsts.clear()
        self.update_sbar("stat")

    def on_menu_filesave(self, widget):
        """Save ip/port/name/params from listview to source dirs."""
        dir_from = self.iptvka.dir_from
        dir_prov = self.iptvka.dir_prov
        L = self.iptvka.lsts
        Lnr = len(L)
        dlg1 = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "Save channels to source dir?")
        dlg1.format_secondary_text("dir = %s\nch = %s" % (join(dir_from, dir_prov), Lnr))
        response = dlg1.run()
        dlg1.hide()
        n_ok = 0
        if response == Gtk.ResponseType.YES:
            for r in range(Lnr):
                nx, prov, ip1234, port, tag_x, list_x, name, demux, stb, extvlc = L[r][:]
                ip1234 = [str(int(x)) for x in ip1234.split(".")]
                ip123 = ".".join(ip1234[:-1])
                ip4 = ip1234[-1]
                dir1 = join(dir_from, dir_prov, prov, port, ip123)
                # Check problem with realpath
                if dir1 == os.path.realpath(dir1):
                    try:
                        if not os.path.exists(dir1):
                            os.makedirs(dir1)
                    except:
                        pass

                    try:
                        if os.path.isdir(dir1):
                            fn1 = join(dir_from, dir_prov, prov, port, ip123, ip4)
                            f1 = open(fn1, "w")
                            f1.writelines("\n".join(L[r][-4:]))
                            f1.close()
                            n_ok += 1
                    except:
                        pass
                else:
                    print "Error: channel %s not saved, realpath '%s' not equal dir '%s'." % (nx, os.path.realpath(dir1), dir1)

            if n_ok == Lnr:
                msg2 = "Success 100%"
            else:
                msg2 = "Partial success %.02f%%" % (100.00 * n_ok / Lnr)
            dlg2 = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, msg2)
            dlg2.format_secondary_text("dir = %s\n(%s from %s) channels saved" % (join(dir_from, dir_prov), n_ok, Lnr))
            dlg2.run()
            dlg2.hide()
        else:
            pass

    def on_menu_createallm3u(self, widget):
        """Create and save all 'm3u' from listview to target dir 'm3u/*'."""
        dir_from = self.iptvka.dir_from
        dir_format = self.iptvka.dir_format
        dir_m3u = self.iptvka.dir_m3u
        tps = self.iptvka.tps
        h = self.iptvka.h

        L = self.iptvka.lsts
        Lnr = len(L)
        text_m3u = str(h)
        tm = {}
        raw = self.iptvka.raw
        for tp in tps:
            for r in range(Lnr):
                if tp in self.iptvka.ip_pre:
                    ip_pre = self.iptvka.ip_pre[tp]
                else:
                    ip_pre = ""
                nx, prov, ip1234, port, tag_x, list_x, name, demux, stb, extvlc = L[r][:]
                ip4 = str(int(ip1234.rsplit(".",1)[-1]))
                if demux:
                    ip_pre = ip_pre.replace(":", "/" + demux + ":", 1)
                if (tp, prov) not in tm:
                    tm[(tp, prov)] = str(h)
                tm[(tp, prov)] += "%s, %s -- %s%s\n" % (raw[0], ip4, name, self.iptvka.in_tags(prov + "." + port + "." + ip1234))
                for e in extvlc.split():
                    tm[(tp, prov)] += "%s%s\n" % (raw[1], e)
                tm[(tp, prov)] += "%s%s:%s\n" % (ip_pre, ip1234, port)
        n_ok = 0
        dir1 = ""
        for (tp, prov) in tm:
            # Check problem with realpath
            dir1 = join(dir_from, dir_m3u)
            if dir1 == os.path.realpath(dir1):
                try:
                    if not os.path.exists(dir1):
                        os.makedirs(dir1)
                except:
                    pass

                try:
                    if os.path.isdir(dir1):
                        fn1 = join(dir_from, dir_m3u, "iptv_" + prov + "_" + tp + "_all.m3u")
                        f1 = open(fn1, "w")
                        f1.writelines(tm[(tp, prov)])
                        f1.close()
                        n_ok += 1
                except:
                    pass
            else:
                print "Error: channel %s not saved, realpath '%s' not equal dir '%s'." % (nx, os.path.realpath(dir1), dir1)
        msg2 = "Done"
        dlg2 = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, msg2)
        dlg2.format_secondary_text("dir = %s\n%s playlists (*.m3u) saved" % (dir1, n_ok))
        dlg2.run()
        dlg2.hide()

    def update_sbar(self, act = "clear"):
        """Update statusbar (act = 'clear' | 'stat')."""
        L = self.iptvka.lsts
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
                u += self.iptvka.x_title[c] + " = " + str(d) + "   |   "
        S.push(S_id, u)
