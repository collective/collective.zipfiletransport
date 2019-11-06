# -*- coding: utf-8 -*-
import os
from zipfile import ZipFile

from zope import component
from collective.zipfiletransport.tests.base import TestCase
from collective.zipfiletransport.browser.interfaces import IExport
from collective.zipfiletransport.utilities.interfaces import \
    IZipFileTransportUtility


class TestZipfiletransportUtility(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.zft_util = component.getUtility(
                            IZipFileTransportUtility,
                            name="zipfiletransport")

    def test_import(self):

        file = os.path.join(os.path.dirname(__file__), 'test_folder.zip')

        # Test Zip file import
        self.zft_util.importContent(
                                file=file,
                                context=self.folder,
                                description='test_folder zip file description',
                                contributors='test_user',
                                overwrite=False,
                                categories=['testing', 'zipfileimport'],
                                excludefromnav=False,
                                )

        folder = self.folder
        self.assertEquals(folder.objectIds(), ['test_folder'])

        # XXX: No properties are being set on the imported folder, is
        # the desirable?
        zip_folder = self.folder.test_folder
        self.assertEquals(zip_folder.getExcludeFromNav(), False)
        self.assertEquals(zip_folder.Subject(), ())

        # Test the properties were correctly set on the sub-items
        zip_folder_contents = \
            ['test_image.jpeg', 'test_image.png', 'test_document.doc',
                'test_document.pdf', 'test_document.odt', ]
        self.assertEquals(zip_folder.objectIds(), zip_folder_contents)

        # Test that the categories were applied
        for oid  in zip_folder_contents:
            self.assertEquals(zip_folder[oid].Subject(),
                              ('testing', 'zipfileimport'))

        # Import again with new properties but with overwrite=False
        self.zft_util.importContent(
                                file=file,
                                context=self.folder,
                                description='test_folder zip file description',
                                contributors='test_user1',
                                overwrite=False,
                                categories=['testing', 'zipfileimport',
                                            'new category'],
                                excludefromnav=True,
                                )

        # Test that no properties were changed, since we specified:
        # overwrite=False
        # XXX: No properties are being set on the imported folder, is
        # the desirable?
        self.assertEquals(zip_folder.getExcludeFromNav(), False)
        self.assertEquals(zip_folder.Subject(), ())

        for oid  in zip_folder_contents:
            self.assertEquals(zip_folder[oid].Subject(),
                              ('testing', 'zipfileimport'))
            self.assertEquals(zip_folder[oid].getExcludeFromNav(), False)

        # Import again with new properties but with overwrite=True
        self.zft_util.importContent(
                                file=file,
                                context=self.folder,
                                description='test_folder zip file description',
                                contributors='test_user2',
                                overwrite=True,
                                categories=['testing', 'zipfileimport',
                                            'new category'],
                                excludefromnav=True,
                                )

        # Test that no properties were changed, since we specified:
        # overwrite=False
        for oid  in zip_folder_contents:
            self.assertEquals(zip_folder[oid].Subject(),
                              ('testing', 'zipfileimport', 'new category'))
            self.assertEquals(zip_folder[oid].getExcludeFromNav(), True)

    def test_export(self):
        self.folder.invokeFactory(
            'File',
            'test-file.zip',
            file=open(os.path.join(os.path.dirname(__file__), 'test_folder.zip')),
        )

        obj_paths = ['/'.join(self.folder.getPhysicalPath())]

        brains = IExport(self.folder).get_brains()

        zip_path = self.zft_util.exportContent(self.folder, brains, obj_paths)
        with open(zip_path, 'rb') as fp:
            with ZipFile(fp, mode='r') as zip_file:
                self.assertIn('test-file.zip', zip_file.namelist())
                self.assertEqual(zip_file.infolist()[0].file_size, 78331)
