#!/usr/bin/env python3
import unittest
import pacman
import json


def pacmain_overall(inputfile, expected):
    with open(inputfile) as f:
        inputdata = json.load(f)
    with open(expected) as f:
        expectedata = json.load(f)
    outputdata = pacman.pacmain(inputdata)
    return expectedata, outputdata


def pac_no_cyclic_overall(inputfile):
    with open(inputfile) as f:
        inputdata = json.load(f)
    return pacman.pac_no_cyclic(inputdata)


class TestPacmain(unittest.TestCase):
    """TestPacmain test suite."""

    def test_pacmain_01(self):
        i, e = pacmain_overall(
            "./resources/01.json",
            "./resources/01-ans.json")
        self.assertDictEqual(i, e)

    def test_pacmain_02(self):
        i, e = pacmain_overall(
            "./resources/02.json",
            "./resources/02-ans.json")
        self.assertDictEqual(i, e)

    def test_pacmain_03(self):
        i, e = pacmain_overall(
            "./resources/03.json",
            "./resources/03-ans.json")
        self.assertDictEqual(i, e)

    # Waiting for A to finish
    def test_pacmain_04(self):
        i, e = pacmain_overall(
            "./resources/04.json",
            "./resources/04.json")
        self.assertDictEqual(i, e)

    # User did not process A yet
    def test_pacmain_05(self):
        i, e = pacmain_overall(
            "./resources/05.json",
            "./resources/05.json")
        self.assertDictEqual(i, e)


class TestPacCyclic(unittest.TestCase):
    """TestPacmain test suite."""

    # Proceed to done
    def test_proceed_to_done(self):
        inp = {
            "DONE": {"A": {}},
            "DOING": {"B": {}},
            "TODO": {"C": {}},
            "PENDING": {"D": {}}
        }
        exp = {
            "DONE": {"A": {}, "B": {}, "C": {}},
            "DOING": {},
            "TODO": {},
            "PENDING": {"D": {}}
        }
        out = pacman.proceed_to_done(inp)
        self.assertDictEqual(out, exp)

    # Cyclic dependencies
    def test_pac_no_cyclic_06(self):
        err = None
        try:
            self.assertFalse(pac_no_cyclic_overall("./resources/06.json"))
        except pacman.PACyclicDependenciesException as e:
            err = e
        self.assertIsNotNone(err)
