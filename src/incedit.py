#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# incedit.py - main app file
# Copyright (C) Kuleshov Alexander 2010 <kuleshovmail@gmail.com>
# 
# Incedit is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# main.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
import pygtk
pygtk.require('2.0')
import gtk
import tab
import about 
import printer
import sep
import toolbar
import undostack
import utils

class Incedit:
    
    vbox = gtk.VBox(homogeneous = False, spacing = 0)
    main_window = gtk.Window()
    FIND = 1
    opened_files = []

    def __init__(self):
       
        self.main_window.set_size_request(800,600)
        self.main_window.set_position(gtk.WIN_POS_CENTER)	
        self.main_window.set_title("Incedit")

        self.init_menu()
        self.init_tab()
        self.initializeEditor()
        self.toolbar.init_toolbar()

        self.main_window.add(self.vbox)
         
        self.tab_panel.new_tab("New File")
        
        self.textview = tab.Tab.editor_access(self.tab_panel)
        self.textbuffer = self.textview.get_buffer()

        self.statusbar = gtk.Statusbar()
        self.vbox.pack_end(self.statusbar,False,False)
        
        self.main_window.show_all()

    # application menu  
    def init_menu(self):  
        agr = gtk.AccelGroup()
        self.main_window.add_accel_group(agr)
 
        self.sep = sep.SeparatorStruct()
        self.main_menu = gtk.MenuBar()
        
        #file menu items
        self.file_menu           = gtk.Menu()
        self.open_menu           = gtk.Menu()     
        self.save_menu           = gtk.Menu()   
        self.save_as_menu        = gtk.Menu()
        self.print_menu          = gtk.Menu()
        self.close_file_menu     = gtk.Menu()
        self.exit_menu           = gtk.Menu()
 
        #edit menu items
        self.edit_menu           = gtk.Menu()
        self.undo_menu           = gtk.Menu()
        self.redo_menu           = gtk.Menu()
        self.cut_menu            = gtk.Menu()
        self.copy_menu           = gtk.Menu()
        self.paste_menu          = gtk.Menu()
        self.delete_menu         = gtk.Menu()
        self.select_all_menu     = gtk.Menu()

        #view menu items
        self.view_menu           = gtk.Menu()
        self.show_toolbar_menu   = gtk.Menu()
        self.show_statusbar_menu = gtk.Menu()        

        #search menu
        self.search_menu         = gtk.Menu()
        self.search_text_menu    = gtk.Menu()

        #about menu
        self.about_menu          = gtk.Menu()
        self.about_form_menu     = gtk.Menu()

        #add sub-menu menu items
        self.file_item = gtk.MenuItem("File")
        self.file_item.set_submenu(self.file_menu)
        self.open_item = gtk.MenuItem("Open")
        self.open_item.set_submenu(self.open_menu)
        self.save_item = gtk.MenuItem("Save")
        self.save_item.set_submenu(self.save_menu)          
        self.save_as_item = gtk.MenuItem("Save as")
        self.save_as_item.set_submenu(self.save_as_menu)
        self.print_item = gtk.MenuItem("Print")
        self.print_item.set_submenu(self.print_menu)
        self.close_file_item = gtk.MenuItem("Close file")
        self.close_file_item.set_submenu(self.close_file_menu)
        self.exit_file_item = gtk.MenuItem("Exit")
        self.exit_file_item.set_submenu(self.exit_menu)

        self.edit_item = gtk.MenuItem("Edit")
        self.edit_item.set_submenu(self.edit_menu)
        self.undo_item = gtk.MenuItem("Undo")
        self.undo_item.set_submenu(self.undo_menu)
        self.redo_item = gtk.MenuItem("Redo")
        self.redo_item.set_submenu(self.redo_menu)
        self.cut_item  = gtk.MenuItem("Cut")
        self.cut_item.set_submenu(self.cut_menu)
        self.copy_item = gtk.MenuItem("Copy")
        self.copy_item.set_submenu(self.copy_menu)
        self.paste_item = gtk.MenuItem("Paste")
        self.paste_item.set_submenu(self.paste_menu)
        self.delete_item = gtk.MenuItem("Delete")
        self.delete_item.set_submenu(self.delete_menu)
        self.select_all_item = gtk.MenuItem("Select All")
        self.select_all_item.set_submenu(self.select_all_menu)

        self.view_item = gtk.MenuItem("View")
        self.view_item.set_submenu(self.view_menu)
        self.show_toolbar_item = gtk.MenuItem("Show toolbar")
        self.show_toolbar_item.set_submenu(self.show_toolbar_menu)
        self.show_statusbar_item = gtk.MenuItem("Show statusbar")
        self.show_statusbar_item.set_submenu(self.show_statusbar_menu)

        self.search_item = gtk.MenuItem("Search")
        self.search_item.set_submenu(self.search_menu)
        self.search_text_item = gtk.MenuItem("Search text")
        self.search_text_item.set_submenu(self.search_text_menu)

        self.statusbar_check_menu = gtk.CheckMenuItem("Show StatusBar")
        self.statusbar_check_menu.set_active(True)
        self.toolbar_check_menu = gtk.CheckMenuItem("Show ToolBar")
        self.toolbar_check_menu.set_active(True)

        self.about_menu_item = gtk.MenuItem("About")
        self.about_menu_item.set_submenu(self.about_menu)
        self.about_form_menu_item = gtk.MenuItem("About")
        self.about_form_menu_item.set_submenu(self.about_form_menu)

        #image file menu items
        self.file_new = gtk.ImageMenuItem(gtk.STOCK_NEW, agr)
        key,mod = gtk.accelerator_parse("<Control>n")
        self.file_new.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
 
        self.file_open = gtk.ImageMenuItem(gtk.STOCK_OPEN,agr)
        key,mod = gtk.accelerator_parse("<Control>o")
        self.file_open.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        
        self.file_save = gtk.ImageMenuItem(gtk.STOCK_SAVE,agr)
        key, mod = gtk.accelerator_parse("<Control>s")
        self.file_save.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
 
        self.file_save_as = gtk.ImageMenuItem(gtk.STOCK_SAVE_AS,agr)
        key, mod = gtk.accelerator_parse("<Shift><Control>s")
        self.file_save_as.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        self.file_print = gtk.ImageMenuItem(gtk.STOCK_PRINT,agr)
        key, mod = gtk.accelerator_parse("<Control>p")
        self.file_print.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
  
        self.file_close = gtk.ImageMenuItem(gtk.STOCK_CLOSE,agr)
        key, mod = gtk.accelerator_parse("<Control>w")
        self.file_close.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
  
        self.file_exit = gtk.ImageMenuItem(gtk.STOCK_QUIT,agr)
        key, mod = gtk.accelerator_parse("<Control>q")
        self.file_exit.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
 
        self.edit_undo = gtk.ImageMenuItem(gtk.STOCK_UNDO, agr)
        key,mod = gtk.accelerator_parse("<Control>z")
        self.edit_undo.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        self.edit_redo = gtk.ImageMenuItem(gtk.STOCK_REDO, agr)
        key,mod = gtk.accelerator_parse("<Control>r")
        self.edit_redo.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        self.edit_paste = gtk.ImageMenuItem(gtk.STOCK_PASTE, agr)
        key,mod = gtk.accelerator_parse("<Control>v")
        self.edit_paste.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        self.edit_copy = gtk.ImageMenuItem(gtk.STOCK_COPY, agr)
        key,mod = gtk.accelerator_parse("<Control>c")
        self.edit_copy.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        self.edit_cut = gtk.ImageMenuItem(gtk.STOCK_CUT, agr)
        key,mod = gtk.accelerator_parse("<Control>x")
        self.edit_cut.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        self.edit_delete = gtk.ImageMenuItem(gtk.STOCK_DELETE, agr)
        key,mod = gtk.accelerator_parse("<Control>e")
        self.edit_delete.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        self.edit_select_all = gtk.ImageMenuItem("Select All",agr)
        key,mod = gtk.accelerator_parse("<Control>a")
        self.edit_select_all.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        self.search_search_text = gtk.ImageMenuItem("Find...",agr)
        key,mod = gtk.accelerator_parse("<Control>f")
        self.search_search_text.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        self.about = gtk.ImageMenuItem("About",agr)
        key,mod = gtk.accelerator_parse("<ALT>A")
        self.about.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        # add menu
        self.file_menu.append(self.file_new)
        self.file_menu.append(self.file_open)       
        self.file_menu.append(self.sep.separator1)
        self.file_menu.append(self.file_save)
        self.file_menu.append(self.file_save_as)
        self.file_menu.append(self.sep.separator2)
        self.file_menu.append(self.file_print)
        self.file_menu.append(self.sep.separator7)
        self.file_menu.append(self.file_close)
        self.file_menu.append(self.sep.separator3)
        self.file_menu.append(self.file_exit) 

        self.edit_menu.append(self.edit_undo)
        self.edit_menu.append(self.edit_redo)
        self.edit_menu.append(self.sep.separator4)
        self.edit_menu.append(self.edit_copy)
        self.edit_menu.append(self.edit_paste)
        self.edit_menu.append(self.edit_cut) 
        self.edit_menu.append(self.sep.separator5)
        self.edit_menu.append(self.edit_delete)
        self.edit_menu.append(self.sep.separator6)
        self.edit_menu.append(self.edit_select_all)
    
        self.view_menu.append(self.statusbar_check_menu)
        self.view_menu.append(self.toolbar_check_menu)

        self.search_menu.append(self.search_search_text)

        self.about_menu.append(self.about)

        self.main_menu.append(self.file_item)
        self.main_menu.append(self.edit_item)
        self.main_menu.append(self.view_item)
        self.main_menu.append(self.search_item) 
        self.main_menu.append(self.about_menu_item)

        self.file_new.connect("activate",self.new_file)
        self.file_open.connect("activate",self.open_file)
        self.file_save.connect("activate",self.save_file)
        self.file_save_as.connect("activate",self.save_as_file)
        self.file_print.connect("activate",self.print_file)
        self.file_close.connect("activate",self.close_file)
        self.file_exit.connect("activate",self.exit)

        self.edit_undo.connect("activate", self.on_undo)
        self.edit_redo.connect("activate", self.on_redo)
        self.edit_copy.connect("activate", self.copy)
        self.edit_cut.connect("activate", self.cut)
        self.edit_paste.connect("activate", self.paste)
        self.edit_delete.connect("activate", self.delete)   
        self.edit_select_all.connect("activate", self.select)

        self.statusbar_check_menu.connect("activate",  self.statusbar_show) 
        self.toolbar_check_menu.connect("activate", self.toolbar_show) 

        self.search_search_text.connect("activate",self.show_find_box)

        self.about.connect("activate",self.show_about)
 
        self.vbox.pack_start(self.main_menu, False, False, 0)
 
    def init_tab(self):  
        self.tab_panel = tab.Tab()
        return self.tab_panel

    #
    # Init editor's elements
    #
    def initializeEditor(self):
        self.toolbar   = toolbar.ToolBar()   
 
        self.toolbutton = gtk.Button() 
 
        self.textbuffer = gtk.TextBuffer()  

        self.find_box   = gtk.HBox() 

        #element for find box
        self.text_to_find = gtk.Entry()
        self.text_to_find.set_size_request(500,26)
        find_button = gtk.Button()
        image_find =  gtk.Image()
        image_find.set_from_stock(gtk.STOCK_FIND,gtk.ICON_SIZE_SMALL_TOOLBAR)
        find_button.set_image(image_find)
        find_button.set_relief(gtk.RELIEF_NONE) 
        close_button  = gtk.Button() 
        image_close =  gtk.Image()
        image_close.set_from_stock(gtk.STOCK_CLOSE,gtk.ICON_SIZE_SMALL_TOOLBAR)
        close_button.set_image(image_close)
        close_button.set_relief(gtk.RELIEF_NONE)
        self.find_next_button = gtk.Button("Find next")
        self.find_next_button.set_relief(gtk.RELIEF_NONE)
        
        self.find_box.pack_start(self.text_to_find,False,False,2)
        self.find_box.pack_start(find_button,False,False,4)
        self.find_box.pack_end(close_button,False,False,2)
        self.find_box.pack_start(self.find_next_button,False,False,5)
        self.find_next_button.set_sensitive(False)
 
        self.vbox.pack_start(self.toolbar,False,False,0)
        self.vbox.add(self.tab_panel)   
        
        toolbar.ToolBar.create_bar.connect("clicked",self.new_file)
        toolbar.ToolBar.open_bar.connect("clicked",self.open_file)
        toolbar.ToolBar.save_bar.connect("clicked",self.save_as_file)
        toolbar.ToolBar.print_bar.connect("clicked",self.print_file)
        toolbar.ToolBar.undo_bar.connect("clicked",self.on_undo)
        toolbar.ToolBar.redo_bar.connect("clicked",self.on_redo)
        toolbar.ToolBar.find_bar.connect("clicked",self.show_find_box)        

        find_button.connect("clicked",self.find)
        close_button.connect("clicked",self.hide_find_box)
        self.find_next_button.connect("clicked",self.find_next)
        
        return self.tab_panel

    # add new file
    def new_file(self,widget):
        pages_num = self.tab_panel.get_n_pages()
 
        self.tab_panel.new_tab("New File")      
        self.main_window.show_all() 
        
        self.tab_panel.set_current_page(self.tab_panel.get_n_pages() - 1) 

    #Open file
    def open_file(self,widget):
        pages_num = self.tab_panel.get_n_pages()
 
        dialog = gtk.FileChooserDialog("Open file..",None,gtk.FILE_CHOOSER_ACTION_OPEN,
                                      (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                       gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
 
        txt_filter=gtk.FileFilter()
        txt_filter.set_name("Text files")
        txt_filter.add_mime_type("text/*")
        all_filter=gtk.FileFilter()
        all_filter.set_name("All files")
        all_filter.add_pattern("*")
 
        dialog.add_filter(txt_filter)
        dialog.add_filter(all_filter)
        
        response = dialog.run()
 
        if response == gtk.RESPONSE_OK: 
            file_name = dialog.get_filename()
            self.tab_panel.set_current_page(pages_num)    
            self.tab_panel.new_tab(str(utils.cut_file_name(dialog.get_filename()))).set_buffer(self.textbuffer)
            self.textbuffer.set_text(open(dialog.get_filename()).read())
 
            self.main_window.set_title(utils.cut_file_name(dialog.get_filename()))
            self.statusbar.push(1,dialog.get_filename()) 
            self.main_window.show_all()  
            
            self.tab_panel.set_current_page(self.tab_panel.get_n_pages() - 1) 
            self.main_window.show_all()
 
            self.opened_files.append(self.tab_panel.get_current_page())
 
            tab.Tab.already_save.insert(self.tab_panel.get_current_page(),file_name)             
 
        elif response == gtk.RESPONSE_CANCEL:
            dialog.destroy()
        
        dialog.destroy() 
  
    #Save file
    def save_file(self,widget):
        tab.Tab.save_file(self.tab_panel,widget)
 
    #Save as file
    def save_as_file(self,widget):
        tab.Tab.save_as_file(self.tab_panel)

    #quit application
    def exit(self,widget):
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
                                   "Do you want to save current file and qiut?")
        dialog.set_title("Close file!")
        response = dialog.run()
        
        if response == gtk.RESPONSE_YES:
           tab.Tab.save_as_file(self.tab_panel)
        else:
           gtk.main_quit()
 
    #toolbar show/hide
    def toolbar_show(self,widget):
         if widget.active: 
             self.toolbar.show()
         else:
             self.toolbar.hide()

    #statusbar show/hide
    def statusbar_show(self,widget):
         if widget.active: 
             self.statusbar.show()
         else: 
             self.statusbar.hide()

    #close file
    def close_file(self,child):
         widget = self.tab_panel
         tab.Tab.close_tab(self.tab_panel,widget,child) 

    #undo provide
    def on_undo(self,widget):
         textview = tab.Tab.editor_access(self.tab_panel)
         textbuffer = textview.get_buffer()
         textbuffer.undo() 
       
    #redo provide
    def on_redo(self,widget):
         textview = tab.Tab.editor_access(self.tab_panel)
         textbuffer = textview.get_buffer()
         textbuffer.redo() 
    
    #copy/paste/cut/delete/select_all
    def copy(self,widget):
        tab.Tab.copy_buffer(self.tab_panel,widget)    

    def cut(self,widget):
        tab.Tab.cut_buffer(self.tab_panel,widget)   

    def paste(self,widget):
        tab.Tab.paste_buffer(self.tab_panel,widget)   
  
    def delete(self,widget):
         tab.Tab.delete_buffer(self.tab_panel,widget)
   
    def select(self,widget):
         tab.Tab.select_all(self.tab_panel,widget)   

    #print file
    def print_file(self,widget):
        textview = tab.Tab.editor_access(self.tab_panel)
        textbuffer = textview.get_buffer()
        prining = printer.PrintDoc(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG,textbuffer.get_text(textbuffer.get_start_iter(),
                                                                                               textbuffer.get_end_iter()))

    #find text provide
    def show_find_box(self,widget): 
          if self.FIND % 2 == 1:
             self.vbox.pack_start(self.find_box,False,False,4)
             self.FIND = self.FIND + 1
             self.main_window.show_all()
             return
          else:
             self.vbox.remove(self.find_box)
             self.FIND = self.FIND + 1
             return
    #find
    def find(self,widget):
         self.textview = tab.Tab.editor_access(self.tab_panel)
         self.textbuffer = self.textview.get_buffer()
         self.search_str =  self.text_to_find.get_text()
         
         start_iter =  self.textbuffer.get_start_iter() 
         self.match_start = self.textbuffer.get_start_iter() 
         self.match_end =   self.textbuffer.get_end_iter() 

         found = start_iter.forward_search(self.search_str,0, None)
         
         if found: 
             self.match_start,self.match_end = found               
             self.textbuffer.select_range(self.match_start,self.match_end)  
             self.last_pos = self.textbuffer.create_mark('last_pos', self.match_end, False)    
             self.find_next_button.set_sensitive(True)
         else:
             utils.dialog_text_not_find()
             self.text_to_find.set_text("")    
             self.find_next_button.set_sensitive(False)

    def find_next(self,widget):
         last_pos = self.textbuffer.get_mark('last_pos')
         if last_pos == None:
             return
         else:
             last_search_iter = self.textbuffer.get_iter_at_mark(last_pos)
         found = last_search_iter.forward_search(self.search_str,0, None)
     
         if found:
             self.match_start,self.match_end = found   
             self.textbuffer.select_range(self.match_start,self.match_end)
             self.last_pos = self.textbuffer.create_mark('last_pos', self.match_end, False) 
         else:
             utils.dialog_text_not_find()
             self.text_to_find.set_text("")
             self.find_next_button.set_sensitive(False)
     
    #About form
    def show_about(self,widget):
         about.on_clicked(widget)

    #hide find box
    def hide_find_box(self,widget):
         self.vbox.remove(self.find_box)
         self.FIND = self.FIND + 1
         self.text_to_find.set_text("")
         self.find_next_button.set_sensitive(False)
         return
   

    def main(self):
        gtk.main()
 
if __name__ == "__main__":
	Win = Incedit()
	Win.main()
