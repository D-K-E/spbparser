"""
python tests of the spb library
"""

import unittest
import csv
import array
from include.python.sbpreader import spb as sbreader
from include.python.sbpwriter import spb as sbwriter


class SpbTest(unittest.TestCase):
    ""

    @classmethod
    def setUpClass(cls):
        ""
        rows = []
        with open("imagespec.csv", "r", encoding="utf-8", newline="\n") as f:
            imspec = csv.reader(f, delimiter=",")
            for row in imspec:
                rs = []
                for cell in row:
                    rs.append(float(cell))
                #
                rows.append(rs)
            #

        cls.spb_csv = rows
        cls.sbp_path = "./imagespec.spb"

    def test_get_header(self):
        "test getting header"
        docs = sbreader.get_header(self.sbp_path)
        magic, dims, winfo = docs[1]
        self.assertEqual(magic, "SPB")
        self.assertEqual(dims, (100, 56, 30))
        self.assertEqual(winfo, (380.0, 11.72412109375, 720.0))

    def test_parseFileHeader(self):
        "test getting header"
        hexample = ("SPB", (100, 56, 30), (380.0, 11.72412109375, 720.0))
        docs = sbreader.parseFileHeader(hexample)
        self.assertEqual(
            docs,
            {
                "width": 100,
                "height": 56,
                "nb_channels": 30,
                "first_wavelength": 380.0,
                "last_wavelength": 720.0,
                "wavelength_resolution": 11.72412109375,
            },
        )

    def test_read_header(self):
        ""
        docs = sbreader.read_header(self.sbp_path)
        self.assertEqual(
            docs,
            (
                True,
                {
                    "width": 100,
                    "height": 56,
                    "nb_channels": 30,
                    "first_wavelength": 380.0,
                    "last_wavelength": 720.0,
                    "wavelength_resolution": 11.72412109375,
                },
            ),
        )

    def test_getImageData(self):
        ""
        docs = sbreader.getImageData(self.sbp_path)
        cs = []
        for row in self.spb_csv[1:]: # skip the first row
            for r in row:
                cs.append(r)
        arr = array.array('f', cs)
        self.assertEqual(arr, docs)


if __name__ == "__main__":
    unittest.main()
