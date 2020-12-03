# spbparser
Header only Spectral Binary Format utils.

Just include header the required file from `ìnclude` folder.

## Features

- Reader
- Writer

## Usage

To read an spb file:

```
c++

#include <spb/spbreader.hpp>

const char *path = "path/to/my/file.spb";

uint32_t width, height, nb_channels;
float first_wavelength, wavelength_resolution;
float last_wavelength;
float *data

spb::read_file(path, width, height, nb_channels,
               first_wavelength, wavelength_resolution,
               last_wavelength, data);

```


To write an spb file:

```
c++

#include <spb/spbwriter.hpp>

const char *path = "path/to/my/outfile.spb";

MyCustomSpb spectrum();
/**
some operations ...
.
.
.
*/

uint32_t width = spectrum.image_width();
uint32_t height = spectrum.image_height();
uint32_t nb_spectral_channels =  spectrum.nb_channels();
float first_wavelength = spectrum.first_wavelength();
float wavelength_resolution = spectrum.wavelength_resolution();
float last_wavelength = spectrum.last_wavelength();
float *data;
spectrum.put_data(data);

spb::write_file(path, width, height, nb_channels,
                first_wavelength, wavelength_resolution,
                last_wavelength, data);

```
