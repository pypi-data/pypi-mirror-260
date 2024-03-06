import unittest

from fallbacks import Var


class VarTest(unittest.TestCase):
    def test_default(self):
        v = Var("app", "var")
        self.assertTrue(v.check("pypi.org"))
        # The types say this is just a bool; might make sense to expand this in
        # the future though...
        self.assertTrue(v.check("pypi.org", default=True))
        self.assertFalse(v.check("pypi.org", default=False))

    def test_record(self):
        v = Var("app", "var")
        self.assertTrue(v.check("pypi.org"))
        v.record("pypi.org", False)
        self.assertFalse(v.check("pypi.org"))
        # defaults don't matter
        self.assertFalse(v.check("pypi.org", default=True))
        self.assertFalse(v.check("pypi.org", default=False))
