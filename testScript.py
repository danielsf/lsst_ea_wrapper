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
            familyTree = self.dbo.getDaughters('g-band Response Envelope')
        self.assertEqual(context.exception.args[0],
                         'More than one object match the name you gave. '
                         'Try specifying an author or a version')
        


if __name__ == "__main__":
    unittest.main()
