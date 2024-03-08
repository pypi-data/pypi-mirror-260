from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    ABOUT = f.read()


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Plugins',
    'Programming Language :: Python',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
]    


setup(name="OrangeARFF",
      packages=["OrangeARFF"],
      package_data={"OrangeARFF": []},
      entry_points={"orange.widgets": "OrangeARFF = OrangeARFF"},
      version="1.0.3",
      author="Gualberto Asencio Cortés",
      author_email="guaasecor@upo.es",
      keywords=['orange3 add-on','OrangeARFF','Orange.data.io mining','orange','addon'],
      url="https://github.com/gualbe/Orange-ARFF",
      license="GPL3+",
      long_description=ABOUT,
      long_description_content_type='text/markdown',
      description="AFFF add-on for Orange 3 Orange.data.io mining software.",
      classifiers=CLASSIFIERS,
      )
