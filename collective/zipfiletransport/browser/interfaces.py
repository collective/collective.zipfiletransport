##################################################################################
#    Copyright (C) 2007 Utah State University, All rights reserved.          
#                                                                                 
#    This program is free software; you can redistribute it and/or modify         
#    it under the terms of the GNU General Public License as published by         
#    the Free Software Foundation; either version 2 of the License, or            
#    (at your option) any later version.                                          
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

__author__ = 'David Ray, Jon Thomas, Brent Lambert'
__docformat__ = 'restructuredtext'
__version__ = "$Revision: 1 $"[11:-2]


from zope.publisher.interfaces.browser import IBrowserView
from zope.app.file.interfaces import IFile
from zope.interface import Interface, Attribute
from zope import schema
from collective.zipfiletransport.schemas import ZipFileLine
from collective.zipfiletransport import ZipFileTransportMessageFactory
from Products.CMFPlone import PloneMessageFactory as _

class IExport(Interface):
    """ Export Form """
    filename = schema.TextLine(title=_(u"Zip File Export"),
                           description=_(u"The name of the file downloaded to your local machine."),
                           required=True)

class IImport(Interface):
    """ Import Form """

    description = schema.Text(title=_(u"Description"),
                              description=_(u"A description which will be given to each file in the ZIP archive."),
                              required=False)

    contributors = schema.Text(title=_(u"Contributors"),
                              description=_(u"The names of people that have contributed to this item.  Each contributor should be on a separate line."),
                              required=False)

    categories = schema.Text(title=_(u"Categories"),
                              description=_(u"Also known as keywords, tags or labels, these help you categorize your content. Each category should be on a separate line."),
                              required=False)


    overwrite = schema.Bool(title=_(u"Overwrite"),
                            description=_(u"Check this box to overwrite existing files with the same name."),
                            default=False, 
                            required=False)

    excludefromnav = schema.Bool(title=_(u"Exclude from navigation"),
                                 description=_(u"If selected, this item will not appear in the navigation tree."),
                                 default=False,
                                 required=False)


    filename = ZipFileLine(title=_(u"Zip File"),
                           description=_(u"Select the ZIP archive file to be uploaded by clicking the 'Browser' button."),
                           required=True)

