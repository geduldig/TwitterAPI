Instructions for Generating Documentation with Sphinx
=====================================================

Generate HTML Files
-------------------

In a command shell::

	cd TwitterAPI\docs

Edit RST files.

In a command shell::

	make html

Open in a browser::

	TwitterAPI\docs\_build\html\index.html

Repeat until happy

Clean Up
--------

In a command shell::

	rm -r TwitterAPI\docs\_build

Publish to Git Repository
-------------------------

In a command shell::

	git add *
	git commit -am '2.2.4 docs'
	git push origin gh-pages
