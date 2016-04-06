# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# Read in long_description from README.rst.  By using a separate file, instead
# of translating README.md, we can use different content on PyPI than on
# GitHub.
with open('README.rst') as readme_file:
    long_description = readme_file.read()

# As PyPI only accepts PEP 440 non-local version strings, we need to strip
# down the version generated for non-tagged commits.
def version_config():
    import os
    if os.environ.get('TRAVIS_TAG'):
        return True
    from setuptools_scm.version import postrelease_version
    # Use a version like 1.1.0.54 for commit with distance 54 from v1.1.0 tag
    def version_scheme(version):
        return postrelease_version(version).replace('post', '')
    def local_scheme(version):
        return ''
    return {'version_scheme': version_scheme, 'local_scheme': local_scheme}

setup(
    # Name of project, see PEP 426
    name="XD-tool",

    # Short and long descriptions, will be displayed on PyPI.
    description='Command-line tool for XD-embedded',
    long_description=long_description,
    url="http://www.xd-embedded.org/xd-tool",
    author='Esben Haabendal',
    author_email='esben@haabendal.dk',
    license='MIT',

    # Version number, see PEP 440
    use_scm_version=version_config,

    # metadata for upload to PyPI
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'Operating System :: Unix',
        'Environment :: Console',
        ],
    keywords=['build', 'embedded', 'linux'],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={'console_scripts': ['xd = xd.tool.main:main']},

    # Run-time dependencies
    install_requires=['sh'],

    # Dependencies needed for setup.py to run
    setup_requires=['setuptools_scm'],

    tests_require=['nose>=1.0', 'coverage'],
    test_suite='nose.collector',
)
