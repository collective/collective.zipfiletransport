# -*- coding: utf-8 -*-
##################################################################################
#    Copyright (c) 2004-2009 Utah State University, All rights reserved.
#    Portions copyright 2009 Massachusetts Institute of Technology, All rights reserved.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
##################################################################################

__author__  = '''Brent Lambert, David Ray, Jon Thomas'''
__version__   = '$ Revision 0.0 $'[11:-2]
from Products.Five import BrowserView
from zope.app.form.browser.textwidgets import TextWidget
from collective.zipfiletransport.browser.interfaces import IExport


class ExportWidgetExtension(BrowserView):

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.description = IExport(self.context).description


class ExportWidget(TextWidget):
    """ Widget for Export Form. """
    description = ""

    def __init__(self, field, request):
        """ Initialize the widget.  """
        super(ExportWidget, self).__init__(field, request)

    def __call__(self):
        widgettext = TextWidget.__call__(self)
        widget_extension = self.context.context.context.restrictedTraverse('@@export_widget')
        widgettext += widget_extension()
        return widgettext
