Instructions for Generating Documentation with Sphinx
=====================================================

INSTALL SPHINX::

	pip3 install -U Sphinx

MAKE NEW DOCS IN MASTER BRANCH::

	git clone git@github.com:geduldig/TwitterAPI.git
	cd TwitterAPI/docs
	vi conf.py (modify version and release)
	make html

TEST DOC WEB PAGE::

	TwitterAPI/docs/_build/html/index.html 

DOWNLOAD OLD DOCS FROM GH-PAGES BRANCH::

	cd ..
	mkdir TwitterAPI-docs
	cd TwitterAPI-docs
	git clone -b gh-pages git@github.com:geduldig/TwitterAPI.git

COPY NEW DOCS OVER OLD DOCS::

	cd ..
	cp TwitterAPI/docs/_build/html/*.* TwitterAPI-docs/TwitterAPI
	cp -r TwitterAPI/docs/_build/html/* TwitterAPI-docs/TwitterAPI
	rm -r TwitterAPI/docs/_build
					
UPLOAD NEW DOCS TO GH-PAGES BRANCH:::

	git commit -am "2.5 docs"
	git push origin gh-pages
