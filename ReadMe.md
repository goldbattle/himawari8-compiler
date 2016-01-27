# himawari8-compiler

 This repo gets images from the [Himawari 8](https://en.wikipedia.org/wiki/Himawari_8) satellite. This was inspired by the great work by https://glittering.blue/ author. The fetch script is a variation of his [original](https://gist.github.com/celoyd/39c53f824daef7d363db) script. See how to run the script below, which will download all the images for a day, and compile each tile into a large single png. Note day is for January of 2016 and that the valid zoom levels seem to be powers of 2, 1..16, and 20.


# Install

* Runs with python 3.5.1
* python -m pip install --upgrade pip
* pip install requests
* pip install python-dateutil
* pip install image

# Running

```console
python hi8_compile.py 25 8
python hi8_compile.py <day of 2016> <scale>
```