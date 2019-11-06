# -*- coding: utf-8 -*-
##################################################################################
#    Copyright (c) 2004-2009 Utah State University, All rights reserved.
#    Portions copyright 2009 Massachusetts Institut of Technology, All rights reserved.
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
from Products.CMFCore.utils import getToolByName

__author__  = '''Brent Lambert, David Ray, Jon Thomas'''
__version__   = '$ Revision 0.0 $'[11:-2]
import logging
import os

from collective.zipfiletransport import ZipFileTransportMessageFactory as _
from collective.zipfiletransport.browser.interfaces import IExport
from collective.zipfiletransport.utilities.interfaces import IZipFileTransportUtility

from plone.app.form.base import EditForm
from widgets import ExportWidget
from zope.component import getUtility
from zope.formlib.form import FormFields, action
from zope.interface import implements


logger = logging.getLogger('zipfiletransport.export')
RESPONSE_BLOCK_SIZE = 32768


class ExportFormAdapter(object):
    """ Adapter for the export form """

    implements(IExport)

    description = _(u'All files in the folder will be exported in .zip file format')
    label = _(u'Export Content')

    def __init__(self, context):
        self.context = context

    def get_zipfile_name(self):
        return self.context.id + '.zip'

    def set_zipfile_name(self, title):
        pass

    filename = property(get_zipfile_name, set_zipfile_name)

    def get_brains(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog.searchResults(
            path={'query': ('/'.join(self.context.getPhysicalPath()))},
            is_folderish=False
        )


class ATTopicExportFormAdapter(ExportFormAdapter):

    description = _(u'All files that matches the topic criteria will be exported in .zip file format')

    def get_brains(self):
        return self.context.queryCatalog()


class ExportForm(EditForm):
    """ Render the export form  """
    implements(IExport)

    form_fields = FormFields(IExport)
    form_fields['filename'].custom_widget = ExportWidget

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.adapter = IExport(context)
        self.zft_util = getUtility(IZipFileTransportUtility, name="zipfiletransport")
        self.description = self.adapter.description
        self.label = self.adapter.label

    @action(_(u'Export'))
    def action_export(self, action, data):
        logger.debug("Discover Object Paths in hidden form fields")
        try:
            paths = self.request['form.obj_paths']
            obj_paths = []
            for x in paths:
                x = x.encode('utf-8')
                obj_paths += [x]
        except KeyError:
            obj_paths = None

        filename = self.request['form.filename']
        if filename.find('.zip') == -1:
            filename += ".zip"

        ## Why ? 
        #if self.context.portal_membership.isAnonymousUser() != 0:
        #    return
        ## XX should use a permission

        zipfilename = self.zft_util.generateSafeFileName(filename).encode('utf-8')
        brains = self.adapter.get_brains()
        zip_path = self.zft_util.exportContent(
            context=self.context,
            brains=brains,
            obj_paths=obj_paths,
            filename=filename,
        )

        response = self.request.RESPONSE

        response.setHeader('content-type', 'application/zip')
        response.setHeader('content-length', str(os.stat(zip_path)[6]))
        response.setHeader('Content-Disposition',
                           'attachment; filename=' + zipfilename)

        # iterate over the temporary file object, returning it to the client
        with open(zip_path, 'rb') as fp:
            while True:
                data = fp.read(RESPONSE_BLOCK_SIZE)
                if data:
                    response.write(data)
                else:
                    break

        try:
            os.unlink(zip_path)
        except Exception, e:
            logger.warning('Cannot remove %s: %s' % (zip_path, e))

