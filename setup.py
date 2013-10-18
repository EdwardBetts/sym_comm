from setuptools import setup, find_packages

setup(
    name = "SimpleCommodities",
    version = "0.0.1",
    packages = find_packages(),
    scripts = ['gltest.py'],

    install_requires = ['docutils>=0.3',
                        'pyglet>=1.1.4',
                        'PIL>=1.1.6'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    }

    # metadata for upload to PyPI
    # author = "Jason Katzwinkel",
    # author_email = "jk@winkel.com",
    # description = "",
    # license = "",
    # keywords = "",
    # url = "",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
