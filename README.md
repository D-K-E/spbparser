# spbparser
Header only Spectral Binary Format utils.

Just include header the required file from `ìnclude` folder.

## WARNING

The parser is still in alpha stage. DO NOT use in production.

## Dependency

## Features

- Reader
- Writer

## SPectral Binary Specification Summary

File section                  | Bytes
----------------------------- | ----------
File identifier ’SPB’         | 3
Header Part                   | 
Image width x                 | 4
Image height y                | 4
Number of spectral channels n | 4
First wavelength              | 4
Wavelength Resolution         | 4
Last Wavelength               | 4
Image Data                    | x\*y\*n\*4



Image data is written to the file in column order and values
are stored in little endian form.
Dimensions (x,y and n) are stored in uint32-format
and wavelength values in float32-format. Spectral image
values are reflectance values stored as float32.


## Usage

To read an spb file:

```
c++

#include <spb/spbreader.hpp>

const char *path = "path/to/my/file.spb";

uint32_t width, height, nb_channels;
float first_wavelength, wavelength_resolution;
float last_wavelength;

spb::read_header(path, width, height, nb_channels,
                 first_wavelength, wavelength_resolution,
                 last_wavelength);
float *data = new float[width * height * nb_channels];
spb::read_file(path, width, height, nb_channels, data);

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
