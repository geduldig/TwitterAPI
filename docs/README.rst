Instructions for Generating Documentation with Sphinx
=====================================================

MAKE NEW DOCS IN MASTER BRANCH::

	clone git@github.com:geduldig/TwitterAPI.git
	cd TwitterAPI/docs
	make html

DOWNLOAD OLD DOCS FROM GH-PAGES BRANCH::

	cd TwitterAPI-docs
	clone -b gh-pages git@github.com:geduldig/TwitterAPI.git

COPY NEW DOCS OVER OLD DOCS::

	cp TwitterAPI/docs/_build/html/*.* TwitterAPI-docs/TwitterAPI
	cp -r TwitterAPI/docs/_build/html/* TwitterAPI-docs/TwitterAPI
	rm -r TwitterAPI/docs/_build
					
UPLOAD NEW DOCS TO GH-PAGES BRANCH:::

	git commit -am "2.5 docs"
	git push origin gh-pages
