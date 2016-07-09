from distutils.core import setup
from TwitterAPI import __version__
import io


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(
    name='TwitterAPI',
    version=__version__,
    author='geduldig',
    author_email='boxnumber03@gmail.com',
    packages=['TwitterAPI'],
    package_data={'': ['credentials.txt']},
    url='https://github.com/geduldig/TwitterAPI',
    download_url='https://github.com/geduldig/TwitterAPI/tarball/master',
    license='MIT',
    keywords='twitter',
    description='Minimal wrapper for Twitter\'s REST and Streaming APIs',
    install_requires=['requests', 'requests_oauthlib']
)
