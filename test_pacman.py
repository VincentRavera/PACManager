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
