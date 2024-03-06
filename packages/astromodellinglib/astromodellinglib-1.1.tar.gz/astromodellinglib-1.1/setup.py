from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='astromodellinglib',
      version='1.1',
      description='Python scripts to modelling kinematics, dynamics and morphology of galaxies.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='J. A. Hernandez-Jimenez',
      author_email='joseaher@gmail.com',
      url = "https://gitlab.com/joseaher/astromodellinglib",
      packages=['astromodellinglib']
      )
