from distutils.core import setup

setup(
    name='TwitterAPI',
    version='2.0.9.1',
    author='Jonas Geduldig',
    author_email='boxnumber03@gmail.com',
    packages=['TwitterAPI'],
    package_data={'': ['credentials.txt']},
    url='https://github.com/geduldig/TwitterAPI',
    download_url = 'https://github.com/geduldig/TwitterAPI/tarball/master',
    license='MIT',
    keywords='twitter',
    description='Easy access to all twitter.com endpoints',
    install_requires = ['requests', 'requests-oauthlib']
)
