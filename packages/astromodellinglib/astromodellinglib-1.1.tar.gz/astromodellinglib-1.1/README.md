# astromodellinglib

A Python collection of routines designed to model the kinematics, dynamics, and morphology of galaxies is available. The package includes functions in both 1D and 2D for modeling surface brightness profiles, incorporating well-known profiles such as SERSIC, FREEMAN, and FERRER (to model bars) functions. Additionally, the collection features functions for modeling velocity curves in 1D and observed velocity fields in 2D. These include implementations for various dark halo potentials (e.g., NFW, isothermal sphere, etc.) and phenomenological models such as Bertola and Plummer, among others. Some examples of  early applications of this package
are exemplified in  [Hernandez-Jimenez 13](https://ui.adsabs.harvard.edu/abs/2013MNRAS.435.3342H/abstract), [15](https://ui.adsabs.harvard.edu/abs/2015MNRAS.451.2278H/abstract).

(c) J. A. Hernandez-Jimenez

E-mail: joseaher@gmail.com

Website: https://gitlab.com/joseaher/astromodellinglib

## Installation

astroplotlib requires:

    * numpy
    * scipy

This version can be easily installed within Anaconda Enviroment via PyPI:

    % pip install astromodellinglib

If you prefer to install astroplotlib manually, you can clone the developing
version at https://gitlab.com/joseaher/astromodellinglib. In the directory this
README is in, simply:

    % pip install .

or,

    % python setup.py install

## Uninstallation

To uninstall  astromodellinglib, simply

    % pip uninstall  astromodellinglib
