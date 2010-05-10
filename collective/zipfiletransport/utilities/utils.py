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

import unicodedata
from os import close
from os.path import split, splitext
from urllib import unquote

from zope.component import queryUtility
from zope.interface import implements
try:
    from zope.site.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

from OFS.SimpleItem import SimpleItem

from Products.ATContentTypes import interfaces
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName

from plone.i18n.normalizer.interfaces import IURLNormalizer

from zipfile import ZipFile, ZIP_DEFLATED
from interfaces import IZipFileTransportUtility

class ZipFileTransportUtility(SimpleItem):
    """ ZipFileTransport Utility """

    implements(IZipFileTransportUtility)
    
    # Import content to a zip file.
    #
    # file          - The file input is a string of the full path name where 
    #                   the zip file is saved. 
    # context       - Context refers to the container object where the objects 
    #                   will be uploaded to.
    # desc          - Description is the description to be attached to the 
    #                   uploaded objects.
    # contributors - Contributors is the contributors message to be attached 
    #                   to the uploaded objects.
    def importContent(
                    self, 
                    file, 
                    context,
                    description=None, 
                    contributors=None, 
                    categories=None, 
                    overwrite=False, 
                    excludefromnav=False,
                    ):
        """ Import content from a zip file, creating the folder structure 
            within a ZODB hierarchy.
        """
        self.bad_folders = []        
        zf=ZipFile(file, 'r')
        files = [file.filename for file in zf.filelist]
        
        if len(files) < 1:
            return ('failure','The zip file was empty')        
        
        for current_file in files:
            # If the current file is a folder move to the next file.
            if current_file[-1] == '/':
                continue
            
            if current_file[0] == '/':            
                path_as_list = current_file[1:].split('/')
            else:
                path_as_list = current_file.split('/')

            file_name = self._convertToUnicode(path_as_list[-1])
            file_name = unicodedata.normalize('NFC', file_name )
            
            normalized_file_name = queryUtility(IURLNormalizer).normalize(file_name)
            
            # Checks to make sure that the file path does not contain any 
            # previouslsy found bad folders.
            if not self._checkFilePath(current_file, path_as_list):
                continue

            folder = self._createFolderStructure(path_as_list, context, excludefromnav)
            
            # no folder to add to? Then move on to next object.
            if not folder:
                continue

            id_available = folder.checkIdAvailable(id=normalized_file_name)
            
            # Create an object if everything looks good
            if id_available or overwrite:
                fdata = zf.read(current_file)
                
                if not id_available:
                    folder.manage_delObjects([normalized_file_name])
 
                obj = self._createObject(normalized_file_name, fdata, folder)

                if hasattr(obj,'description') and description:
                    obj.setDescription(description)
                if hasattr(obj,'contributors') and contributors:
                    obj.setContributors(contributors)
                if hasattr(obj,'subject') and categories:
                    obj.setSubject(categories)
                if excludefromnav:
                    obj.setExcludeFromNav(True)
                obj.reindexObject()
		obj.setTitle(file_name)
                obj.reindexObject()
        zf.close()   


    def _checkFilePath(self, current_file, path_as_list):
        """ Make sure file isn't in a bad folder, if it is skip to the next 
            one.
        """
        for bad_folder in self.bad_folders:
            if current_file.find(bad_folder) == 0:
                return False
        return True
        

    def _createFolderStructure(self, path_as_list, parent, excludefromnav):
        """ Creates the folder structure given a path_part and parent object 
        """
        props = getToolByName(parent, 'portal_properties')
        folder_type = props.zipfile_properties.folder_type
        catalog = getToolByName(parent, 'portal_catalog')
        factory = getToolByName(parent, 'portal_factory')

        file_name = self._convertToUnicode(path_as_list[-1])
        file_name = unicodedata.normalize('NFC', file_name )
        
        # Create the folder structure
        for i in range( len(path_as_list) - 1 ):
            path_part = self._convertToUnicode(path_as_list[i])
            path_part = unicodedata.normalize('NFC', path_part)
            normalized_path_part = \
                queryUtility(IURLNormalizer).normalize(path_part)
            current_path = '/'.join(path_as_list[:i+1])
            
            # If in the current folder, then just get the folder
            if normalized_path_part not in parent.objectIds():
                # Checks to make sure that the folder is valid.            
                if not parent.checkIdAvailable(id=normalized_path_part):
                    self.bad_folders.append(current_path)
                    return None          
                    
                parent.invokeFactory(type_name=folder_type, id=normalized_path_part)
                foldr = getattr(parent, normalized_path_part)
                foldr.setTitle(path_part)
                if excludefromnav:
                    foldr.setExcludeFromNav(True)
                foldr = factory.doCreate(foldr, normalized_path_part)
                catalog.reindexObject(foldr, catalog.indexes())
                
            else:
                foldr = getattr(parent, normalized_path_part)
                
            parent = foldr
        return parent
           

    def _createObject(self, filepath, fdata, parent):
        """ """ 
        props = getToolByName(parent, 'portal_properties')
        image_type = props.zipfile_properties.image_type
        file_type = props.zipfile_properties.file_type
        doc_type = props.zipfile_properties.doc_type
        folder_type = props.zipfile_properties.folder_type
        
        mt = parent.mimetypes_registry
        
        ext = filepath.split('.')[-1]
        ext = ext.lower()
        ftype = mt.lookupExtension(ext)    
        if ftype:
            mimetype = ftype.normalized()
            newObjType = self._getFileObjectType(ftype.major(), mimetype)        
        else:
            newObjType = self._getFileObjectType(
                                        'application', 
                                        'application/octet-stream'
                                        )
            mimetype = 'application/octet-stream'
        nm = filepath.split('/')
        
        if nm[-1]:
            filename = nm[-1]
        else:
            filename = nm[0]
        
        if filename not in parent.objectIds():
            parent.invokeFactory(type_name=newObjType, id=filename)
            obj = getattr(parent, filename)
            obj.setTitle(splitext(filename)[0])
        else:
            obj = getattr(parent, filename)
        
        if newObjType == image_type:
            obj.setImage(fdata)
        elif newObjType == doc_type:
            obj.setText(fdata)
        elif newObjType == file_type:
            obj.setFile(fdata)

        factory = getToolByName(parent, 'portal_factory')
        catalog = getToolByName(parent, 'portal_catalog')
        obj = factory.doCreate(obj, filename)
        obj.setFormat(mimetype)
        catalog.reindexObject(obj, catalog.indexes())
        return obj
    

    def _getFileObjectType(self, major, mimetype):
        """ """        
        props = getToolByName(getSite(), 'portal_properties')
        image_type = props.zipfile_properties.image_type
        file_type = props.zipfile_properties.file_type
        doc_type = props.zipfile_properties.doc_type
        folder_type = props.zipfile_properties.folder_type

        if 'image' == major:
            type = image_type
        elif mimetype in ['text/html','text/plain','text/structured','text/x-rst']:
            type = doc_type            
        else:
            type = file_type
        return type
    

    def getTime(self,id):
        """ Returns the gmtime appended to the an id, used to obtain a unique 
            id for the logFile object 
        """
        import time
        uid = id
        for tp in time.gmtime():
            uid += str(tp)
        return uid

    # Export content to a zip file.
    # 
    # context   - Container refers to the container of all the objects that 
    #               are to be exported.
    # obj_paths - Refers to a list of paths of either objects or contexts 
    #               that will be included in the zip file.
    # filename - Refers to the fullpath filename of the exported zip file.

    def exportContent(self, context, obj_paths=None, filename=None):
        """ Export content to a zip file.
        """      
        objects_list = self._createObjectList(context, obj_paths)
        zip_path = self._getAllObjectsData(context, objects_list)        
        return zip_path

    def _createObjectList(self, context, obj_paths=None, state=None):
        """ Create a list of objects by iteratively descending a folder 
            tree... or trees (if obj_paths is set).
        """
        objects_list=[]
        
        if obj_paths:
            portal = getToolByName(context, 'portal_url').getPortalObject() 
            for path in obj_paths:
                obj = portal.restrictedTraverse(path)      
                # if this is a folder, then add everything in this folder to 
                # the obj_paths list otherwise simply add the object.
                if obj.isPrincipiaFolderish:
                    self._appendItemsToList(folder=obj, list=objects_list,state=state)
                elif obj not in objects_list:
                    if state:
                        if obj.portal_workflow.getInfoFor(obj,'review_state') in state:
                            objects_list.append(obj)
                    else:
                        objects_list.append(obj)
        else:
            #create a list of the objects that are contained by the context
            self._appendItemsToList(folder=context, list=objects_list,state=state)
            
        return objects_list

    def generateSafeFileName(self, file_name): 
        """ Remove illegal characters from the exported filename.
        """
        file_name = unquote(file_name)
        return file_name

    def _getAllObjectsData(self, context, objects_listing):
        """ Returns the data in all files with a content object to be placed
            in a zipfile
        """
        import tempfile
        # Use temporary IO object instead of writing to filesystem.
        fd, path = tempfile.mkstemp('.zipfiletransport')
        close(fd)
        
        zipFile =  ZipFile(path, 'w', ZIP_DEFLATED)
        context_path = str(context.virtual_url_path())

        for obj in objects_listing:
            object_extension = ''
            object_path = str(obj.virtual_url_path())
            
            if self._objImplementsInterface(obj, interfaces.IATFile) or \
                        self._objImplementsInterface(obj, interfaces.IATImage):
                file_data = str(obj.data)
                object_path = object_path.replace(context_path + '/', '')
                
            elif self._objImplementsInterface(obj, interfaces.IATDocument):

                if "text/html" == obj.Format():
                    file_data = obj.getText()
                    object_extension = ".html"
                        
                elif "text/x-rst" == obj.Format():
                    file_data = obj.getRawText() 
                    object_extension = ".rst"                    

                elif "text/structured" == obj.Format():
                    file_data = obj.getRawText() 
                    object_extension = ".stx"
                        
                elif "text/plain" == obj.Format():
                    file_data = obj.getRawText() 
                    object_extension = ".txt"

                else:
                    file_data = obj.getRawText()

                object_path = object_path.replace(context_path + '/', '')

            elif self._objImplementsInterface(obj,interfaces.IATFolder):
                if hasattr(obj, 'getRawText'):
                    file_data = obj.getRawText()

                    if object_path == context_path:
                        object_path = object_path.split("/")[-1]
                    else:
                        object_path = object_path.replace(context_path + '/', '')
            
                    if object_path[-5:] != ".html" and object_path[-4:] != ".htm":
                        object_extension = ".html"
            else:
                continue

            # start point for object path, adding 1 removes the initial '/'
            object_path = self.generateSafeFileName(object_path)

            if object_path: 
                # reconstruct path with filename, restores non-ascii 
                # characters in filenames
                filename_path = []
                for i in range(0, len(object_path.split('/'))):
                    filename_path.append(obj.Title())
                    obj = obj.aq_inner.aq_parent

                if len(filename_path) > 1:
                    filename_path.reverse()
                    filename_path = '/'.join(filename_path)
                else:
                    filename_path = filename_path[0] 

                # Add the correct file extension
                if filename_path[-len(object_extension):] != object_extension:
                    filename_path += object_extension

                if 'Windows' in context.REQUEST['HTTP_USER_AGENT']:
                    filename_path = filename_path.decode('utf-8').encode('cp437')
                zipFile.writestr(filename_path, file_data)                

        zipFile.close()
        return path
                
        
    def _objImplementsInterface(self, obj, interfaceClass):
        """ Return boolean indicating if obj implements the given interface.
        """
        if shasattr(interfaceClass, 'providedBy') and \
                interfaceClass.providedBy(obj):
            return True

        if not shasattr(obj, '__implements__'):
            return False
    
        if interfaceClass in self._tupleTreeToList(obj.__implements__):
            return True
    

    def _tupleTreeToList(self, t, lsa=None):
        """Convert an instance, or tree of tuples, into list."""
        import types
        if lsa is None: lsa = []
        if isinstance(t, types.TupleType):
            for o in t:
                self._tupleTreeToList(o, lsa)
        else:
            lsa.append(t)
        return lsa


    def _appendItemsToList(self, folder, list, state):
        """ """
        brains = folder.portal_catalog.searchResults(
                    path={'query':('/'.join(folder.getPhysicalPath())+'/'),}
                    )
        
        for brain_object in brains:
            obj = brain_object.getObject()
            
            if not (obj in list or obj.isPrincipiaFolderish):
                if state:
                    if obj.portal_workflow.getInfoFor(obj,'review_state') in state:
                        list.append(obj)
                else:
                    list.append(obj)
                
        return list

    
    def _convertToUnicode(self, bytestring):
        """ Convert bytestring into unicode object
        """
        # *nix encoding
        try:
            unicode_text = unicode(bytestring, 'utf-8')
        # WinZip encoding            
        except UnicodeDecodeError:
            unicode_text = unicode(bytestring, 'cp437')
        return unicode_text

    #
    # Utility functions for use by outside tools.
    #
    #
    def getZipFilenames(self, zfile):
         """ Gets a list of filenames in the Zip archive."""
         try:
             f = ZipFile(zfile)
         except error:
             return []
         if f:
             return f.namelist()
         else:
             return []
        
    def getZipFileInfo(self, zfile):
         """ Gets info about the files in a Zip archive.
         """
         mt = self.mimetypes_registry
         f = ZipFile(zfile)
         fileinfo = []
         for x in f.infolist():
             fileinfo.append((x.filename, 
                              mt.lookupExtension(x.filename).normalized(), 
                              x.file_size))
         return fileinfo
    
    def getZipFile(self, zfile, filename):
         """ Gets a file from the Zip archive.
         """
         mt = self.mimetypes_registry
         f = ZipFile(zfile)
         finfo = f.getinfo(filename)
         fn = split(finfo.filename)[1] # Get the file name
         path = fn.replace('\\', '/')
         fp = path.split('/') # Split the file path into a list
         
         if '' == fn:
             return 'dir', fn, fp, None, None, 0, None
         ftype = mt.lookupExtension(finfo.filename)
         if not ftype:
             major = 'application'
             mimetype = 'application/octet-stream'
         else:
             major =  ftype.major()
             mimetype = ftype.normalized()
         fdata = f.read(filename)
         return 'file', fn, fp, major, mimetype, finfo.file_size, fdata


    def get_zipfile_name(self):
        return 'Test.zip'
        
