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
__version__ = '$ Revision 0.0 $'[11:-2]

from zope.interface import Interface, implements
from zope.component import adapts, getUtility
from zope.formlib import form
from zope.schema import TextLine, Bool
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.zipfiletransport import ZipFileTransportMessageFactory as _
from Products.CMFCore.interfaces import IPropertiesTool
from plone.app.controlpanel.form import ControlPanelForm


class IZipFileTransportPrefsForm(Interface):
    """ The view for zipfile transport prefs form. """

    image_type = TextLine(title=_(u'Image Type'),
                          description=_(u'Set the image type here. Images imported via ZipFileTransport '
                                        'will be instantiated as an object of this type.'),
                          required=True)

    file_type = TextLine(title=_(u'File Type'),
                         description=_(u'Set your file type here. Files imported via ZipFileTransport '
                                       'will be instantiated as an object of this type'),
                         required=True)

    doc_type = TextLine(title=_(u'Document Type'),
                        description=_(u'Set your document type here. Documents imported via ZipFileTransport '
                                      'will be instantiated as an object of this type.'),
                        required=True)

    folder_type = TextLine(title=_(u'Folder Type'),
                           description=_(u'Set your folderish type here. Folders imported via ZipFileTransport '
                                         'will be instantiated as an object of this type'),
                           required=True)

    name_by_title = Bool(title=_('Name Objects By Title'),
                         description=_(u'Use an object''s title as filename in ZIP export instead of ID.'),
                         required=False)

    allow_zip64 = Bool(title=_(u"Allow Zip64"),
                       description=_(u"Allow ZIP64 library. This is required if you want to allow handling of zipfiles larger than 2Go"),
                       default=False,
                       required=False)


class ZipFileTransportControlPanelAdapter(SchemaAdapterBase):
    """ Control Panel adapter """

    adapts(IPloneSiteRoot)
    implements(IZipFileTransportPrefsForm)

    def __init__(self, context):
        super(ZipFileTransportControlPanelAdapter, self).__init__(context)
        pprop = getUtility(IPropertiesTool)
        self.zf_props = pprop.zipfile_properties

    def get_image_type(self):
        return self.zf_props.image_type

    def set_image_type(self, image_type):
        self.zf_props.image_type = image_type

    def get_file_type(self):
        return self.zf_props.file_type

    def set_file_type(self, file_type):
        self.zf_props.file_type = file_type

    def get_doc_type(self):
        return self.zf_props.doc_type

    def set_doc_type(self, doc_type):
        self.zf_props.doc_type = doc_type

    def get_folder_type(self):
        return self.zf_props.folder_type

    def set_folder_type(self, folder_type):
        self.zf_props.folder_type = folder_type

    def get_name_by_title(self):
        return self.zf_props.name_by_title

    def set_name_by_title(self, value):
        self.zf_props.name_by_title = value

    def get_allow_zip64(self):
        return self.zf_props.allow_zip64

    def set_allow_zip64(self, allow_zip64):
        self.zf_props.allow_zip64 = allow_zip64

    image_type = property(get_image_type, set_image_type)
    file_type = property(get_file_type, set_file_type)
    doc_type = property(get_doc_type, set_doc_type)
    folder_type = property(get_folder_type, set_folder_type)
    name_by_title = property(get_name_by_title, set_name_by_title)
    allow_zip64 = property(get_allow_zip64, set_allow_zip64)


class ZipFileTransportPrefsForm(ControlPanelForm):
    """ The view class for the zipfile transport preferences form. """

    implements(IZipFileTransportPrefsForm)
    form_fields = form.FormFields(IZipFileTransportPrefsForm)

    label = _(u'ZipFileTransport Settings Form')
    description = _(u'Configure object type settings for imported objects.  These values should not be adjusted unless your site has overwritten '
                    'the default object types.')
    form_name = _(u'ZipFileTransport Settings')
