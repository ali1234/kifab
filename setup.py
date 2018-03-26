from setuptools import setup

setup(
    name='kifab',
    keywords='kicad',
    version='0.1',
    author='Alistair Buxton',
    author_email='a.j.buxton@gmail.com',
    url='http://github.com/ali1234/kifab',
    license='GPLv3+',
    platforms=['linux'],
    packages=['kifab'],
    entry_points={
        'console_scripts': [
            'kifab = kifab.kifab:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
)