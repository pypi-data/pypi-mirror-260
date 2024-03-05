from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='astromorphlib',
      version='0.2.23',
      description='Python scripts to analyze the morphology of isolated/interacting galaxies',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='J. A. Hernandez-Jimenez',
      author_email='joseaher@gmail.com',
      url = "https://gitlab.com/joseaher/astromorphlib",
      packages=['stat_lib'],
      package_data = {'stat_lib':['Table_Arp_Madore_pairs_updated.txt',
                                  'iDR4_obs_seeing.csv','iDR4_zero-points.csv',
                                  'properties.dat']},
      include_package_data =  True
      )
