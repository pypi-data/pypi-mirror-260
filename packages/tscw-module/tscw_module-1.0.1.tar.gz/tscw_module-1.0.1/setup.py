from setuptools import setup

# def readme():
#     with open('README.rst') as f:
#         return f.read()

setup(name='tscw_module',
      version='1.0.1',
      description='Module to create input and process output of TSCW Software',
      long_description="Module to create input and process output of TSCW Software (c) UGS GmbH",
      author='Thomas Simader',
      author_email='simader@ugsnet.de',
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        ],
      packages=['tscw_module',],
      include_package_data=True,
      zip_safe=False,
      install_requires = [
        'matplotlib',
        'matplotlib-inline',
        'mplcursors',
        'numpy',
        'pandas',
        'pathlib',
        'scipy',
        'Sphinx',
        'sphinx-autodoc-typehints',
        'sphinx-rtd-theme',
        'sphinxcontrib-applehelp',
        'sphinxcontrib-devhelp',
        'sphinxcontrib-htmlhelp',
        'sphinxcontrib-jquery',
        'sphinxcontrib-jsmath',
        'sphinxcontrib-qthelp',
        'sphinxcontrib-serializinghtml',
        'tqdm',
        'openpyxl',
      ]
)


# [tool.poetry.dependencies]
# python = "^3.6"
# matplotlib = "^3.0"
# matplotlib-inline = "^0.1"
# mplcursors = "^0.3"
# numpy = "^1.15"
# pandas = "^0.23"
# pathlib = "^1.0"
# scipy = "^1.1"
# Sphinx = "^3.0"
# sphinx-autodoc-typehints = "^1.11"
# sphinx-rtd-theme = "^0.5"
# sphinxcontrib-applehelp = "^1.0"
# sphinxcontrib-devhelp = "^1.0"
# sphinxcontrib-htmlhelp = "^1.0"
# sphinxcontrib-jquery = "^1.0"
# sphinxcontrib-jsmath = "^1.0"
# sphinxcontrib-qthelp = "^1.0"
# sphinxcontrib-serializinghtml = "^1.1"
# tqdm = "^4.40"

# [tool.poetry.files]
# "README.md" = "README.md"
# "LICENSE.txt" = "LICENSE.txt"
# "calculateForces_benchmark.py" = "calculateForces_benchmark.py"
# "docs" = "docs"
# "tscw_module/ffmpeg" = "tscw_module/ffmpeg"