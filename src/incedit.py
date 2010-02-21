#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# incedit.py - main app file
# Copyright (C) Kuleshov Alexander 2010 <kuleshovmail@gmail.com>
# 
# main.py is free software: you can redistribute it and/or modify it
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
import utils
 
#
#Main class
#
class Incedit:
 
    opened_files = []
   
    def __init__(self):
 
        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_window.set_size_request(800,600)
        self.main_window.set_position(gtk.WIN_POS_CENTER)	
        self.main_window.set_title("Incedit")
 
        self.vbox = gtk.VBox(homogeneous = False, spacing = 0)
       
        self.init_menu()
        self.initializeEditor()
        self.init_tab_buttons() 
        self.init_toolbar()
        
        self.main_window.add(self.vbox)
         
        self.tab_panel.new_tab("New File")
 
        self.main_window.show_all()
    #
    # application menu
    #    
    def init_menu(self):  
        agr = gtk.AccelGroup()
        self.main_window.add_accel_group(agr)
 
        self.separator1 = gtk.SeparatorMenuItem()
        self.separator2 = gtk.SeparatorMenuItem()
        self.separator3 = gtk.SeparatorMenuItem()
 
        #ain menu
        self.main_menu = gtk.MenuBar()
        
        #menu item's
        self.file_menu           = gtk.Menu()
        self.open_menu           = gtk.Menu()     
        self.save_menu           = gtk.Menu()   
        self.save_as_menu        = gtk.Menu()
        self.close_file_menu     = gtk.Menu()
        self.exit_menu           = gtk.Menu()
 
        #add sub-menu menu items
        self.file_item = gtk.MenuItem("File")
        self.file_item.set_submenu(self.file_menu)
        
        self.open_item = gtk.MenuItem("Open")
        self.open_item.set_submenu(self.open_menu)
    
        self.save_item = gtk.MenuItem("Save")
        self.save_item.set_submenu(self.save_menu)          
        
        self.save_as_item = gtk.MenuItem("Save as")
        self.save_as_item.set_submenu(self.save_as_menu)
        
        self.close_file_item = gtk.MenuItem("Close file")
        self.close_file_item.set_submenu(self.close_file_menu)
        
        self.exit_file_item = gtk.MenuItem("Exit")
        self.exit_file_item.set_submenu(self.exit_menu)
 
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
 
        self.file_close = gtk.ImageMenuItem(gtk.STOCK_CLOSE,agr)
        key, mod = gtk.accelerator_parse("<Control>w")
        self.file_close.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
  
        self.file_exit = gtk.ImageMenuItem(gtk.STOCK_QUIT,agr)
        key, mod = gtk.accelerator_parse("<Control>q")
        self.file_exit.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
 
        # add menu
        self.file_menu.append(self.file_new)
        self.file_menu.append(self.file_open)       
        self.file_menu.append(self.separator1)
        self.file_menu.append(self.file_save)
        self.file_menu.append(self.file_save_as)
        self.file_menu.append(self.separator2)
        self.file_menu.append(self.file_close)
        self.file_menu.append(self.separator3)
        self.file_menu.append(self.file_exit) 
 
        self.main_menu.append(self.file_item)
         
        #signals
        self.file_new.connect("activate",self.new_file)
        self.file_open.connect("activate",self.open_file)
        self.file_save.connect("activate",self.save_file)
        self.file_save_as.connect("activate",self.save_as_file)
        self.file_close.connect("activate",self.close_file)
        self.file_exit.connect("activate",self.exit)
 
        self.vbox.pack_start(self.main_menu, False, False, 0)
 
    #
    # Init editor's elements
    #
    def initializeEditor(self):
        self.tab_panel = tab.Tab()
 
        self.statusbar = gtk.Statusbar()
 
        self.toolbar   = gtk.Toolbar()   
 
        self.toolbutton = gtk.Button() 
 
        self.textbuffer = gtk.TextBuffer()  
         
        self.vbox.pack_start(self.toolbar,False,False,0)
        self.vbox.add(self.tab_panel)
        self.vbox.pack_start(self.statusbar,False,False,0)
    
    #
    #tab close buttons
    #
    def init_tab_buttons(self): 
        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        image_w, image_h = gtk.icon_size_lookup(gtk.ICON_SIZE_MENU)
 
        self.toolbutton.set_relief(gtk.RELIEF_NONE)
        self.toolbutton.set_size_request(image_w+2, image_h+2)
        self.toolbutton.add(close_image)
    #
    #ToolBar
    #
    def init_toolbar(self):
        self.create_bar = gtk.ToolButton(gtk.STOCK_NEW)
        self.open_bar   = gtk.ToolButton(gtk.STOCK_OPEN)
        self.save_bar   = gtk.ToolButton(gtk.STOCK_SAVE)        
 
        self.toolbar.insert(self.create_bar,0)
        self.toolbar.insert(self.open_bar,1)
        self.toolbar.insert(self.save_bar,2)
 
        #toolbar signals
        self.create_bar.connect("clicked",self.new_file)
        self.open_bar.connect("clicked",self.open_file)
        self.save_bar.connect("clicked",self.save_as_file)
    #
    # add new file
    #
    def new_file(self,widget):
        pages_num = self.tab_panel.get_n_pages()
 
        self.tab_panel.new_tab("New File")      
        self.main_window.show_all() 
        
        self.tab_panel.set_current_page(self.tab_panel.get_n_pages() - 1) 
    #
    #Open file
    #
    def open_file(self,param = 1):
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
        return file_name    
  
    #
    #Save file
    #
    def save_file(self,widget):
        tab.Tab.save_file(self.tab_panel)
 
    #
    #Save as file
    #
    def save_as_file(self,widget):
        tab.Tab.save_as_file(self.tab_panel)
        self.main_window.show_all()
 
    #
    #quit application
    #
    def exit(self,widget):
        gtk.main_quit()
 
    #
    #close file
    #
    def close_file(self,child):
         tab.Tab.close_tab(self.tab_panel,child)
         self.main_window.show_all()
 
    #
    #MAIN
    #
    def main(self):
        gtk.main()
 
if __name__ == "__main__":
	Win = Incedit()
	Win.main()
