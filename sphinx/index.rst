.. CEDA Example Python code for style guidance and conventions documentation master file, created by
   sphinx-quickstart on Fri Sep 21 12:49:20 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CEDA Example Python code for style guidance and conventions's documentation!
=======================================================================================
To make these pages I made sphinx directory in the top-level directory::

   $ mkdir sphinx 

for this directory I ran this command accepting all the defaults::

   $ sphinx-quickstart

I then ran this command to generate the module content::

   $ sphinx-apidoc -o . ..
   
I then modified ``conf.py``, add ``..`` to the ``sys.path`` variable.  I also 
modified the ``copyright`` and ``version`` variables.
   
.. toctree::
   :maxdepth: 2
   :caption: Contents:

I also added a ``clean`` target to the default ``Makefile`` so that the 
``_build`` directory is removed.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
