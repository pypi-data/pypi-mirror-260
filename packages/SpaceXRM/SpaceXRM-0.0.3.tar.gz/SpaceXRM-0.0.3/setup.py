from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Special package'
# LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="SpaceXRM",
    version=VERSION,
    author="Ramiz Al-Jabri",
    author_email="<ramzalgabry232@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pycountry', 'phonenumbers', 'phone_iso3166', 'colorama', 'curl_cffi', 'selenium_profiles', 'playwright', 'selenium', 'ua_generator', 'bs4'],
    keywords=['python', 'selenium', 'playwright', 'selenium_profiles', 'curl_cffi', 'requests'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)