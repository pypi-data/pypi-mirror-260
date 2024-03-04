from setuptools import setup
import sys

if not sys.version_info[0] == 3 and sys.version_info[1] < 8:
    sys.exit('Python < 3.8 is not supported')

version = '1.1.3'

setup(
    name='steampyplus',
    packages=['steampy', 'test', 'examples', ],
    version=version,
    description='A Steam lib for trade automation',
    author='kurt',
    author_email='kurt.loong@foxmail.com',
    license='MIT',
    url='https://github.com/kurtloong/steampy',
    download_url='https://github.com/kurtloong/steampy/tarball/' + version,
    keywords=['steam', 'trade', ],
    classifiers=[],
    install_requires=[
        "requests",
        "beautifulsoup4",
        "rsa"
    ],
)
