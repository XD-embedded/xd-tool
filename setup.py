try:
    import ez_setup
    ez_setup.use_setuptools(version="5.5.1")
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

    install_requires=['sh'],
    setup_requires=[],
    tests_require=['nose>=1.0', 'coverage'],

    # metadata for upload to PyPI
    author="Esben Haabendal",
    author_email="esben@haabendal.dk",
    description="""Command line tool for XD-embedded.
XD-tool provides a shell CLI command used to interact with XD-embedded
manifest.  It supports basic manifest management, and a command plugin
framework, so that manifest layers can provide commands.""",
    license="MIT",
    url="http://www.xd-embedded.org/xd-tool",
    keywords=['build', 'embedded', 'linux'],
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

    test_suite='nose.collector',
)
