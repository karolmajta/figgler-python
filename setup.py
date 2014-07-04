from setuptools import setup
 
setup(
    name = "figgler",
    version = "1.1.4",
    package_dir = {
        '': 'src',
    },
    packages = [
        'figgler',
    ],

    install_requires = [],

    author = "Karol Majta",
    author_email = "karolmajta@gmail.com",
    description = "Utilities for reading environment variables in containers instrumented with fig.",
    license = "MIT",
    url = "https://github.com/karolmajta/figgler-python",
    
    cmdclass = {
        'test': RunUnittests,
    },
)
