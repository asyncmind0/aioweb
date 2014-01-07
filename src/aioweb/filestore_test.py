import os
from os.path import join
import unittest
import shutil
from aioweb.filestore import FileStore
from loremipsum import generate_sentence, generate_paragraph
from nose.tools import nottest


@nottest
class FileStoreTest(unittest.TestCase):
    def setUp(self):
        self.testdir = "/tmp/filestoretest/"
        self.filestore = FileStore(self.testdir)
        shutil.rmtree(self.testdir, True)
        os.mkdir(self.testdir)
        self.testfiles = []
        for testfile in range(10):
            testfile = join(self.testdir, "testfile%s.rst" % testfile)
            self.testfiles.append(testfile)
            with open(testfile, 'x') as testfile:
                testfile.write(generate_paragraph()[2])
    
    def tearDown(self):
        shutil.rmtree(self.testdir)
        

    def test_list_posts(self):
        testfiles = self.filestore.list_posts()
        self.assertListEqual(sorted(testfiles), sorted(self.testfiles))
