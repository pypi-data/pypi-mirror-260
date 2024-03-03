=========
GDT-RXTE
=========

The GDT-RXTE is an extension to Gamma-ray Data Tools that adds functions specific to the RXTE mission.

Normal Installation
-------------------

If you don't plan to contribute code to the project, the recommended install method is installing from PyPI using:

.. code-block:: sh

   pip install astro-gdt-rxte
   gdt-data init

The ``gdt-data init`` is required to initialize the library after installation of astro-gdt. You do not need to
perform the initialization again if astro-gdt was already installed and initialized.  There is no harm in running
it again "just in case".


Writing Extensions using Namespace Packaging
--------------------------------------------
This is an extension to astro-gdt and should should contain a directory 'gdt' with a subdirectory 'missions' which will hold the extension code
in a package directory named after the mission.

For example, GDT-RXTE has the following directory layout::

  .
  ├── config
  ├── dist
  ├── docs
  ├── src
  │   └── gdt
  │      └── missions
  │          └── rxte
  │              └── __init__.py
  └── tests
    └── missions
        └── rxte


Since GDT-RXTE uses namespace packaging, both ``src/gdt`` and  ``src/gdt/missions`` do not contain a file named
``__init__.py``. This is because they are Namespace packages.

Notice that directory ``src/gdt/mission/rxte`` contains an `__init__.py` file
signalling to Python that those directories are regular packages.

You can learn more about Namespace packages by reading `PEP-420 <https://peps.python.org/pep-0420/>`_.

Helping with Documentation
--------------------------

You can contribute additions and changes to the documentation. In order to use sphinx to compile the documentation
source files, we recommend that you install the packages contained within ``requirments.txt``.

To compile the documentation, use the following commands:

.. code-block:: sh

   cd $PROJ_ROOT/docs
   make html

