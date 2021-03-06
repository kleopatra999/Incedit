#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# print.py - provide file printing
# Copyright (C) Kuleshov Alexander 2010 <kuleshovmail@gmail.com>
# 
# main.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# main.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without esavingven the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 

import gtk

#
#print document class
#
class PrintDoc:
    def __init__(self, action=None, data=None, filename=None):
   
        self.text = data
        self.layout = None
        self.font_size=12
        self.lines_per_page=0
   
        if action==None:
            action = gtk.PRINT_OPERATION_ACTION_PREVIEW
    
        paper_size = gtk.PaperSize(gtk.PAPER_NAME_A4)
        
        setup = gtk.PageSetup()
        setup.set_paper_size(paper_size)
        
        print_ = gtk.PrintOperation()
        print_.set_default_page_setup(setup)
        print_.set_unit(gtk.UNIT_MM)
        print_.connect("begin_print", self.begin_print)
        print_.connect("draw_page", self.draw_page)
    
        if action == gtk.PRINT_OPERATION_ACTION_EXPORT:
            print_.set_export_filename(filename)
            
        response = print_.run(action)
        
    def begin_print(self, operation, context):
    
        width = context.get_width()
        height = context.get_height()

        self.layout = context.create_pango_layout()
        self.layout.set_font_description(
      
        pango.FontDescription("Sans " + str(self.font_size)) )
 
        self.layout.set_width(int(width*pango.SCALE))
        self.layout.set_text(self.text)
 
        num_lines = self.layout.get_line_count()
      
        self.lines_per_page = math.floor(context.get_height() / (self.font_size/2) )
        pages = ( int(math.ceil( float(num_lines) / float(self.lines_per_page))))
 
        operation.set_n_pages(pages)
        
    def draw_page (self, operation, context, page_number):
 
        cr = context.get_cairo_context()
        cr.set_source_rgb(0, 0, 0)
  
        start_line = page_number * self.lines_per_page
  
        if page_number + 1 != operation.props.n_pages:
            end_line = start_line + self.lines_per_page
        else:
            end_line = self.layout.get_line_count()
   
        cr.move_to(0, 0)
    
        iter = self.layout.get_iter()
        i=0
   
        while 1:
            if i > start_line:
                line = iter.get_line()
                cr.rel_move_to(0, self.font_size/2)
                cr.show_layout_line(line)
            i += 1
            if not (i < end_line and iter.next_line()):
                break



 
