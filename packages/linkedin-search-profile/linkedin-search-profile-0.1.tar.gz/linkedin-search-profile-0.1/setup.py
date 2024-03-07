from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent

setup(
    name = 'linkedin-search-profile',
    packages = ['linkedin-search-profile'],
    version = '0.1',
    license='ISC',
    description = 'Automates the process of searching for LinkedIn profiles for a given list of names and compiles their profile URLs in an Excel file.',
    author = 'gvoze32',
    author_email = 'gvoze32@gmail.com',
    keywords = ['linkedin'],
  install_requires=[
          'pandas==2.2.0',
          'selenium==4.18.1',
          'openpyxl==3.1.2',
          'pyarrow==15.0.0',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3.10',
  ],
)