=====================
Developer Quick Start
=====================

This section will get you up and running with CultureMesh FFB.

.. _getting-started:

Getting Started
===============

TODO

Environment Variables
---------------------

You need to define two environment variables before you can start the
application.

======================  ====================================================================
  Variable                   Purpose
======================  ====================================================================
WTF_CSRF_SECRET_KEY     A secret of your choosing for generating and validating CSRF tokens
CULTUREMESH_API_KEY     The key to access the CultureMesh API
======================  ====================================================================

Theme options
-------------

.. code-block:: python

    html_theme_options = {
        'logo': 'logo.png',
        'github_user': 'bitprophet',
        'github_repo': 'alabaster',
    }


Variables and feature toggles
-----------------------------

  .. note:: This value must end with a trailing slash.
