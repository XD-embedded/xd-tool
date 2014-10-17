try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils import setup, find_packages

from xd.tool import __version__

setup(
    name="XD-tool",
    version=__version__,

    packages=find_packages(exclude=['_test']),
    py_modules=['ez_setup'],
    entry_points={'console_scripts': ['xd = xd.tool.main:main']},

    # metadata for upload to PyPI
    author="Esben Haabendal",
    author_email="esben@haabendal.dk",
    description="XD-tool - command line tool for XD-embedded",
    license="MIT",
    url="http://www.xd-embedded.org/xd-tool",
    keywords=['build', 'embedded', 'linux'],

    # nose integration
    setup_requires=['nose>=1.0'],
    tests_require=['coverage'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Build Tools',
        ],
)
