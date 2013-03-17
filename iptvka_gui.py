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
    btnT = []

    def __init__(self, iptvka):
        self.iptvka = iptvka
        L = self.iptvka.lsts
        x_title = self.iptvka.x_title
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

        box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(box2, False, False, 0)

        btnT = self.btnT
        for x_col in range(len(x_title)):
            xc = x_title[x_col]

            column = Gtk.TreeViewColumn(xc, Gtk.CellRendererText(), text=x_col)
            column.set_sort_column_id(x_col)
            column.set_resizable(True)
            self.trvw1.append_column(column)
            L.set_sort_func(x_col, self.iptvka.compare, self.iptvka.x_title_sort_val[xc][0])

            btnT.append(Gtk.ToggleButton(xc))
            box2.pack_start(btnT[x_col], False, False, 0)
            btnT[x_col].set_active((self.iptvka.x_title_sort_val[xc][1]))
            btnT[x_col].connect("toggled", self.on_button_toggled, xc)

        self.iptvka.reload_ip_from_dir()

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

        self.trvw1.get_selection().connect("changed", self.on_changed)
        self.trvw1.connect("row-activated", self.on_row_activated)

        self.add(box)
        self.update_trvw()
        self.update_sbar("stat")

    def on_row_activated(self, trvw, row, c):
        """Show the dialog for editing row."""
        L = self.iptvka.lsts
        x_title = self.iptvka.x_title

        dlg = Gtk.Dialog("Edit row %s" % self.iptvka.lsts[row][0], self)
        E = Gtk.ListStore(str, str)
        trvw = Gtk.TreeView(model=E)
        cr = Gtk.CellRendererText()
        cr.set_property('editable', False)
        column = Gtk.TreeViewColumn("name", cr, text=0)
        trvw.append_column(column)
        cr = Gtk.CellRendererText()
        cr.set_property('editable', True)
        cr.connect('edited', self.on_edited_e, E)
        column = Gtk.TreeViewColumn("value", cr, text=1)
        trvw.append_column(column)
        for x_col in range(len(x_title)):
            xc = x_title[x_col]
            E.append([xc, L[row][x_col]])
        swnd = Gtk.ScrolledWindow()
        swnd.add(trvw)
        Enr = len(E)
        swnd.set_size_request(160 * 2, 30 * Enr)
        dlg.vbox.pack_start(swnd, True, True, 0)
        dlg.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dlg.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        dlg.show_all()
        response = dlg.run()
        dlg.hide()

        if response == Gtk.ResponseType.OK:
            for x_col in range(len(x_title)):
                xc = x_title[x_col]
                L[row][x_col] = E[x_col][1]
        else:
            pass

    def on_edited_e( self, cell, path, new_text, model ):
        """
        Called when a text cell is edited.  It puts the new text
        in the model so that it is displayed properly.
        """
        #print "Change '%s' to '%s'" % (model[path][1], new_text)
        model[path][1] = new_text
        #return

    def on_changed(self, selection):
        """ get the model and the iterator that points at the data in the model"""
        (model, iter) = selection.get_selected()
        #print "\n %s %s %s" %(model[iter][0],  model[iter][1], model[iter][2])

    def on_button_toggled(self, button, name):
        self.update_trvw()
        self.update_sbar("stat")

    def add_file_menu_actions(self, action_group):
        # menu 1 / toolbar 1
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

        # menu 2 / toolbar 1
        action_actionmenu = Gtk.Action("ActionMenu", "Action", None, None)
        action_group.add_action(action_actionmenu)

        action_createallm3u = Gtk.Action("CreateAllM3U", None, None, Gtk.STOCK_CONVERT)
        action_createallm3u.connect("activate", self.on_menu_createallm3u)
        action_group.add_action(action_createallm3u)

        # menu 3 / toolbar 1
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
                    except: pass
                    try:
                        if os.path.isdir(dir1):
                            fn1 = join(dir_from, dir_prov, prov, port, ip123, ip4)
                            f1 = open(fn1, "w")
                            f1.writelines("\n".join(L[r][-4:]))
                            f1.close()
                            n_ok += 1
                    except: pass
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
        h = str(self.iptvka.h)
        L = self.iptvka.lsts
        Lnr = len(L)
        LA = self.iptvka.la
        LL = self.iptvka.ll
        raw = self.iptvka.raw
        # tm{} temporary stores completed playlists for key (tp, prov, list)
        tm = {}
        # tp_prov{} temporary stores pair (tp, prov)
        tp_prov = {}
        # ma{} temporary stores all records for all IP
        ma = {}

        for tp in tps:
            for r in range(Lnr):
                if tp in self.iptvka.ip_pre:
                    ip_pre = self.iptvka.ip_pre[tp]
                else:
                    ip_pre = ""
                nx, prov, ip1234, port, tag_x, list_x, name, demux, stb, extvlc = L[r][:]
                ip4 = str(int(ip1234.rsplit(".",1)[-1]))
                zx = prov + "." + port + "." + ip1234
                if demux:
                    ip_pre = ip_pre.replace(":", "/" + demux + ":", 1)
                if (tp, prov, "all") not in tm:
                    tm[(tp, prov, "all")] = h
                    tp_prov[(tp, prov)] = 1
                ma[(tp,zx)] = ("%s, %s -- %s%s\n" % (raw[0], ip4, name, self.iptvka.in_tags(zx)))
                for e in extvlc.split():
                    ma[(tp,zx)] += "%s%s\n" % (raw[1], e)
                ma[(tp,zx)] += "%s%s:%s\n" % (ip_pre, ip1234, port)
                tm[(tp, prov, "all")] += ma[(tp,zx)]
        n_ok = 0
        dir1 = ""
        dir1 = join(dir_from, dir_m3u)
        # Check problem with realpath
        if dir1 == os.path.realpath(dir1):
            try:
                if not os.path.exists(dir1):
                    os.makedirs(dir1)
            except: pass
            for (tp, prov) in tp_prov:
                # Generate all lists
                try:
                    if os.path.isdir(dir1):
                        fn1 = join(dir_from, dir_m3u, "iptv_" + prov + "_" + tp + "_all.m3u")
                        if fn1 == os.path.realpath(fn1):
                            f1 = open(fn1, "w")
                            f1.writelines(tm[(tp, prov, "all")])
                            f1.close()
                            n_ok += 1
                        else:
                            print "Error: playlist not saved, realpath '%s' not equal file '%s'." % (os.path.realpath(fn1), fn1)
                except: pass
                # Generate special lists
                try:
                    for zl in LL:
                        try:
                            for zx in LA[zl]:
                                if (tp, prov, zl) not in tm:
                                    tm[(tp, prov, zl)] = h
                                tm[(tp, prov, zl)] += ma[(tp,zx)]
                            fn2 = join(dir_from, dir_m3u, "iptv_" + prov + "_" + tp + "_" + zl + ".m3u")
                            if fn2 == os.path.realpath(fn2):
                                f2 = open(fn2, "w")
                                f2.writelines(tm[(tp, prov, zl)])
                                f2.close()
                                n_ok += 1
                            else:
                                print "Error: playlist not saved, realpath '%s' not equal file '%s'." % (os.path.realpath(fn2), fn2)
                        except: pass
                except: pass
        msg2 = "Done"
        dlg2 = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, msg2)
        dlg2.format_secondary_text("dir = %s\n%s playlists (*.m3u) saved" % (dir1, n_ok))
        dlg2.run()
        dlg2.hide()

    def update_trvw(self):
        """Update Gtk.TreeView. Set visibility of the columns"""
        cr = range(len(self.btnT))
        xx = self.trvw1.get_columns()
        for c in cr:
            xx[c].set_visible(self.btnT[c].get_active())

    def update_sbar(self, act = "clear"):
        """Update statusbar (act = 'clear' | 'stat')."""
        L = self.iptvka.lsts
        Lnc = L.get_n_columns()
        Lnr = len(L)
        cr = range(min(Lnc, len(self.btnT)))
        S = self.sbar
        S_id = self.sbar_id
        u = "Uniq values:   "
        if act == "clear":
            S.push(S_id, "")
        elif act == "stat":
            for c in cr:
                name = self.iptvka.x_title[c]
                if self.btnT[c].get_active():
                    d = len(list(set([L[r][c] for r in range(Lnr) if L[r][c]])))
                    u += name + " = " + str(d) + "   |   "
        S.push(S_id, u)
