.. statmorphlib documentation master file, created by
   sphinx-quickstart on Mon Nov  6 12:41:08 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to astromorphlib's documentation!
========================================

.. raw:: html

 <object data="_static/logo.png" type="image/svg+xml" width="500"></object>

Overview
========

Astromorphlib (https://gitlab.com/joseaher/astromorphlib) is a powerful and
versatile collection of Python functions designed to analyze the morphology of
both isolated and interacting galaxies in various environments,
including fields, groups, and clusters. The package offers a wide range of
functionalities that enable users to conduct comprehensive analyses of
astronomical images. One of the key features of Astromorphlib is its seamless
integration with S-PLUS (https://splus.cloud/) and Legacy
(https://www.legacysurvey.org) image databases, allowing users to effortlessly
download relevant images for their analyses. By automating this process,
researchers can focus on their analysis without the burden of manual data
retrieval. The library provides essential image processing capabilities, such
as calculating 2D sky background models and generating segmentation maps with
optional source deblending.

Astromorphlib also facilitates the determination of non-parametric parameters
like CAS (Concentration, Asymmetry, and Smoothness) or
MID (M20, Intensity, and Deviation) statistics. These parameters are valuable
for characterizing galaxy morphologies and understanding their evolutionary
processes. The non-parametric analysis is performed by using  statmorph package
(https://github.com/vrodgom/statmorph).

Furthermore, Astromorphlib enables researchers to study the environment of their
target object/system by fetching a list of galaxies within the field-of-view of
S-PLUS/Legacy images from the SIMBAD server (http://simbad.u-strasbg.fr/simbad/).
This feature enhances the context and understanding of the analyzed objects by
considering their neighbouring galaxies.

In summary, Astromorphlib is a
comprehensive and user-friendly Python package that allows the user to conduct
detailed morphological analyses of galaxies in diverse environments.

Installation
============
.. toctree::
   :maxdepth: 2

   installation

Examples
=========

.. toctree::
   :maxdepth: 2

   examples

Parameters
=========

.. toctree::
   :maxdepth: 2

   parameters

Authors
=======

- Jose Hernandez-Jimenez (joseaher@gmail.com)
- Angela Krabbe

**Acknowledgments**

This software was funded partially by Brazilian agency FAPESP,
process number 2021/08920-8.

Citing
======

If you use this code for a scientific publication, please cite `Hernandez-Jimenez & Krabbe et al. (2020) <https://zenodo.org/records/6940848#.YzS4ENXMJH4>`_
The BibTeX entry for this package is::

    @software{hernandez_jimenez_2022_6940848,
    author       = {{Hernandez-Jimenez}, J. A. and {Krabbe}, A. C.},
    title        = {{Astromorphlib: Python scripts to analyze the
    morphology of isolated and interacting galaxies}},
    month        = jul,
    year         = 2022,
    publisher    = {Zenodo},
    version      = {0.2},
    }

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
