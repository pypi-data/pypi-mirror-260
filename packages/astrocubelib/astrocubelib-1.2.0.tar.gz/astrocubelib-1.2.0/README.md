## Astrocubelib: python astronomy package to handle data cubes

This software package offers a comprehensive suite of tools designed to accurately fit emission and absorption lines within a spectrum. By integrating the area under the line profiles within a specified spectral range around the Gaussian peak, it calculates precise line fluxes. Additionally, the program generates continuum maps by integrating spectral windows near the lines or by fitting polynomial (or Chebyshev) functions.

Key features of the program include:

    -Extraction of Gaussian parameters such as centroid, sigma, and height.
    -Computation of Gaussian-Hermite parameters like h3 and h4.
    -Determination of equivalent widths and their corresponding errors.
    -Capability to fit multiple lines simultaneously.
    -Flexibility to fit multiple Gaussians for a single line, a feature particularly useful for modeling AGN broad lines.
    -Automation for processing data cubes, with options to mask specific areas within the cubes and customize fitting --procedures for each masked region.

Overall, this package provides advanced functionalities for analyzing spectral data, enabling users to accurately model and extract valuable information from their data sets.


## INSTALLATION

This version can be easily installed via PyPI (https://pypi.org/project/astrocubelib/):

    % pip install astrocubelib

If you prefer to install astrocubelib manually, you can clone the developing
version at https://gitlab.com/joseaher/astrocubelib. In the directory this
README is in, simply type:

    % pip install .

or,

    % python setup.py install

## Uninstallation

To uninstall astrocubelib, just type:

    % pip uninstall astrocubelib


## Author

- Jose Hernandez-Jimenez (joseaher@gmail.com)
