from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Simple Interface for Camera Streams in Python'
LONG_DESCRIPTION = 'A simple interface for camera streams in Python using OpenCV and Tkinter.'

# Setting up
setup(
    name="camconnect",
    version=VERSION,
    author="Aimar Abimayu Pratama",
    author_email="aimarabimanyu123@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['opencv-python', 'tk', 'Pillow'],
    keywords=['python', 'interface', 'stream', 'camera', 'opencv', 'tkinter'],
    license="MIT",
    url="https://github.com/aimarabimanyu/camconnect.git",
    project_urls={
        'Source': 'https://github.com/aimarabimanyu/camconnect.git',
    },
)
