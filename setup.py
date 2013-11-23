from setuptools import setup, find_packages

setup(
    name = "SimpleCommodities",
    description = "simulation stuff.",
    version = "0.0.1",

    long_description = open('README.md').read(),
    
    packages = find_packages(),
    scripts = ['gltest.py', 'texgen.py'],

    install_requires = ['docutils>=0.3',
                        'pyglet>=1.1.4',
                        'PIL>=1.1.6'],

    entry_points = {
            'console_scripts': []
        },
    # metadata for upload to PyPI
    # author = "Jason Katzwinkel",
    # author_email = "jk@winkel.com",
    # description = "",
    # license = "",
    # keywords = "",
    # url = "",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
