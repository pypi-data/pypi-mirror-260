from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='astroismlib',
      version='1.1.0',
      description='Utilities to handle models of shock and ionization',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='J. A. Hernandez-Jimenez',
      author_email='joseaher@gmail.com',
      url = "https://gitlab.com/joseaher/astroismlib",
      packages=['model_shock', 'model_ionization', 'extinction','metallicity',
                'HIIregs','examples'],
      package_data = {'model_ionization':['models_phot/Peg_cont_n10/*',
                                         'models_phot/Peg_cont_n350/*',
                                         'models_phot/Peg_inst_n10/*',
                                         'models_phot/Peg_inst_n350/*',
                                         'models_phot/SB99_cont_n10/*',
                                         'models_phot/SB99_cont_n350/*',
                                         'models_phot/SB99_inst_n10/*',
                                         'models_phot/SB99_inst_n10/*',],
                      'model_shock':['models_shock/*'],
                      'HIIregs':['temden/*'],
                      'examples':['*']
                     }
      )
