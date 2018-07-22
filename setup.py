import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='opencv_iav',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    description='Take a picture or record a video using OpenCV.',
    long_description=README,
    author='Mike Cornwell',
    author_email='michael.a.cornwell@gmail.com',
    url='https://github.com/macornwell/opencv-image-and-video',
    install_requires=['opencv-python',],
    entry_points = {
        'console_scripts': ['opencv_iav=opencv_iav.opencv_iav:main'],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

