from unittest import TestCase
import os
from shutil import rmtree
from tempfile import gettempdir

import recipe
import recipe.temppath

__author__ = 'elon'

TESTDIR = os.path.join(gettempdir(), 'recipe')


class Testtemppath_module(TestCase):
    def setUp(self):
        try:
            rmtree(TESTDIR)
        except OSError:
            pass
        assert (not os.path.exists(TESTDIR))

    def implements_string(self, obj):
        self.assertEqual(obj + 'foo', str(obj) + 'foo')

    def test_randompath(self):
        os.mkdir(TESTDIR)
        p = recipe.temppath._randompath(TESTDIR)
        self.assertTrue(os.path.samefile(os.path.dirname(p), TESTDIR))
        self.assertFalse(os.path.exists(p))
        os.rmdir(TESTDIR)


class Testtemppath(Testtemppath_module):
    def test_temppath(self):
        os.mkdir(TESTDIR)
        t = recipe.temppath.temppath(TESTDIR)

        self.implements_string(t)

        del t
        os.rmdir(TESTDIR)


class Testtempdirpath(Testtemppath_module):
    def test_tempdirpath(self):
        d = recipe.temppath.tempdirpath(TESTDIR)

        self.implements_string(d)

        self.assertTrue(os.path.isdir(TESTDIR))

        e = recipe.temppath.tempdirpath(TESTDIR)

        del d, e
        self.assertFalse(os.path.exists(TESTDIR))

    def test_tempfilepath(self):
        d = recipe.temppath.tempdirpath(TESTDIR)
        p = d.tempfilepath()
        self.assertTrue(os.path.samefile(os.path.dirname(p), TESTDIR))
        self.assertFalse(os.path.exists(p))


class Testtempfilepath(Testtemppath_module):
    def test_tempfilepath(self):
        p = recipe.temppath.tempfilepath()

        self.implements_string(p)

        self.assertFalse(os.path.exists(p))

        f = open(p, 'w')
        f.write('foobar\nbaz')
        f.close()
        f = open(p, 'r')
        self.assertEqual(f.read(), 'foobar\nbaz')
        f.close()
