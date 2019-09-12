from unittest import TestCase

from aup.Proposer import SequenceProposer as sp
from aup.Proposer import get_proposer


class SequenceTestCase(TestCase):
    def setUp(self):
        self.pc = {
            "proposer": "sequence",
            "parameter_config": []
        }

    def test_int(self):
        self.pc["parameter_config"] = [
            {"name": "x1", "type": "int", "range": [0, 10]},
            {"name": "x2", "type": "int", "range": [0, 10]}
        ]
        rp = get_proposer("sequence")(self.pc)
        self.assertEqual(rp.nSamples, 121)
        param1 = rp.get()
        self.assertTrue(param1 == {"x1": 0, "x2": 0})
        param1 = rp.get()
        self.assertTrue(param1 == {"x1": 1, "x2": 0})
        while not rp.finished:
            param1 = rp.get()
        self.assertTrue(param1 == {"x1": 10, "x2": 10})

    def test_int_interval(self):
        self.pc["parameter_config"] = [
            {"name": "x1", "type": "int", "range": [0, 10], "interval":2},  # 0 2 4 6 8 10
            {"name": "x2", "type": "int", "range": [0, 10], "n":3}          # 0 5 10
        ]
        rp = get_proposer("sequence")(self.pc)
        self.assertEqual(rp.nSamples, 18)
        param1 = rp.get()
        self.assertTrue(param1 == {"x1": 0, "x2": 0})
        param1 = rp.get()
        self.assertTrue(param1 == {"x1": 2, "x2": 0})
        for i in range(10):
            param1 = rp.get()
        self.assertTrue(param1 == {"x1": 10, "x2": 5})
        while not rp.finished:
            param1 = rp.get()
        self.assertTrue(param1 == {"x1": 10, "x2": 10})

    def test_float(self):
        self.pc["parameter_config"] = [
            {"name": "x1", "type": "float", "range": [0, 1], "interval":0.2},
            {"name": "x2", "type": "float", "range": [0, 1]}
        ]
        rp = get_proposer("sequence")(self.pc)
        self.assertEqual(rp.nSamples, 12)
        param1 = rp.get()
        self.assertDictEqual(param1, {"x1": 0, "x2": 0})
        param1 = rp.get()
        self.assertDictEqual(param1, {"x1": 0.2, "x2": 0})
        for i in range(4):
            param1 = rp.get()
        self.assertDictEqual(param1, {"x1": 1, "x2": 0})
        while not rp.finished:
            param1 = rp.get()
        self.assertTrue(param1 == {"x1": 1, "x2": 1})

        self.pc["parameter_config"] = [
            {"name": "x1", "type": "float", "range": [0, 1], "interval": 0.2},
            {"name": "x2", "type": "float", "range": [0, 1], "n": 2}
        ]
        rp = get_proposer("sequence")(self.pc)
        self.assertEqual(rp.nSamples, 12)
        param1 = rp.get()
        self.assertDictEqual(param1, {"x1": 0, "x2": 0})
        param1 = rp.get()
        self.assertDictEqual(param1, {"x1": 0.2, "x2": 0})
        for i in range(4):
            param1 = rp.get()
        self.assertDictEqual(param1, {"x1": 1, "x2": 0})
        while not rp.finished:
            param1 = rp.get()
        self.assertTrue(param1 == {"x1": 1, "x2": 1})

    def test_choice(self):
        self.pc["parameter_config"] = [
            {"name": "x1", "type": "choice", "range": [2, 4, 6, 8, 10]},
            {"name": "x2", "type": "choice", "range": ["a", "b", "c"]}
        ]
        rp = get_proposer("sequence")(self.pc)
        self.assertEqual(rp.nSamples, 15)
        param1 = rp.get()
        self.assertTrue(param1 == {"x1": 2, "x2": "a"})
        while not rp.finished:
            param1 = rp.get()
        self.assertTrue(param1 == {"x1": 10, "x2": "c"})

    def test_gen(self):
        self.assertRaises(KeyError, sp._AbstractGen.get_gen, {'type': 'wrong'})
