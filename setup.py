from distutils.core import setup

setup(
    name='TwitterAPI',
    version='1.0.0',
    author='Jonas Geduldig',
    author_email='boxnumber03@gmail.com',
    packages=['twitterapi', 'twitterapi.test', 'twitterapi.tools'],
	package_data={'': ['credentials.txt']},
    url='https://github.com/geduldig/twitterapi',
    download_url = 'https://github.com/gedldig/twitterapi/tarball/1.0.0',
    license='MIT',
    keywords='twitter',
    description='Classes for interacting with twitter.com.',
    long_description=open('README.txt').read(),
    install_requires = ['oauth2']
)