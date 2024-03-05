try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = """algaestat is a package to extract, transform and aggregate Algae cultivation data. 
A series of proprietary and open-source instruments collected this data: 
Burge Environmental MiProbe (Algae Probe), YSI (Algae Probe), HoboLink (Weather Data)
pH Meters.
Free from notebook entries are also accessible.
Cultivation data.
- Algae Pool Status including, levels, temperature. 
- This package contains classes to: 
- Query the WS Dynomodb (where the data is stored).
- Extract data from AWS Dynomodb, 
- Transform and aggregate the data to relational tables or JSON formats.
- Export results as files (i.e. csv)
"""

major = 1
minor = 0
revision = 2
version = '%d.%d.%d' % (major, minor, revision)

setup(name='algaestat',
      version=version,
      description='Algae cultivating data extract-transform-load package',
      author='David A. Baker',
      url='https://azcati.asu.edu/',
      long_description=long_description,
      packages=['algaestat','algaestat.io','algaestat.utils'],
      install_requires=['pandas', 'boto3', 'simplejson','csaps','importlib_resources', 'numpy'],
      python_requires='>3.10.0',
      include_package_data=True,
      license_files = ('LICENSE',),
      classifiers=[
              "Intended Audience :: Manufacturing ",
                "License :: Other/Proprietary License",
              "Programming Language :: Python :: 3 :: Only"
          ]
)