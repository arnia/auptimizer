import unittest
from aup.setupdb import sqlite

from six.moves.configparser import ConfigParser


class SQLITETestCase(unittest.TestCase):
    config = ConfigParser()

    def test_createDB(self):
        self.assertRaises(Exception, sqlite.create_database, self.config, ['test'], 4, 'test')


if __name__ == '__main__':
    unittest.main()
