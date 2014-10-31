from setuptools import setup, find_packages, findall  # Always prefer setuptools over distutils

setup(
    name='hatbot_resources',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    # version='1.2.0',

    description='A sample Python project',
    # long_description=long_description,

    # The project's main homepage.
    url='https://github.com/hatbot-team/hatbot_resources',

    # Author details
    author='Hatbot Team',
    # author_email='pypa-dev@googlegroups.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 1 - Raw',

        # Indicate who your project is intended for
        'Intended Audience :: Hatbot Team Projects',

        'Topic :: Entertainment :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='hat ai resources hatbot huge-data',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(include=('hb_res', 'hb_res.*')),

    package_data={
        'hb_res.storage': findall('hb_res/assets')
    },

    install_requires=['pymorphy2'],

    extras_require={
        'web': ['beautifulsoup4', 'requests'],
    }
)
