ZipFileTransport Tool
=====================

  This tool is used to import and export zip files.

Installation
------------

  For full installation instructions see the "INSTALL.txt" file.

Features
--------

  * Import of the file system objects (within zipfile) into Plone objects

  * Export of content objects to a zip file.
  
  * Adds two action buttons (import/export) to the bottom of folder_contents view.
  
  * Custom settings for creating your own created content types.

Requires
--------

  * Plone 3.0.0 and greater

  * Zope 2.10.4 and greater


How to run the tests for this egg (Unix):
-----------------------------------------

*Plone 3*

Make sure you are using Python-2.4.*

Check the egg trunk out into a directory:

svn co https://svn.plone.org/svn/collective/collective.zipfiletransport/trunk collective.zipfiletransport

Download bootstrap.py and run it:

wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py

python bootstrap.py -c test-plone-3.3.x.cfg

Run the buildout:

./bin/buildout -vc test-plone-3.3.x.cfg

Now run the tests::

./bin/test -s collective.zipfiletransport







