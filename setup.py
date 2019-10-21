import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    README = fh.read()

setuptools.setup(
    name="hikingmap",
    version="0.0.1",
    license='GNU General Public License (GNU GPL v3 or above)',
    author="Roel Derickx",
    author_email="hikingmap.pypi@derickx.be",
    description="A script to calculate the minimum amount of pages needed to render one or more GPX tracks",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/roelderickx/hikingmap",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['hikingmap = hikingmap.hikingmap:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)

