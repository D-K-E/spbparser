/**
  Spectral Binary File IO
 */

#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
//
namespace spbparser {
/**
Spectral Binary File Format (.spb) Specification

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

*/

#define HEADER_SIZE 27

/**
  Check if file header is "SPB"
 */
bool check_file_identifier(char headerInfo[HEADER_SIZE]) {
  return headerInfo[0] == 'S' && headerInfo[1] == 'P' &&
         headerInfo[2] == 'B';
}

void get_header(std::ifstream &file,
                char headerInfo[HEADER_SIZE]) {
  //
  // set file to back
  if (file.is_open()) {
    file.seekg(0);
    file.read(headerInfo, HEADER_SIZE);
  } else {
    throw std::runtime_error("spb file is not opened");
  }
  if (!check_file_identifier(headerInfo)) {
    std::stringstream ss;
    ss << "File identifier for spb file is not correct."
       << std::endl
       << "It should be 'SPB'"
       << "see given header: " << headerInfo << std::endl;
    std::string err = ss.str();
    throw std::runtime_error(err);
  }
}
void get_sub(unsigned int &start, char arr[4],
             char headerInfo[HEADER_SIZE]) {
  for (unsigned int k = 0; k < 4; k++) {
    arr[k] = headerInfo[start];
    start++;
  }
}
void get_sub_ui(unsigned int &start, uint32_t val,
                char headerInfo[HEADER_SIZE]) {
  char arr[4];
  get_sub(start, arr, headerInfo);
  std::string s(arr);
  val = std::stoul(s);
}
void get_sub_f(unsigned int &start, float val,
               char headerInfo[HEADER_SIZE]) {
  char arr[4];
  get_sub(start, arr, headerInfo);
  std::string s(arr);
  val = std::stof(s);
}
void parseFileHeader(char headerInfo[HEADER_SIZE],
                     uint32_t &width, uint32_t &height,
                     uint32_t &nb_channels,
                     float &first_wavelength,
                     float &wavelength_resolution,
                     float &last_wavelength) {
  unsigned int start = 3;
  get_sub_ui(start, width, headerInfo);
  get_sub_ui(start, height, headerInfo);
  get_sub_ui(start, nb_channels, headerInfo);
  get_sub_f(start, first_wavelength, headerInfo);
  get_sub_f(start, wavelength_resolution, headerInfo);
  get_sub_f(start, last_wavelength, headerInfo);
}
void getImageData(std::ifstream &file, float *&data,
                  const uint32_t &width,
                  const uint32_t &height,
                  const uint32_t &nb_channels) {
  file.seekg(0);
  char headerInfo[HEADER_SIZE];
  get_header(file, headerInfo);
  file.seekg(HEADER_SIZE);
  uint32_t total_size = width * height * nb_channels;
  uint32_t stride = 4;
  data = new float[total_size];
  uint32_t gpos = HEADER_SIZE;
  for (uint32_t pos = 0; pos < total_size; pos++) {
    char arr[stride];
    file.seekg(gpos);
    file.read(arr, stride);
    std::string s(arr);
    data[pos] = std::stof(s);
    gpos += stride;
  }
}

void read_file(const char *fpath, uint32_t &width,
               uint32_t &height, uint32_t &nb_channels,
               float &first_wavelength,
               float &wavelength_resolution,
               float &last_wavelength, float *&data) {
  std::ifstream file;
  file.open(fpath, std::ifstream::in);
  char headerInfo[HEADER_SIZE];
  get_header(file, headerInfo);
  parseFileHeader(headerInfo, width, height, nb_channels,
                  first_wavelength, wavelength_resolution,
                  last_wavelength);
  getImageData(file, data, width, height, nb_channels);
  file.close();
}
}
