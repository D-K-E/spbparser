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

NB_HEADER_BYTE = 4


class spb:
    ""

    @staticmethod
    def to_array(
        width: int,
        height: int,
        nb_channels: int,
        first_wavelength: int,
        wavelength_resolution: int,
        last_wavelength: int,
        data: List[float],
    ):
        ""
        arr = array.array("B")
        arr.append("S")
        arr.append("P")
        arr.append("B")

        #
        width_c = ctypes.c_uint32(width)
        arr.append(width_c)

        #
        height_c = ctypes.c_uint32(height)
        arr.append(height_c)

        #
        n_c = ctypes.c_uint32(nb_channels)
        arr.append(n_c)

        #
        first_w = ctypes.c_float(first_wavelength)
        arr.append(first_w)

        #
        wave_res = ctypes.c_float(wavelength_resolution)
        arr.append(wave_res)

        #
        last_w = ctypes.c_float(last_wavelength)
        arr.append(last_w)
        for d in data:
            arr.append(d)
        return arr

    @staticmethod
    def save(
        fpath: str,
        width: int,
        height: int,
        nb_channels: int,
        first_wavelength: int,
        wavelength_resolution: int,
        last_wavelength: int,
        data: List[float],
    ):
        ""
        arr = Spb.to_array(
            width=width,
            height=height,
            nb_channels=nb_channels,
            first_wavelength=first_wavelength,
            last_wavelength=last_wavelength,
            data=data,
            wavelength_resolution=wavelength_resolution,
        )
        with open(fpath, "wb") as f:
            for a in arr:
                f.write(a)
