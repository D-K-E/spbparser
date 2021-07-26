"""
MIT License

Copyright (c) 2020 D.Kaan Eraslan & Qm Auber

Permission is hereby granted, free of charge, to any person
obtaining a copy
of this software and associated documentation files (the
"Software"), to deal
in the Software without restriction, including without
limitation the rights
to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall
be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE
SOFTWARE.
"""
"""\brief Spectral Binary File Format (.spb) Specification

Table 1: Structure of Spectral Binary File.

File section                  | Bytes
----------------------------- | ----------
File identifier ’SPB’         | 3
Header Part                   | 24
Image width                   | 4
Image height                  | 4
Number of spectral channels n | 4
First wavelength              | 4
Wavelength Resolution         | 4
Last Wavelength               | 4
Image Data                    | x*y*n*4

Image data is written to the file in column order and values
are stored in little endian form.
Dimensions (x,y and n) are stored in uint32-format
and wavelength values in float32-format. Spectral image
values are reflectance values stored as float32.
"""

from typing import List, Tuple, Dict, Union, Optional
import os
import array

HEADER_SIZE = 27


class spb:
    @staticmethod
    def check_file_identifier(headerInfo: List[str]) -> bool:
        ""
        return headerInfo[0] == "S" and headerInfo[1] == "P" and headerInfo[2] == "B"

    @staticmethod
    def get_header(fpath: str) -> Tuple[bool, Optional[str]]:
        ""

        with open(fpath, "rb") as f:
            hinfo = f.read()

        headerInfo = hinfo[: HEADER_SIZE + 1]
        magic_header = hinfo[:3].decode()
        diminfo = hinfo[3 : 3 + 12]
        dimarr = array.array("I", diminfo)
        waveinfo = hinfo[3 + 12 : 3 + 12 + 12]
        wavearr = array.array("f", waveinfo)
        # headerInfo = headerInfo.decode("ascii")
        if spb.check_file_identifier(magic_header) is False:
            return False, None
        return True, (magic_header, tuple(dimarr), tuple(wavearr))

    @staticmethod
    def parseFileHeader(
        headerInfo: Tuple[str, Tuple[int, int, int], Tuple[float, float, float]]
    ) -> Dict[str, Union[float, int]]:
        ""
        width = int(headerInfo[1][0])
        height = int(headerInfo[1][1])
        nb_channels = int(headerInfo[1][2])
        first_wavelength = float(headerInfo[2][0])
        wavelength_resolution = float(headerInfo[2][1])
        last_wavelength = float(headerInfo[2][2])
        return {
            "width": width,
            "height": height,
            "nb_channels": nb_channels,
            "first_wavelength": first_wavelength,
            "last_wavelength": last_wavelength,
            "wavelength_resolution": wavelength_resolution,
        }

    @staticmethod
    def getImageData(fpath: str,) -> List[float]:
        "get image data"
        with open(fpath, "rb") as f:
            fimage = f.read()

        image_data = array.array("f", fimage[HEADER_SIZE:])

        return image_data

    @staticmethod
    def read_header(fpath: str) -> Tuple[bool, Union[Dict[str, Union[int, float]]]]:
        ""
        check, header = spb.get_header(fpath)
        if check is False:
            return check, None
        header = spb.parseFileHeader(header)
        return True, header

    @staticmethod
    def read_file(fpath: str) -> Tuple[bool, Optional[Dict[str, Union[int, float]]]]:
        ""
        check, header = Spb.read_header(fpath)
        if check is False:
            return check, None
        imdata = getImageData(fpath)
        fdata = {}
        fdata.update(header)
        fdata["data"] = imdata
        return fdata
