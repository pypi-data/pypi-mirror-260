# makeitseg2

`makeitseg2` is a Python module that converts SEGY or SU (Seismic Un*x) files to SEG2 (or DAT) files. It also supports converting stream data to SEG2 format.

### Getting Started

A working example is provided in the "test.ipynb" file.

### Prerequisites

Before installing `makeitseg2`, ensure that `obspy` is installed. You can install it via pip using the following command:

``` bash
pip install obspy
```

## Installation

Since the pip installation for the latest version of makeitseg2 is not yet available, you can download the repository and install it using the setup file.

``` bash
git clone https://github.com/yourusername/makeitseg2.git
cd makeitseg2
python setup.py install
```
## How it works

To use makeitseg2, you can import it and call the from_file function to convert SEGY or SU files to SEG2 format. Optionally, you can call the from_data function to convert stream data to SEG2 format.

``` python
import makeitseg2

# Convert SEGY or SU file to SEG2
makeitseg2.from_file(SEGY_or_SU_filename, newConverted_SEG2_file_name)

# Convert stream data to SEG2
makeitseg2.from_data(src_rcvr_location, sampling_interval, trace_Array, newConverted_SEG2_file_name)
```
If `newConverted_SEG2_file_name` is not provided, the new SEG2 file will have the same name as the original and will be placed in the `Converted_SEG2` folder.