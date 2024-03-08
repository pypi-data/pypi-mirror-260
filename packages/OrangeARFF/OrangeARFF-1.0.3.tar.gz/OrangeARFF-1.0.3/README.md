Orange3 ARFF
===============

ARFF add-on for [Orange] 3 data mining software provides load and save functionality to retrieve and store data in the Weka ARFF file format. **No new widgets are provided in this package**. The Orange native nodes **File** and **Save Data** will have full support to read/write ARFF files (.arff).

[Orange]: https://orangedatamining.com/

Installation
------------

### Orange add-on installer

Install from Orange add-on installer through Options -> Add-ons. Press button "**Add more...**", write the name "**OrangeARFF**" and press "**Add**" button.

### Using pip

To install the add-on with pip use

    pip install OrangeARFF

To install the add-on from source, run

    python setup.py install

To register this add-on with Orange, but keep the code in the development directory (do not copy it to 
Python's site-packages directory), run

    python setup.py develop

You can also run

    pip install -e .

which is sometimes preferable as you can *pip uninstall* packages later.

### Anaconda

If using Anaconda Python distribution, simply run

    pip install OrangeARFF

**Required Dependencies**:
* numpy>=1.22.4
* AnyQt>=0.2.0
* Orange3>=3.30.0
* PyQt6>=6.5.0
* scipy>=1.7.3

Usage
-----

After the installation, the widgets from this add-on are registered with Orange. To run Orange from the terminal,
use

    orange-canvas

or

    python3 -m Orange.canvas
