![alt text](logo.png)

# Overview

Python scripts to analyze the morphology of isolated and interacting galaxies.
The package is designed to download S-PLUS (https://splus.cloud/) and
Legacy (https://www.legacysurvey.org) images automatically. There are functions
to calculate a 2D sky background of the images and deblended segmentation maps of
interacting systems with merger isophotes. The non-parametric analysis is
performed by using `statmorph` package (https://github.com/vrodgom/statmorph).  
The user can study the environment of the object/system by downloading a list of
the galaxies within Field-of-View of S-PLUS/Legacy images from SIMBAD server
(http://simbad.u-strasbg.fr/simbad/). In addition, there is a function to
display DSS2 (http://alasky.u-strasbg.fr/hips-image-services/hips2fits) images
of any size.

Website: https://gitlab.com/joseaher/astromorphlib

## Documentation

The documentation is available at https://astromorphlib.readthedocs.io


## Installation

**Requirements**

astromorphlib requires to run the following packages:

    * statmorph
    * splusdata
    * astroplotlib
    * numpy
    * scipy
    * matplotlib
    * astropy
    * astroquery
    * wget


This version can be easily installed via PyPI (https://pypi.org/project/astromorphlib/):

    % pip install astromorphlib

If you prefer to install astromorphlib manually, you can clone the developing
version at https://gitlab.com/joseaher/astromorphlib. In the directory this
README is in, simply type:

    % pip install .

or,

    % python setup.py install

## Uninstallation

To uninstall astromorphlib, just type:

    % pip uninstall astromorphlib


## Authors

- Jose Hernandez-Jimenez (joseaher@gmail.com)
- Angela Krabbe                              


**Acknowledgements**

This software was funded partially by Brazilian agency FAPESP,
process number 2021/08920-8.

## Citing

If you use this code for a scientific publication, please
cite [Hernandez-Jimenez & Krabbe et al. (2022)](https://zenodo.org/records/6940848#.YzS4ENXMJH4).
The BibTeX entry for this package is:

```
@software{hernandez_jimenez_2022_6940848,
  author       = {Hernandez-Jimenez, J. A. and
                  Krabbe, A. C.},
  title        = {{Astromorphlib: Python scripts to analyze the
                   morphology of isolated and interacting galaxies}},
  month        = jul,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {0.2},
}
```
