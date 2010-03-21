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

from zope.formlib.form import FormFields, action
from Products.Five.formlib.formbase import EditForm
from zope.component import getUtility
from zope.interface import implements
from collective.zipfiletransport.utilities.interfaces import IZipFileTransportUtility
from collective.zipfiletransport.browser.interfaces import IExport
from widgets import ExportWidget
import os
import string
from collective.zipfiletransport import ZipFileTransportMessageFactory as _

class ExportFormAdapter(object):
    """ Adapter for the export form """

    implements(IExport)

    def __init__(self,context):
        self.context = context

    def get_zipfile_name(self):
        return self.context.id + '.zip'

    def set_zipfile_name(self, title):
        pass

    filename = property(get_zipfile_name, set_zipfile_name)
    

class ExportForm(EditForm):
    """ Render the export form  """

    implements(IExport)

    form_fields = FormFields(IExport)
    form_fields['filename'].custom_widget = ExportWidget

    label = _(u'Export Content')
    description = _(u'All files in the folder will be exported in .zip file format')


    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.zft_util = getUtility(IZipFileTransportUtility)


    @action(_(u'Export'))
    def action_export(self, action, data):
        RESPONSE_BLOCK_SIZE = 32768
        #Discover Object Paths in hidden form fields
        obj_paths = None
        try:
            self.context.REQUEST['form.obj_paths']
            paths = self.context.REQUEST['form.obj_paths']
            obj_paths = []
            for x in paths:
                x = x.encode('utf-8')
                obj_paths += [x]
        except:
            pass
        filename = self.context.REQUEST['form.filename']

        if string.find(filename,'.zip') == -1:
            filename += ".zip"

        if self.context.portal_membership.isAnonymousUser() != 0:
            return


        zipfilename = self.zft_util.generateSafeFileName(filename)
        #Detect OS
        zipfilename = filename.encode('utf-8')

        zip_path = self.zft_util.exportContent(context=self.context,obj_paths=obj_paths, filename=filename)

        self.context.REQUEST.RESPONSE.setHeader('content-type', 'application/zip')
        self.context.REQUEST.RESPONSE.setHeader('content-length', str(os.stat(zip_path)[6]))
        self.context.REQUEST.RESPONSE.setHeader('Content-Disposition',' attachment; filename='+zipfilename)


        # iterate over the temporary file object, returning it to the client
        fp = open(zip_path, 'rb')
        while True:
            data = fp.read(RESPONSE_BLOCK_SIZE)
            if data:
                self.context.REQUEST.RESPONSE.write(data)
            else:
                break
        fp.close()
        # temporary measure to see the file object...
        os.rename(zip_path, zip_path + "_TEMP")
        return
    


