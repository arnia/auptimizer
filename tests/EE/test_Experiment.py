import unittest
import os
from shutil import copyfile, rmtree

from aup import Experiment, BasicConfig


class ExperimentTestCase(unittest.TestCase):
    path = os.path.join("tests", "data", "exp5.json")
    auppath = os.path.join("tests", "data", ".aup")
    ori_db = os.path.join(auppath, "sqlite3.db")
    bk_db = os.path.join(auppath, "bk.db")

    def setUp(self):
        copyfile(self.ori_db, self.bk_db)

    def tearDown(self):
        copyfile(self.bk_db, self.ori_db)
        # clean test files
        os.remove(self.bk_db)
        if os.path.isfile(os.path.join(os.getcwd(), "exp2.pkl")):
            os.remove(os.path.join(os.getcwd(), "exp2.pkl"))
        rmtree(os.path.join("tests", "jobs"))

    def test_run_through(self):
        exp = Experiment(BasicConfig().load(self.path),
                         username="test", auppath=self.auppath)

        exp.start()
        exp.finish()
        self.assertDictEqual(exp.pending_jobs, {})


if __name__ == '__main__':
    unittest.main()
