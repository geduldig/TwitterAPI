Instructions for Generating Documentation with Sphinx
=====================================================

MAKE NEW DOCS IN MASTER BRANCH::

	git clone git@github.com:geduldig/TwitterAPI.git
	cd TwitterAPI/docs
	make html

DOWNLOAD OLD DOCS FROM GH-PAGES BRANCH::

	cd gh-pages
	git clone -b gh-pages git@github.com:geduldig/TwitterAPI.git

COPY NEW DOCS OVER OLD DOCS::

	cp TwitterAPI/docs/_build/html/*.* gh-pages/TwitterAPI
	cp -r TwitterAPI/docs/_build/html/* gh-pages/TwitterAPI
	rm -r TwitterAPI/docs/_build
					
UPLOAD NEW DOCS TO GH-PAGES BRANCH:::

	cd gh-pages/TwitterAPI
	git commit -am "2.5 docs"
	git push origin gh-pages
