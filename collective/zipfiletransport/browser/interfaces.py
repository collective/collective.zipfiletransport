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

__author__ = '''Brent Lambert, David Ray, Jon Thomas'''
__version__  = '$ Revision 0.0 $'[11:-2]

from collective.zipfiletransport import ZipFileTransportMessageFactory as _
from collective.zipfiletransport.schemas import ZipFileLine

from zope import schema
from zope.interface import Interface


class IExport(Interface):
    """ Export Form """
    filename = schema.TextLine(
        title=_(u"Zip File Export"),
        description=_(u"The name of the file downloaded to your local machine."),
        required=True)

    def get_brains(self):
        """
        The list of brains to export
        :return:
        """


class IImport(Interface):
    """ Import Form """

    description = schema.Text(
                        title=_(u"Import Description"),
                        description=_(
                            u"A description which will be given to each file "
                            u"in the ZIP archive."),
                        required=False)

    contributors = schema.Text(
                        title=_(u"Contributors"),
                        description=_(
                            u"The names of people that have contributed to "
                            u"imported item(s).  Each contributor should be "
                            u"on a separate line."),
                        required=False)

    categories = schema.Text(
                        title=_(u"Keyword Categories"),
                        description=_(
                            u"Also known as keywords, tags or labels, these "
                            u"help you categorize your content. Each category "
                            u"should be on a separate line."),
                        required=False)

    overwrite = schema.Bool(
                        title=_(u"Overwrite"),
                        description=_(
                            u"Check this box to overwrite existing files with "
                            u"the same name. If left unchecked, same named "
                            u"files will not import."),
                        default=False,
                        required=False)

    excludefromnav = schema.Bool(
                        title=_(u"Exclude from left navigation"),
                        description=_(
                            u"If selected, imported item(s) will not appear "
                            u"in the navigation tree."),
                        default=False,
                        required=False)

    filename = ZipFileLine(
                        title=_(u"Zip File"),
                        description=_(
                            u"Select the ZIP archive file to be imported."),
                        required=True)
