from collective.zipfiletransport.tests.base import TestCase

class TestChat(TestCase):
    """ Tests the babble/client/browser/chat.py module
    """

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def test_initial(self):
        self.assertEquals(True, True)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestChat))
    return suite
