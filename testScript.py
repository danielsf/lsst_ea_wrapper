from __future__ import with_statement
import unittest
from EADBWrapper import EADBWrapper

class InheritanceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dbo = EADBWrapper()

    def test_many_options(self):
        """
        Make sure that an exception is raised if more than one object
        match the name you give
        """

        with self.assertRaises(RuntimeError) as context:
            familyTree = self.dbo.getFamilyIDs('g-band Response Envelope')
        self.assertEqual(context.exception.args[0],
                         'More than one object match the name you gave. '
                         'Try specifying an author or a version')


    def test_no_options(self):
        """
        Make sure that an exception is raise if no objects are returned.
        """

        with self.assertRaises(RuntimeError) as context:
            familyTree = self.dbo.getFamilyIDs('blah blah blah')
        self.assertEqual(context.exception.args[0],
                         'No objects matched the name you gave.')


    def test_g_band_daughters(self):
        """
        Make sure that we get the full inheritance tree of
        g-band Response Envelope

        This verifies that things I 'know' are correct get returned
        as daughters (i.e. things that are in Chuck's example diagram)

        It does not verify the length of 'daughters' (if something
        that is not in Chuck's diagram is in the inheritance tree,
        that still shows up)
        """

        daughters = self.dbo.getFamilyIDs('g-band Response Envelope',
                                          author='Chuck Claver')

        self.assertTrue(385412 in daughters)
        self.assertTrue(385333 in daughters)
        self.assertTrue(385376 in daughters)
        self.assertTrue(385394 in daughters)
        self.assertTrue(385385 in daughters)
        self.assertTrue(385362 in daughters)
        self.assertTrue(385340 in daughters)


if __name__ == "__main__":
    unittest.main()
