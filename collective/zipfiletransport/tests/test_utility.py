from zope import component
from collective.zipfiletransport.tests.base import TestCase
from collective.zipfiletransport.utilities.interfaces import IZipFileTransportUtility

class TestChat(TestCase):
    """ Tests the babble/client/browser/chat.py module
    """

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def test_import(self):
        self.zft_util = component.getUtility(
                            IZipFileTransportUtility, 
                            name="zipfiletransport")

        file = '/'.join(['..',
                        '..',
                        'src',
                        'collective.zipfiletransport',
                        'collective',
                        'zipfiletransport',
                        'tests',
                        'test_folder.zip',])
        try:
            testfile = open(file)
        except:
            file = '/'.join([
                            'collective',
                            'zipfiletransport',
                            'tests',
                            'test_folder.zip',])

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

        # XXX: No properties are being set on the imported folder, is the desirable?
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
            self.assertEquals(zip_folder[oid].Subject(), ('testing', 'zipfileimport'))


        # Import again with new properties but with overwrite=False
        self.zft_util.importContent(
                                file=file, 
                                context=self.folder, 
                                description='test_folder zip file description', 
                                contributors='test_user1', 
                                overwrite=False, 
                                categories=['testing', 'zipfileimport', 'new category'], 
                                excludefromnav=True,
                                )

        # Test that no properties were changed, since we specified:
        # overwrite=False
        # XXX: No properties are being set on the imported folder, is the desirable?
        self.assertEquals(zip_folder.getExcludeFromNav(), False)
        self.assertEquals(zip_folder.Subject(), ())

        for oid  in zip_folder_contents:
            self.assertEquals(zip_folder[oid].Subject(), ('testing', 'zipfileimport'))
            self.assertEquals(zip_folder[oid].getExcludeFromNav(), False)

        # Import again with new properties but with overwrite=True
        self.zft_util.importContent(
                                file=file, 
                                context=self.folder, 
                                description='test_folder zip file description', 
                                contributors='test_user2', 
                                overwrite=True, 
                                categories=['testing', 'zipfileimport', 'new category'], 
                                excludefromnav=True,
                                )

        # Test that no properties were changed, since we specified:
        # overwrite=False
        for oid  in zip_folder_contents:
            self.assertEquals(zip_folder[oid].Subject(), ('testing', 'zipfileimport', 'new category'))
            self.assertEquals(zip_folder[oid].getExcludeFromNav(), True)
        

    def test_export(self):
        self.zft_util = component.getUtility(
                            IZipFileTransportUtility, 
                            name="zipfiletransport")

        obj_paths = ['/'.join(self.folder.getPhysicalPath())]
        zip_path = self.zft_util.exportContent(self.folder, obj_paths)
        fp = open(zip_path, 'rb')

        # XXX: Add additional tests...
        # Only works in Plone4
        # self.assertEquals(fp.errors, None) 
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestChat))
    return suite

