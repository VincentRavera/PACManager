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
