``packages`` key - Additional Packages
======================================

Additional packages can be installed by specifying them under the top-level ``packages`` key. The OU Container Builder
supports installing additional packages via ``apt`` and ``pip``:

.. code:: yaml

    packages:
      apt:     # Additional packages to install via the apt package manager
      pip:     # Additional packages to install via the pip package manager

``apt`` - Additional apt packages
---------------------------------

The apt configuration setting supports a list of package names that are then installed via ``apt-get install -y``

.. code:: yaml

    packages:
      apt:
        - pkg-name  # The name of the package to install

``pip`` - Additional python packages
------------------------------------

The pip configuration setting supports a list of package names that are then installed via ``pip install --no-cache-dir``

.. code:: yaml

    packages:
      pip:
        - pkg-name  # The name of the package to install (can be any valid pip package requirement)

.. note::

    It is recommended that you provide at least an upper version limit for any python packages, so that in case the
    VCE has to be rebuilt for security issues, there are no incompatible updates to these packages.

.. warning::

    The pip installer does not ensure that any system packages required by a pip package are automatically installed.
    These system package dependencies **must** be explicitly listed under the ``apt`` key.

Examples
--------

.. code:: yaml

    packages:
      apt:
        - curl

.. code:: yaml

    packages:
      pip:
        - Sphinx>=5.0.0
